"""Streamlit demo: Explainable AI Agent with Model-Based Evaluation.  Run: streamlit run app.py"""
import hmac
import os
import uuid

import pandas as pd
import streamlit as st
from langsmith import Client, evaluate, tracing_context

import core
from cases import NEW_CASES, PAST_CASES

st.set_page_config(page_title="Explainable AI Agent", layout="wide")

APP_PASSWORD = os.getenv("APP_PASSWORD")
if APP_PASSWORD and not st.session_state.get("authed"):
    st.title("Explainable AI Agent with Model-Based Evaluation")
    pw = st.text_input("Password", type="password")
    if pw and hmac.compare_digest(pw, APP_PASSWORD):
        st.session_state["authed"] = True
        st.rerun()
    elif pw:
        st.error("Wrong password")
    st.stop()
PROJECT = os.getenv("LANGSMITH_PROJECT", "explainable-agent")
EVAL_DATASET = os.getenv("EVAL_DATASET", "claims-new-cases")
TRACING = os.getenv("LANGSMITH_TRACING", "").lower() == "true" and bool(os.getenv("LANGSMITH_API_KEY"))


@st.cache_resource
def ls_client():
    return Client() if TRACING else None


def trace_url(run_id: str) -> str | None:
    try:
        ls_client().flush()
        return ls_client().read_run(run_id).url
    except Exception:
        return None


def fsm_dot(wm: dict, highlight: tuple | None = None, bad: bool = False) -> str:
    lines = ['digraph { rankdir=LR; bgcolor="transparent"; node [shape=box style="rounded,filled" '
             'fillcolor="#f3eefa" color="#8c6bc2" fontname="Helvetica" fontsize=11]; '
             'edge [fontname="Helvetica" fontsize=9 color="#9aa6bd"];']
    for r in wm["rules"]:
        style = ""
        if highlight == (r["from_state"], r["to_state"]):
            style = ' color="#2f9e5a" penwidth=3 fontcolor="#2f9e5a"'
        lines.append(f'"{r["from_state"]}" -> "{r["to_state"]}" [label="{",".join(r["source_cases"])}"{style}];')
    if highlight and bad and highlight not in {(r["from_state"], r["to_state"]) for r in wm["rules"]}:
        lines.append(f'"{highlight[0]}" -> "{highlight[1]}" [label="agent (not in model)" color="#e0306a" '
                     f'fontcolor="#e0306a" style=dashed penwidth=3];')
    return "\n".join(lines) + "}"


def md(text: str) -> str:
    return text.replace("$", "\\$")


def scorecard(results: list[dict]):
    for r in results:
        badge = ":green-background[PASS]" if r["score"] == 1 else (
            ":red-background[FAIL]" if r["score"] == 0 else ":blue-background[SCORE]")
        st.markdown(f"{badge} **{r['key']}** = `{r['score']}`  \n:gray[{md(r['comment'])}]")


st.title("Explainable AI Agent with Model-Based Evaluation")
st.caption("Many cases → **one world model**. The world model plus each case's ground truth (when it exists) "
           "is the reference for scoring. The agent stack runs unchanged; only the scorer changes.")
with st.sidebar:
    st.subheader("Stack")
    st.markdown(f"- **LangChain**: `init_chat_model('{core.MODEL}')` + structured output\n"
                "- **LangGraph**: map-reduce consolidation, decide → verify → repair agent\n"
                f"- **LangSmith**: tracing {'ON' if TRACING else 'OFF'} · project `{PROJECT}`")
    wm_source = st.radio("World model source", ["Local file", "LangSmith dataset"],
                         help=f"LangSmith dataset: `{core.WM_DATASET}`")
    st.markdown("---\n[Request changes](https://app.devin.ai/sessions/3c2a71bed27641c98da4db72bae3ab93)")


def current_wm():
    if wm_source == "LangSmith dataset" and TRACING:
        return core.load_world_model_from_langsmith()
    return core.load_world_model()


tab1, tab2, tab3 = st.tabs(["① Build world model", "② Run agent + score", "③ Batch evaluation"])

with tab1:
    left, right = st.columns([1, 2])
    with left:
        st.subheader(f"{len(PAST_CASES)} past cases")
        for cid, text in PAST_CASES.items():
            with st.expander(cid):
                st.write(text)
        if st.button("Consolidate into a world model", type="primary"):
            with st.spinner("LangGraph: one extract_case per case (Send), then merge_and_verify…"):
                st.session_state.wm_built = core.consolidate(PAST_CASES)
            st.success("World model built and saved to world_model.json")
        if TRACING and st.button("Publish world model to LangSmith"):
            st.success(f"Saved as dataset `{core.WM_DATASET}` (one example per rule)")
            st.markdown(f"[Open in LangSmith]({core.publish_world_model(core.load_world_model())})")
    with right:
        wm = current_wm()
        if not wm:
            st.info("No world model yet. Click **Consolidate**.")
        else:
            st.subheader("World model")
            st.markdown("**Entities:** " + ", ".join(f"`{e}`" for e in wm["entities"]))
            st.graphviz_chart(fsm_dot(wm))
            st.dataframe(pd.DataFrame([{"from": r["from_state"], "to": r["to_state"],
                                        "condition(s)": " / ".join(r["conditions"]),
                                        "source cases": ", ".join(r["source_cases"]),
                                        "evidence": " | ".join(f'{e["case"]}: "{e["quote"]}"' for e in r["evidence"])}
                                       for r in wm["rules"]]), hide_index=True, use_container_width=True)
            if wm.get("dropped_ungrounded"):
                st.caption(f"Verifier dropped {len(wm['dropped_ungrounded'])} rule(s) whose evidence was not "
                           "found verbatim in the source case.")

