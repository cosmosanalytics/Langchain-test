"""Lesson 3 - Observe and evaluate the agent with LangSmith.

  1. Tracing: with LANGSMITH_TRACING=true every LangChain/LangGraph call is
     logged automatically. @traceable adds your own functions to the trace.
  2. Datasets: a set of inputs + reference outputs stored in LangSmith.
  3. Evaluation: run the agent over the dataset and score each run with
     evaluator functions. Results appear as an "experiment" you can compare.

Run:  python lesson3_langsmith.py
Then open LangSmith -> Projects -> agent-tutorial (traces)
                  and Datasets & Experiments -> agent-tutorial-qa (evals).
"""

import os
import re

from langchain_core.messages import HumanMessage
from langsmith import Client, evaluate, traceable

from lesson2_langgraph import build_agent

DATASET = "agent-tutorial-qa"

EXAMPLES = [
    # "answer" lists acceptable keywords: the run passes if any one appears.
    ({"question": "What is 1234 * 5678?"}, {"answer": ["7006652"], "tool": "calculator"}),
    ({"question": "What is (2**10) - 24?"}, {"answer": ["1000"], "tool": "calculator"}),
    ({"question": "What is 15% of 840?"}, {"answer": ["126"], "tool": "calculator"}),
    ({"question": "Define LCEL using the glossary."}, {"answer": ["| operator", "pipe"], "tool": "glossary"}),
    ({"question": "What does a LangSmith evaluator do?"}, {"answer": ["score", "compare", "metric"], "tool": "glossary"}),
]

agent = build_agent()


# ---------------------------------------------------------------- 1. tracing


@traceable(name="tutor_agent", tags=["lesson3"])
def run_agent(question: str) -> dict:
    """Shows up as the parent span; the LangGraph run nests under it."""
    result = agent.invoke({"messages": [HumanMessage(question)]})
    tools_used = [c["name"] for m in result["messages"] for c in getattr(m, "tool_calls", None) or []]
    return {"answer": result["messages"][-1].content, "tools_used": tools_used}


def demo_tracing():
    print("=== 1. Tracing ===")
    out = run_agent("What is 99 * 101?")
    print(out)
    print(f"-> trace logged to project '{os.getenv('LANGSMITH_PROJECT', 'default')}'")


# ---------------------------------------------------------------- 2. dataset


def ensure_dataset(client: Client):
    print("\n=== 2. Dataset ===")
    if client.has_dataset(dataset_name=DATASET):
        print(f"dataset '{DATASET}' already exists")
        return
    ds = client.create_dataset(DATASET, description="Tutor agent: math + glossary questions")
    client.create_examples(
        dataset_id=ds.id,
        inputs=[i for i, _ in EXAMPLES],
        outputs=[o for _, o in EXAMPLES],
    )
    print(f"created dataset '{DATASET}' with {len(EXAMPLES)} examples")


# ---------------------------------------------------------------- 3. evaluation


def _normalize(text: str) -> str:
    text = re.sub(r"[`*_]", "", text.lower())  # drop markdown formatting
    return re.sub(r"(?<=\d)[,\u202f ](?=\d)", "", text)  # 7,006,652 -> 7006652


def correct_answer(outputs: dict, reference_outputs: dict) -> dict:
    """Pass if any reference keyword appears in the agent's answer."""
    answer = _normalize(outputs["answer"])
    # (?<!\d)/(?!\d) stop "1000" from matching inside "21000".
    ok = any(re.search(rf"(?<!\d){re.escape(_normalize(k))}(?!\d)", answer) for k in reference_outputs["answer"])
    return {"key": "correct", "score": int(ok)}


def used_right_tool(outputs: dict, reference_outputs: dict) -> dict:
    """Pass if the agent called the tool we expected."""
    return {"key": "used_right_tool", "score": int(reference_outputs["tool"] in outputs["tools_used"])}


def target(inputs: dict) -> dict:
    return run_agent(inputs["question"])


def demo_evaluation():
    print("\n=== 3. Evaluation ===")
    results = evaluate(
        target,
        data=DATASET,
        evaluators=[correct_answer, used_right_tool],
        experiment_prefix="tutor-agent",
        max_concurrency=2,
    )
    rows = list(results)
    for r in rows:
        scores = {e.key: e.score for e in r["evaluation_results"]["results"]}
        print(f"  {r['example'].inputs['question']:<40} {scores}")
    for key in ("correct", "used_right_tool"):
        vals = [e.score for r in rows for e in r["evaluation_results"]["results"] if e.key == key]
        print(f"{key}: {sum(vals)}/{len(vals)}")
    print("experiment:", results.experiment_name)


if __name__ == "__main__":
    client = Client()
    demo_tracing()
    ensure_dataset(client)
    demo_evaluation()
