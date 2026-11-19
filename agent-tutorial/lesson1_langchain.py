"""Lesson 1 - LangChain basics.

LangChain gives every LLM provider the same interface. You learn five ideas:
  1. Chat models and messages
  2. Prompt templates
  3. LCEL: composing steps with the | operator
  4. Structured output (get a Pydantic object back, not text)
  5. Tools: let the model ask *you* to call a function

Run:  python lesson1_langchain.py
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from config import get_model

model = get_model()


def step1_chat_model():
    print("\n=== 1. Chat model + messages ===")
    messages = [
        SystemMessage("You are a concise tutor. Answer in one sentence."),
        HumanMessage("What is LangChain?"),
    ]
    reply = model.invoke(messages)  # returns an AIMessage
    print(reply.content)
    print("token usage:", reply.usage_metadata)


def step2_prompt_template():
    print("\n=== 2. Prompt template ===")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You explain {topic} to a {audience}. Max 2 sentences."),
            ("human", "{question}"),
        ]
    )
    filled = prompt.invoke(
        {"topic": "LangGraph", "audience": "Python developer", "question": "Why use it?"}
    )
    print("Messages sent to the model:")
    for m in filled.to_messages():
        print(f"  [{m.type}] {m.content}")
    return prompt


def step3_lcel_chain(prompt):
    print("\n=== 3. LCEL chain: prompt | model | parser ===")
    # Every piece is a Runnable, so they share invoke / batch / stream.
    chain = prompt | model | StrOutputParser()
    print(chain.invoke({"topic": "LangSmith", "audience": "manager", "question": "What does it do?"}))

    print("\nbatch() runs several inputs in parallel:")
    answers = chain.batch(
        [
            {"topic": "tracing", "audience": "child", "question": "What is it?"},
            {"topic": "evaluation", "audience": "child", "question": "What is it?"},
        ]
    )
    for a in answers:
        print("  -", a)

    print("\nstream() yields tokens as they arrive:")
    for chunk in chain.stream({"topic": "agents", "audience": "chef", "question": "Explain."}):
        print(chunk, end="", flush=True)
    print()


class Concept(BaseModel):
    """A single concept extracted from text."""

    name: str = Field(description="Short name of the concept")
    library: str = Field(description="One of: langchain, langgraph, langsmith")
    one_liner: str = Field(description="One-sentence definition")


def step4_structured_output():
    print("\n=== 4. Structured output ===")
    extractor = model.with_structured_output(Concept)
    concept = extractor.invoke("A checkpointer saves graph state between steps so agents remember.")
    print(type(concept).__name__, "->", concept.model_dump())


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def step5_tools():
    print("\n=== 5. Tools (tool calling) ===")
    # The docstring + type hints become the JSON schema the model sees.
    print("Schema the model sees:", multiply.args)
    # tool_choice="any" forces a tool call; the default ("auto") lets the model decide.
    model_with_tools = model.bind_tools([multiply], tool_choice="any")
    ai_msg = model_with_tools.invoke("What is 23.5 times 4.75?")
    # The model does NOT run the tool. It returns a request to call it.
    print("Model requested:", ai_msg.tool_calls)
    for call in ai_msg.tool_calls:
        print("We run it ourselves ->", multiply.invoke(call["args"]))
    print("Running tools and looping back to the model is what LangGraph automates (lesson 2).")


if __name__ == "__main__":
    step1_chat_model()
    prompt = step2_prompt_template()
    step3_lcel_chain(prompt)
    step4_structured_output()
    step5_tools()
