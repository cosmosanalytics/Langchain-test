"""Lesson 2 - Build a tool-calling agent with LangGraph.

An agent is a loop:  model -> (wants a tool?) -> run tool -> model -> ... -> answer.
LangGraph models that loop as a graph:
  - State: a typed dict every node reads and updates (here: the message list)
  - Nodes: plain Python functions
  - Edges: which node runs next (conditional edges = branching)
  - Checkpointer: saves state per thread_id, giving the agent memory

Run:  python lesson2_langgraph.py
"""

import ast
import operator
from datetime import datetime, timezone
from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from config import get_model

# ---------------------------------------------------------------- tools

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("unsupported expression")


@tool
def calculator(expression: str) -> str:
    """Evaluate an arithmetic expression, e.g. '(17 * 23) + 4**2'. Use for any math."""
    try:
        return str(_eval(ast.parse(expression, mode="eval").body))
    except Exception as e:  # returned to the model so it can retry
        return f"error: {e}"


GLOSSARY = {
    "langchain": "Framework with a common interface for models, prompts, tools and retrievers.",
    "langgraph": "Library for building stateful agents as graphs of nodes and edges.",
    "langsmith": "Platform for tracing, debugging, evaluating and monitoring LLM apps.",
    "lcel": "LangChain Expression Language: compose runnables with the | operator.",
    "checkpointer": "LangGraph component that persists graph state per thread_id.",
    "toolnode": "Prebuilt LangGraph node that executes the tool calls in the last AI message.",
    "dataset": "LangSmith collection of input/reference-output examples used for evals.",
    "evaluator": "Function that scores a run's output, e.g. correctness or tool usage.",
}


@tool
def glossary(term: str) -> str:
    """Look up the official tutorial definition of a LangChain/LangGraph/LangSmith term."""
    return GLOSSARY.get(term.lower().replace(" ", ""), f"'{term}' not in glossary. Known: {', '.join(GLOSSARY)}")


@tool
def current_time() -> str:
    """Return the current UTC date and time."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


TOOLS = [calculator, glossary, current_time]

SYSTEM_PROMPT = (
    "You are a helpful tutor for LangChain, LangGraph and LangSmith. "
    "Use the calculator for any arithmetic and the glossary for definitions of terms. "
    "Keep answers short."
)

# ---------------------------------------------------------------- graph


class State(TypedDict):
    # add_messages is a *reducer*: node outputs are appended, not overwritten.
    messages: Annotated[list[AnyMessage], add_messages]


def build_agent(checkpointer=None):
    model = get_model().bind_tools(TOOLS)

    def agent(state: State):
        response = model.invoke([SystemMessage(SYSTEM_PROMPT)] + state["messages"])
        return {"messages": [response]}

    graph = StateGraph(State)
    graph.add_node("agent", agent)
    graph.add_node("tools", ToolNode(TOOLS))
    graph.add_edge(START, "agent")
    # tools_condition routes to "tools" if the AI message has tool_calls, else END.
    graph.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")  # loop back so the model sees tool results
    return graph.compile(checkpointer=checkpointer)


# ---------------------------------------------------------------- demo


def demo():
    app = build_agent(checkpointer=InMemorySaver())

    print("=== Graph structure (paste into https://mermaid.live) ===")
    print(app.get_graph().draw_mermaid())

    config = {"configurable": {"thread_id": "demo-1"}}

    print("\n=== Turn 1: stream every step of the loop ===")
    question = "What is (17 * 23) + 4**2? Also, what is a checkpointer?"
    print("user:", question)
    for update in app.stream({"messages": [HumanMessage(question)]}, config, stream_mode="updates"):
        for node, payload in update.items():
            msg = payload["messages"][-1]
            if getattr(msg, "tool_calls", None):
                print(f"[{node}] calls -> {[(c['name'], c['args']) for c in msg.tool_calls]}")
            else:
                print(f"[{node}] {msg.type}: {msg.content}")

    print("\n=== Turn 2: memory (same thread_id) ===")
    follow_up = "Multiply the number you computed by 2."
    print("user:", follow_up)
    result = app.invoke({"messages": [HumanMessage(follow_up)]}, config)
    print("agent:", result["messages"][-1].content)

    print("\n=== Turn 3: new thread_id = no memory ===")
    result = app.invoke({"messages": [HumanMessage(follow_up)]}, {"configurable": {"thread_id": "demo-2"}})
    print("agent:", result["messages"][-1].content)

    state = app.get_state(config)
    print(f"\nThread demo-1 holds {len(state.values['messages'])} messages in its checkpoint.")


if __name__ == "__main__":
    demo()
