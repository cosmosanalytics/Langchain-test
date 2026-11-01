"""Analysis of the Jev Lyapunov experiments.

Usage:
  python3 -I analyze.py --steps steps.jsonl --pairs calibration_pairs.csv --out summary.json

steps.jsonl: one JSON object per step (fields in SPEC.md section 10; needs phase, arm, item_id,
step, accepted, v_main, v_audit, v_true, stopped).
calibration_pairs.csv: header p,s,rule,artifact  (p = Jev probability of compliance; s = 1 if truly compliant).
"""
import argparse, csv, json
import numpy as np

def auroc(score, label):
    score = np.asarray(score, float); label = np.asarray(label, int)
    pos, neg = score[label == 1], score[label == 0]
    if len(pos) == 0 or len(neg) == 0:
        return None
    ranks = np.argsort(np.argsort(np.concatenate([pos, neg]))) + 1.0
    r_pos = ranks[: len(pos)].sum()
    return float((r_pos - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))

def calibration(path, bins=10, seed=0):
    p, s, rule = [], [], []
    for r in csv.DictReader(open(path)):
        p.append(float(r["p"])); s.append(int(r["s"])); rule.append(r["rule"])
    p, s = np.array(p), np.array(s)
    order = np.argsort(p)
    chunks = np.array_split(order, bins)
    rows, ece = [], 0.0
    rng = np.random.default_rng(seed)
    for c in chunks:
        if len(c) == 0:
            continue
        conf, acc = p[c].mean(), s[c].mean()
        boots = [s[rng.choice(c, len(c))].mean() for _ in range(500)]
        rows.append(dict(n=int(len(c)), mean_p=float(conf), accuracy=float(acc),
                         ci_lo=float(np.percentile(boots, 2.5)), ci_hi=float(np.percentile(boots, 97.5)),
                         small_bin=bool(len(c) < 30)))
        ece += len(c) / len(p) * abs(conf - acc)
    bm = np.array([r["mean_p"] for r in rows]); ba = np.array([r["accuracy"] for r in rows])
    rho = None
    if len(rows) > 2:
        rk = lambda x: np.argsort(np.argsort(x)).astype(float)
        rho = float(np.corrcoef(rk(bm), rk(ba))[0, 1])
    per_rule = {}
    for rl in sorted(set(rule)):
        m = np.array([x == rl for x in rule])
        per_rule[rl] = dict(n=int(m.sum()), accuracy_at_0_5=float(((p[m] >= 0.5) == (s[m] == 1)).mean()))
    rings = {}
    for target in (0.90, 0.99):
        best = None
        for t in np.unique(p):
            sel = p >= t
            if sel.sum() >= 30 and s[sel].mean() >= target:
                best = float(t); break
        rings[str(target)] = best   # smallest p threshold whose retained set meets the accuracy target
    return dict(n=int(len(p)), ece=float(ece), brier=float(((p - s) ** 2).mean()), auroc=auroc(p, s),
                spearman_bins=rho, bins=rows, per_rule=per_rule, ring_p_thresholds=rings,
                mean_p_satisfied=float(p[s == 1].mean()) if (s == 1).any() else None,
                mean_p_violated=float(p[s == 0].mean()) if (s == 0).any() else None)

def load_steps(path):
    return [json.loads(l) for l in open(path) if l.strip()]

def boot_diff(a, b, n=2000, seed=0):
    a, b = np.asarray(a, float), np.asarray(b, float)
    rng = np.random.default_rng(seed)
    idx = np.arange(len(a))
    d = []  # paired bootstrap over items
    for _ in range(n):
        k = rng.choice(idx, len(idx))
        d.append(a[k].mean() - b[k].mean())
    return float(np.mean(a - b)), float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))

def by_item(steps, phase, arm):
    items = {}
    for r in steps:
        if r["phase"] == phase and r["arm"] == arm:
            items.setdefault(r["item_id"], []).append(r)
    for k in items:
        items[k].sort(key=lambda r: r["step"])
    return items