with tab2:
    wm = current_wm()
    if not wm:
        st.info("Build the world model first (tab ①).")
    else:
        options = {f'{c["id"]}: {c["text"][:70]}…': c for c in NEW_CASES} | {"Custom case…": None}
        pick = st.selectbox("Case", list(options))
        case = options[pick] or {"id": "custom", "text": "", "current_state": "under_review", "ground_truth": None}
        text = st.text_area("Case text", case["text"], height=90)
        c1, c2, c3 = st.columns(3)
        cur = c1.selectbox("Current state", core.STATES, index=core.STATES.index(case["current_state"]))
        gt_opts = ["(none: score on world model only)"] + core.STATES
        gt = c2.selectbox("Ground truth (optional)", gt_opts,
                          index=gt_opts.index(case["ground_truth"]) if case["ground_truth"] else 0)
        gt = None if gt.startswith("(none") else gt
        sloppy = c3.toggle("Sloppy agent", help="System prompt says 'approve whenever you reasonably can'")
        if st.button("Run agent and score", type="primary") and text.strip():
            run_id = str(uuid.uuid4())
            inputs = {"case_text": text, "current_state": cur}
            with st.spinner("Agent: decide → verify → (repair)…"):
                with tracing_context(enabled=TRACING):
                    out = core.run_agent({**inputs, "sloppy": sloppy}, langsmith_extra={"run_id": run_id})
            with st.spinner("Judge: scoring against the world model…"):
                with tracing_context(enabled=TRACING):
                    results = core.judge(inputs, out, gt, wm)
            if TRACING:
                for r in results:
                    ls_client().create_feedback(run_id, key=r["key"], score=r["score"], comment=r["comment"])
            st.session_state.last = (out, results, run_id, cur)

        if "last" in st.session_state:
            out, results, run_id, cur0 = st.session_state.last
            a, b = st.columns([1, 1])
            with a:
                st.subheader("Agent output (stack unchanged)")
                st.markdown(f"**{cur0} → {out['next_state']}**  \n{md(out['rationale'])}")
                st.markdown("**Evidence cited:** " + md(" · ".join(f'"{q}"' for q in out["evidence"])))
                st.code("\n".join(out["steps"]), language="text")
                st.graphviz_chart(fsm_dot(wm, (cur0, out["next_state"]),
                                          bad=any(r["key"] == "fsm_valid" and r["score"] == 0 for r in results)))
            with b:
                st.subheader("Model-based evaluation")
                scorecard(results)
                if TRACING:
                    url = trace_url(run_id)
                    st.markdown(f"Scores were logged as feedback on the trace. "
                                + (f"[Open trace in LangSmith]({url})" if url else f"Run id `{run_id}`"))

with tab3:
    st.markdown(f"Runs `evaluate(run_agent, data='{EVAL_DATASET}', evaluators=[world_model_judge])` in LangSmith. "
                "Cases without ground truth are still scored on the world model.")
    st.dataframe(pd.DataFrame([{"id": c["id"], "current": c["current_state"],
                                "ground truth": c["ground_truth"] or "— (missing)", "case": c["text"]}
                               for c in NEW_CASES]), hide_index=True, use_container_width=True)
    sloppy_b = st.toggle("Sloppy agent", key="sloppy_batch")
    if not TRACING:
        st.warning("Set LANGSMITH_API_KEY and LANGSMITH_TRACING=true to run experiments.")
    elif st.button("Run experiment", type="primary"):
        client = ls_client()
        if not client.has_dataset(dataset_name=EVAL_DATASET):
            ds = client.create_dataset(EVAL_DATASET, description="New claim cases; some have no ground truth")
            client.create_examples(dataset_id=ds.id, examples=[
                {"inputs": {"case_text": c["text"], "current_state": c["current_state"]},
                 "outputs": {"next_state": c["ground_truth"]} if c["ground_truth"] else {},
                 "metadata": {"case_id": c["id"]}} for c in NEW_CASES])
        with st.spinner("Running experiment…"):
            res = evaluate(lambda i: core.run_agent({**i, "sloppy": sloppy_b}), data=EVAL_DATASET,
                           evaluators=[core.make_world_model_judge(current_wm())],
                           experiment_prefix="wm-judge-sloppy" if sloppy_b else "wm-judge", max_concurrency=2)
            rows = []
            for r in res:
                row = {"case": r["example"].metadata.get("case_id"), "agent": r["run"].outputs["next_state"],
                       "ground truth": (r["example"].outputs or {}).get("next_state") or "—"}
                for e in r["evaluation_results"]["results"]:
                    row[e.key] = e.score
                rows.append(row)
        st.dataframe(pd.DataFrame(rows).sort_values("case"), hide_index=True, use_container_width=True)
        st.markdown(f"[Open experiment in LangSmith]({res.url})" if getattr(res, "url", None)
                    else f"Experiment: `{res.experiment_name}`")
