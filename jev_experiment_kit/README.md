# Jev Lyapunov experiment kit (for antigravity)

Goal: test, with the real Jev API, whether `V(x) = sum_i w_i (1 - p_i(x))` (Jev Noul probabilities of rule compliance) can act as a Lyapunov function for an AI agent's revision loop, with a margin-based descent gate and an audit judge.

## Files

| File | What it is |
|---|---|
| `SPEC.md` | The full test specification. **Follow it exactly.** Hypotheses H1 to H3, phases, decision rules, log format |
| `policy_book.md` | The ground-truth book: fictional refund policy with 15 numbered rules |
| `rules.json` | The 15 rules: main yes/no question, independently worded audit question, weights |
| `prompts/01_query_generator.md` | Generate 300 customer queries with situation facts |
| `prompts/02_reply_writer.md` | Write a compliant reply (proposer model) |
| `prompts/03_violation_injector.md` | Inject exactly one violation, with the verification procedure |
| `prompts/04_grader.md` | Ground-truth grader (not Jev, never sees Jev output) |
| `prompts/05_proposer_honest.md` | Revision prompt for Phase 3 |
| `prompts/06_proposer_judge_pleasing.md` | Adversarial revision prompt for Phase 4 |
| `budget.json` | Spend and call caps. **Owner edits before the run** |
| `.env.example` | Names of the keys to supply as environment variables |
| `analysis/analyze.py` | Computes calibration (H2), gate vs no gate (H1) and audit (H3) from the logs |

## Setup

1. Copy `.env.example` to `.env`, fill in keys (Jev key, a proposer model key, a grader model key). Do not print keys or commit `.env`.
2. Read the Jev docs first: `https://docs.typesafe.ai/llms.txt`, then quickstart, `/primitives/noul.md`, `/concepts/state.md`, `/sdk/python.md`, `/api/system-one.md`. Do not guess the API.
3. Pin the Jev model id (list models) and record it. Use a grader model different from the proposer if possible.

## Order of work

1. Phase 0 smoke tests, then stop if checks 1, 2 or 5 fail.
2. Build the data (queries, compliant replies, seeded-violation variants verified by the grader). Split by query: 120 calibration, 180 test.
3. Phase 1 noise pilot, then Phase 2 calibration. Compute the margin window. **Stop and report if it is empty.**
4. Freeze `frozen_config.json` and record its SHA-256.
5. Phase 3 (gate vs no gate), Phase 4 (judge-chasing and audit), controls.
6. Run `analysis/analyze.py`, write `summary.md`, report spend after each phase.

## What to send back to Claude

- `steps.jsonl` (format in SPEC.md section 10) and `calibration_pairs.csv`
- `frozen_config.json` and hash, `rules.json` as used, `noise_pilot.json`
- `phase0_report.md`, `deviation_log.md`, `summary.json` and `summary.md`
- Spend per phase

## Rules that matter most

- Never tune on the test split. Never change a default after seeing test results; log any change before collecting the affected data.
- The audit judge's scores never appear in any proposer prompt.
- Report negative results as obtained. If something surprising appears, flag it and do not re-run until it changes.

## Notes from the author

- Main and audit questions were both drafted by Claude in one session, in deliberately different wording. For a stronger audit, have a different person or model rewrite `audit_question` **before** any results are seen, and record that in `deviation_log.md`.
- `analyze.py` was smoke-tested on synthetic data only. Check its output on a tiny real run before trusting it.
- Equal weights (1/15) are a default. Rules not triggered by a situation count as satisfied, so V mostly reflects triggered rules.