def h1(steps):
    out = {}
    per = {}
    for arm in ("A0", "A1"):
        its = by_item(steps, "phase3", arm)
        rise, final, acc, tot = {}, {}, 0, 0
        for k, rows in its.items():
            prev = None; r_flag = 0
            for r in rows:
                acc += 1 if r.get("accepted") else 0; tot += 1
                if r.get("accepted") and prev is not None and r["v_true"] is not None and r["v_true"] > prev + 1e-12:
                    r_flag = 1
                if r.get("accepted") and r["v_true"] is not None:
                    prev = r["v_true"]
            rise[k] = r_flag
            final[k] = prev if prev is not None else rows[-1]["v_true"]
        per[arm] = (rise, final)
        out[arm] = dict(items=len(its), share_items_with_rise=float(np.mean(list(rise.values()))) if rise else None,
                        mean_final_v_true=float(np.mean(list(final.values()))) if final else None,
                        acceptance_rate=acc / max(1, tot))
    common = sorted(set(per["A0"][0]) & set(per["A1"][0]))
    if common:
        a = [per["A0"][0][k] for k in common]; b = [per["A1"][0][k] for k in common]
        out["diff_share_rise_A0_minus_A1"] = boot_diff(a, b)
        a = [per["A0"][1][k] for k in common]; b = [per["A1"][1][k] for k in common]
        out["diff_final_v_true_A0_minus_A1"] = boot_diff(a, b)
        r0, r1 = out["A0"]["share_items_with_rise"], out["A1"]["share_items_with_rise"]
        lo = out["diff_share_rise_A0_minus_A1"][1]
        out["H1_decision_rule"] = dict(
            gated_share_at_most_half=bool(r1 <= 0.5 * r0), ci_excludes_zero=bool(lo > 0),
            final_not_worse_by_more_than_0_02=bool(out["A1"]["mean_final_v_true"] - out["A0"]["mean_final_v_true"] <= 0.02))
    return out

def h3(steps, premature_thr=0.10):
    out = {}
    per = {}
    for arm in ("G1", "G2"):
        its = by_item(steps, "phase4", arm)
        prem, vend, n_steps, stopped = {}, {}, {}, {}
        for k, rows in its.items():
            stop_row = next((r for r in rows if r.get("stopped")), None)
            last = stop_row or rows[-1]
            stopped[k] = 1 if stop_row else 0
            prem[k] = 1 if (stop_row and stop_row["v_true"] is not None and stop_row["v_true"] > premature_thr) else 0
            vend[k] = last["v_true"]
            n_steps[k] = last["step"]
        per[arm] = (prem, vend)
        out[arm] = dict(items=len(its), premature_stop_rate=float(np.mean(list(prem.values()))) if prem else None,
                        reached_stop=float(np.mean(list(stopped.values()))) if stopped else None,
                        mean_v_true_end=float(np.mean(list(vend.values()))) if vend else None,
                        mean_steps=float(np.mean(list(n_steps.values()))) if n_steps else None)
    common = sorted(set(per["G1"][0]) & set(per["G2"][0]))
    if common:
        a = [per["G1"][0][k] for k in common]; b = [per["G2"][0][k] for k in common]
        out["diff_premature_G1_minus_G2"] = boot_diff(a, b)
        a = [per["G1"][1][k] for k in common]; b = [per["G2"][1][k] for k in common]
        out["diff_v_true_end_G1_minus_G2"] = boot_diff(a, b)
    # Goodhart gap: V_true - V_main over steps (positive means the judge is too optimistic)
    gaps = [r["v_true"] - r["v_main"] for r in steps
            if r["phase"] == "phase4" and r["arm"] == "G1" and r.get("v_true") is not None and r.get("v_main") is not None]
    out["mean_gap_true_minus_main_G1"] = float(np.mean(gaps)) if gaps else None
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps"); ap.add_argument("--pairs"); ap.add_argument("--out", default="summary.json")
    a = ap.parse_args()
    res = {}
    if a.pairs:
        res["H2_calibration"] = calibration(a.pairs)
    if a.steps:
        st = load_steps(a.steps)
        res["H1_gate"] = h1(st)
        res["H3_audit"] = h3(st)
    json.dump(res, open(a.out, "w"), indent=1)
    print(json.dumps(res, indent=1)[:3000])
