# Explainable AI Agent with Model-Based Evaluation

A Streamlit demo of one idea: **many cases are consolidated into a world model, and the world model
(plus each case's ground truth, when it exists) is the reference for scoring.**
The agent stack runs unchanged; only the scorer changes. Cases with no ground truth are still scored.

```
① Build   past cases C1…C6 ──LangGraph map-reduce──▶ world model (entities + state machine, every rule cites its cases)
② Operate new case ──LangChain + LangGraph agent (decide → verify → repair)──▶ next state + evidence
③ Score   agent output + world model (+ ground truth if any) ──world_model_judge──▶ scores with reasons
          everything traced to LangSmith; scores logged as feedback / experiments
```

## Run

```bash
cd explainable-agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # add your Groq and LangSmith keys
streamlit run app.py
```

## What's where

| File | What it shows |
| --- | --- |
| `cases.py` | 6 past cases (to learn from) and 6 new cases; some new cases have no ground truth |
| `core.py` · `consolidate()` | LangGraph `Send` fan-out: one `extract_case` per case (LangChain structured output), then `merge_and_verify` drops rules whose evidence isn't verbatim in the case |
| `core.py` · `run_agent()` | The agent. It never sees the world model: `decide` → `verify` quotes → repair loop |
| `core.py` · `judge()` / `world_model_judge()` | The scorer. `fsm_valid` (transition seen in past cases), `wm_rule_match` (LLM applies the world-model rules to the case), `evidence_grounded`, `ground_truth_match` (only if labeled), `wm_score`. Each result has a `comment` that names the rule and source cases |
| `core.py` · `publish_world_model()` | Stores the world model in LangSmith as dataset `claims-world-model` (one example per rule) |
| `app.py` | ① build/publish the world model, ② run + score one case (feedback attached to the trace), ③ LangSmith `evaluate()` experiment over dataset `claims-new-cases` |
| `world_model.json` | A world model built from `cases.py`, so the app works before you click Consolidate |

## Example: scoring without ground truth

Case N3 ("$72,000 claim … all documents are present") has no label. The agent approves it.
`fsm_valid = 1` (under_review → approved is a known transition), but
`wm_rule_match = 0`: *"World model expects escalated (rule: claim amount exceeds $50,000 limit for standard review, case C4)."*

## Reading the world model through the LangSmith MCP server

The MCP server reads; the SDK writes. After **Publish world model to LangSmith**, ask an MCP client to call
`list_examples(dataset_name="claims-world-model")` to see each rule, its source cases and evidence.
