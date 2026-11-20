"""Explainable AI agent with model-based evaluation.

A. consolidate(): many past cases -> one world model (LangGraph map-reduce, LangChain structured output)
B. run_agent():   the agent (LangChain + LangGraph) decides a case's next state. It never sees the world model.
C. world_model_judge(): scores the agent against the world model, plus the case's ground truth when it exists.
Everything is traced to LangSmith when LANGSMITH_TRACING=true.
"""
import json
import operator
import os
from pathlib import Path
from typing import Annotated, Literal, Optional, TypedDict

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
from langsmith import traceable
from pydantic import BaseModel

load_dotenv()

MODEL = os.getenv("MODEL", "groq:openai/gpt-oss-120b")
WORLD_MODEL_PATH = Path(__file__).with_name("world_model.json")

State_ = Literal["submitted", "under_review", "on_hold", "approved", "denied", "escalated", "fraud_check", "paid"]
STATES = list(State_.__args__)


def llm(schema):
    return init_chat_model(MODEL, temperature=0).with_structured_output(schema).with_retry(stop_after_attempt=3)


def norm(s: str) -> str:
    return " ".join(s.lower().split()).strip(" .\"'")


def grounded(quote: str, text: str) -> bool:
    return bool(norm(quote)) and norm(quote) in norm(text)


# ---------------- A. Build the world model from many cases ----------------

class Rule(BaseModel):
    from_state: State_
    to_state: State_
    condition: str
    evidence: str


class CaseRules(BaseModel):
    entities: list[str]
    rules: list[Rule]


class BuildState(TypedDict, total=False):
    cases: dict[str, str]
    extracted: Annotated[list, operator.add]
    world_model: dict


EXTRACT_PROMPT = (
    "You build a world model of an insurance claims process.\n"
    "From this ONE case, list every state transition of the claim. Allowed states: {states}.\n"
    "Write each condition generally: no names, and specific items become their category (e.g. 'a required "
    "document is missing', not 'the medical report is missing'), but KEEP numeric thresholds such as amounts or days. "
    "Quote evidence VERBATIM from the case. In 'entities', list every generic entity type involved "
    "(e.g. customer, claim, adjuster, policy, document, payment).\n"
    "CASE: {text}"
)


def extract_case(item: dict):
    out = llm(CaseRules).invoke(EXTRACT_PROMPT.format(states=", ".join(STATES), text=item["text"]))
    rules = [dict(r.model_dump(), case_id=item["case_id"], grounded=grounded(r.evidence, item["text"]))
             for r in out.rules]
    return {"extracted": [{"case_id": item["case_id"], "entities": out.entities, "rules": rules}]}


def merge(state: BuildState):
    entities, merged = set(), {}
    for case in state["extracted"]:
        entities.update(e.lower() for e in case["entities"])
        for r in case["rules"]:
            if not r["grounded"]:
                continue  # verifier: drop rules whose evidence is not in the source case
            key = (r["from_state"], r["to_state"])
            m = merged.setdefault(key, {"from_state": key[0], "to_state": key[1], "conditions": [],
                                        "source_cases": [], "evidence": []})
            m["conditions"].append(r["condition"])
            m["source_cases"].append(r["case_id"])
            m["evidence"].append({"case": r["case_id"], "quote": r["evidence"]})
    dropped = [dict(r, case_id=c["case_id"]) for c in state["extracted"] for r in c["rules"] if not r["grounded"]]
    wm = {"entities": sorted(entities), "states": STATES,
          "rules": sorted(merged.values(), key=lambda r: (STATES.index(r["from_state"]), r["to_state"])),
          "dropped_ungrounded": dropped}
    return {"world_model": wm}


def build_consolidation_graph():
    g = StateGraph(BuildState)
    g.add_node("extract_case", extract_case)
    g.add_node("merge_and_verify", merge)
    g.add_conditional_edges(
        START, lambda s: [Send("extract_case", {"case_id": k, "text": v}) for k, v in s["cases"].items()],
        ["extract_case"])
    g.add_edge("extract_case", "merge_and_verify")
    g.add_edge("merge_and_verify", END)
    return g.compile()


@traceable(name="consolidate_world_model", tags=["world-model", "build"])
def consolidate(cases: dict[str, str]) -> dict:
    wm = build_consolidation_graph().invoke({"cases": cases})["world_model"]
    WORLD_MODEL_PATH.write_text(json.dumps(wm, indent=2))
    return wm


def load_world_model() -> Optional[dict]:
    return json.loads(WORLD_MODEL_PATH.read_text()) if WORLD_MODEL_PATH.exists() else None


# ---------------- B. The agent (unchanged stack, never sees the world model) ----------------

class Decision(BaseModel):
    next_state: State_
    rationale: str
    evidence: list[str]


class AgentState(TypedDict, total=False):
    case_text: str
    current_state: str
    sloppy: bool
    decision: dict
    unsupported: list
    repairs: int
    steps: Annotated[list, operator.add]


AGENT_PROMPT = (
    "You are a claims-processing agent. The claim is currently in state '{current}'.\n"
    "Decide the claim's NEXT state. Allowed states: {states}.\n{policy}"
    "In 'evidence', list the facts you rely on, each copied VERBATIM from the case.\nCASE: {text}{feedback}"
)
CAREFUL = "Follow normal claims practice.\n"
SLOPPY = "Customers hate waiting: approve the claim whenever you reasonably can.\n"


def decide(s: AgentState):
    fb = (f"\nThese quotes were not found verbatim in the case; fix them: {s['unsupported']}"
          if s.get("unsupported") else "")
    d = llm(Decision).invoke(AGENT_PROMPT.format(
        current=s["current_state"], states=", ".join(STATES), text=s["case_text"], feedback=fb,
        policy=SLOPPY if s.get("sloppy") else CAREFUL))
    n = s.get("repairs", -1) + 1
    return {"decision": d.model_dump(), "repairs": n,
            "steps": [f"decide{' (repair ' + str(n) + ')' if n else ''}: next_state={d.next_state}"]}


def verify(s: AgentState):
    bad = [q for q in s["decision"]["evidence"] if not grounded(q, s["case_text"])]
    return {"unsupported": bad, "steps": [f"verify: {len(bad)} unsupported quote(s)"]}


def build_agent():
    g = StateGraph(AgentState)
    g.add_node("decide", decide)
    g.add_node("verify", verify)
    g.add_edge(START, "decide")
    g.add_edge("decide", "verify")
    g.add_conditional_edges("verify", lambda s: "decide" if s["unsupported"] and s["repairs"] < 2 else END,
                            ["decide", END])
    return g.compile()


AGENT = build_agent()


@traceable(name="explainable_claims_agent", tags=["agent"])
def run_agent(inputs: dict) -> dict:
    out = AGENT.invoke({"case_text": inputs["case_text"], "current_state": inputs["current_state"],
                        "sloppy": inputs.get("sloppy", False)})
    return {**out["decision"], "current_state": inputs["current_state"], "steps": out["steps"]}


# ---------------- C. Model-based evaluation ----------------

class Expected(BaseModel):
    expected_next_state: Literal[State_, "no_matching_rule"]
    rule_condition: str
    reason: str


JUDGE_PROMPT = (
    "You are an auditor. Use ONLY the world-model rules below (learned from past cases) to decide which "
    "transition applies to this case from state '{current}'. Apply conditions by analogy (e.g. a rule about one missing document covers any missing required document). In 'rule_condition' copy the condition you used. If truly no rule applies, answer no_matching_rule.\nRULES:\n{rules}\nCASE: {text}"
)


def rules_from(wm: dict, state: str) -> list[dict]:
    return [r for r in wm["rules"] if r["from_state"] == state]


@traceable(name="world_model_judge", run_type="chain", tags=["evaluator"])
def judge(inputs: dict, outputs: dict, ground_truth: Optional[str], wm: dict) -> list[dict]:
    cur, nxt, text = inputs["current_state"], outputs["next_state"], inputs["case_text"]
    candidates = rules_from(wm, cur)
    allowed = {r["to_state"]: r for r in candidates}
    results = []

    rule = allowed.get(nxt)
    results.append({"key": "fsm_valid", "score": int(rule is not None), "comment":
                    f"{cur} -> {nxt} is in the world model (learned from {', '.join(rule['source_cases'])})."
                    if rule else f"{cur} -> {nxt} never happened in past cases. Allowed: {sorted(allowed) or 'none'}."})

    if candidates:
        listing = "\n".join(f"- {r['from_state']} -> {r['to_state']} WHEN {' / '.join(r['conditions'])}"
                            f" [cases {', '.join(r['source_cases'])}]" for r in candidates)
        exp = llm(Expected).invoke(JUDGE_PROMPT.format(current=cur, rules=listing, text=text))
        if exp.expected_next_state == "no_matching_rule":
            results.append({"key": "wm_coverage", "score": 0, "comment":
                            f"World-model gap: no past case covers this situation. {exp.reason}"})
            candidates = []
    if candidates:
        ok = exp.expected_next_state == nxt
        src = allowed.get(exp.expected_next_state, {}).get("source_cases", [])
        results.append({"key": "wm_rule_match", "score": int(ok), "comment":
                        f"World model expects {exp.expected_next_state} (rule: \"{exp.rule_condition}\", "
                        f"cases {', '.join(src)}). Agent chose {nxt}. {exp.reason}"})

    bad = [q for q in outputs.get("evidence", []) if not grounded(q, text)]
    results.append({"key": "evidence_grounded", "score": int(not bad and bool(outputs.get("evidence"))),
                    "comment": "All cited facts appear verbatim in the case." if not bad
                    else f"Not in the case: {bad}"})

    if ground_truth:
        results.append({"key": "ground_truth_match", "score": int(ground_truth == nxt),
                        "comment": f"Labeled outcome is {ground_truth}; agent chose {nxt}."})

    scored = [r for r in results if r["key"] != "wm_coverage"]
    results.append({"key": "wm_score", "score": round(sum(r["score"] for r in scored) / len(scored), 2),
                    "comment": "Mean of the checks above" + ("" if ground_truth else
                               " (no ground truth: scored on the world model alone)")})
    return results


def world_model_judge(inputs: dict, outputs: dict, reference_outputs: Optional[dict] = None) -> dict:
    """LangSmith evaluator. reference_outputs may be empty: then the world model is the only reference."""
    gt = (reference_outputs or {}).get("next_state")
    return {"results": judge(inputs, outputs, gt, load_world_model())}


# ---------------- Store the world model in LangSmith (read it back with the MCP server) ----------------

WM_DATASET = os.getenv("WM_DATASET", "claims-world-model")


def publish_world_model(wm: dict) -> str:
    """One LangSmith example per rule; each publish replaces the examples, so the dataset keeps version history."""
    from langsmith import Client
    client = Client()
    if client.has_dataset(dataset_name=WM_DATASET):
        ds = client.read_dataset(dataset_name=WM_DATASET)
        old = [e.id for e in client.list_examples(dataset_id=ds.id)]
        if old:
            client.delete_examples(example_ids=old)
    else:
        ds = client.create_dataset(WM_DATASET, description="World model consolidated from past claim cases")
    client.create_examples(dataset_id=ds.id, examples=[
        {"inputs": {"from_state": r["from_state"], "conditions": r["conditions"]},
         "outputs": {"to_state": r["to_state"], "source_cases": r["source_cases"], "evidence": r["evidence"]},
         "metadata": {"entities": wm["entities"]}} for r in wm["rules"]])
    return ds.url


def load_world_model_from_langsmith() -> Optional[dict]:
    from langsmith import Client
    client = Client()
    if not client.has_dataset(dataset_name=WM_DATASET):
        return None
    ex = list(client.list_examples(dataset_name=WM_DATASET))
    rules = [{"from_state": e.inputs["from_state"], "conditions": e.inputs["conditions"], **e.outputs} for e in ex]
    rules.sort(key=lambda r: (STATES.index(r["from_state"]), r["to_state"]))
    return {"entities": (ex[0].metadata or {}).get("entities", []) if ex else [], "states": STATES,
            "rules": rules, "dropped_ungrounded": []}
