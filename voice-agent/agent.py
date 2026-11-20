"""Voice claims agent: speech -> text (Groq Whisper) -> LangGraph tool agent -> speech (gTTS).

The agent's tools reuse the explainable agent from core.py: every recommendation is scored against the world
model (plus the claim's ground truth when it has one), and a claim can only move along a world-model transition.
"""
import copy
import io
import os
import re

from groq import Groq
from gtts import gTTS
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langsmith import traceable

import core
from cases import NEW_CASES

STT_MODEL = os.getenv("STT_MODEL", "whisper-large-v3-turbo")

SYSTEM_PROMPT = (
    "You are a voice assistant for insurance claims adjusters. Your replies are read aloud, so answer in one to "
    "three short spoken sentences: no markdown, lists, tables or symbols, and say states in plain words "
    "(e.g. 'under review'). Always use your tools for facts about claims; never guess. Claim IDs look like N1, "
    "and the user may refer to a claim by the customer's first name. When asked what should happen to a claim, "
    "call recommend_next_state and mention its evaluation score; if the score is below 1, say why. When the user "
    "describes a case in their own words (any claim situation with details such as an amount, documents or the policy, "
    "even without saying 'new case'), or names a customer who is not in list_claims, call submit_case with their "
    "description and the customer's name, and speak "
    "the result: the decided next state, the score and, if below 1, why. Only call move_claim when the user "
    "explicitly asks you to move or update a claim."
)


def new_claims_db() -> dict:
    return {c["id"]: {**copy.deepcopy(c), "history": []} for c in NEW_CASES}


def _find(db: dict, ref: str) -> dict | None:
    norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
    key = norm(ref)
    return db.get(key.upper()) or next((c for c in db.values() if norm(c["customer"]) == key), None)


def build_tools(db: dict, wm: dict, evaluations: list):
    @tool
    def list_claims() -> list[dict]:
        """List all open claims with their ID, customer and current state."""
        return [{"id": c["id"], "customer": c["customer"], "state": c["current_state"]} for c in db.values()]

    @tool
    def get_claim(claim: str) -> dict:
        """Get the details and history of one claim, by claim ID (e.g. N3) or customer first name."""
        c = _find(db, claim)
        if not c:
            return {"error": f"No claim '{claim}'. Known: {', '.join(db)}. If the user described a case, call submit_case."}
        return {k: c[k] for k in ("id", "customer", "current_state", "text", "history")}

    def _decide_and_score(c: dict) -> dict:
        inputs = {"case_text": c["text"], "current_state": c["current_state"]}
        out = core.run_agent(inputs)
        scores = core.judge(inputs, out, c["ground_truth"] if not c["history"] else None, wm)
        evaluations.append({"claim": c["id"], "decision": out, "scores": scores})
        return {"claim": c["id"], "customer": c["customer"], "current_state": c["current_state"],
                "recommended": out["next_state"], "rationale": out["rationale"],
                "evaluation": {s["key"]: s["score"] for s in scores},
                "evaluation_reasons": [s["comment"] for s in scores if s["score"] != 1]}

    @tool
    def submit_case(description: str, current_state: str = "under_review", customer: str = "",
                    separate_claim: bool = False) -> dict:
        """Add a NEW case the user describes in their own words, then decide its next state and score that
        decision against the world model (a new case has no ground truth). Use the user's wording as description.
        Set separate_claim=true only when the user says it is another claim for a customer who already has one."""
        existing = _find(db, customer) if customer else None
        if existing and not separate_claim:
            return {"error": f"{existing['customer']} already has claim {existing['id']}. If the user means that "
                             f"claim, call recommend_next_state('{existing['id']}'); if they clearly mean another "
                             "claim, call submit_case again with separate_claim=true."}
        cur = current_state.strip().lower().replace(" ", "_")
        if cur not in core.STATES:
            cur = "under_review"
        cid = f"N{len(db) + 1}"
        while cid in db:
            cid = f"N{int(cid[1:]) + 1}"
        db[cid] = {"id": cid, "customer": customer or "new customer", "current_state": cur,
                   "ground_truth": None, "text": description, "history": []}
        return _decide_and_score(db[cid])

    @tool
    def recommend_next_state(claim: str) -> dict:
        """Ask the explainable claims agent what the claim's next state should be. The recommendation is scored
        against the world model (rules learned from past cases) and the claim's ground truth when it has one."""
        c = _find(db, claim)
        if not c:
            return {"error": f"No claim '{claim}'. Known: {', '.join(db)}. If the user described a case, call submit_case."}
        return _decide_and_score(c)

    @tool
    def explain_rules(state: str) -> list[dict]:
        """Explain the world-model rules for leaving a state (e.g. under_review): where a claim can go next,
        under which conditions, and which past cases each rule came from."""
        s = state.strip().lower().replace(" ", "_")
        return [{"to": r["to_state"], "when": r["conditions"], "source_cases": r["source_cases"]}
                for r in core.rules_from(wm, s)] or [{"error": f"No rules from '{state}'. States: {core.STATES}"}]

    @tool
    def move_claim(claim: str, new_state: str, reason: str) -> dict:
        """Move a claim to a new state. Only transitions that exist in the world model are allowed."""
        c = _find(db, claim)
        if not c:
            return {"error": f"No claim '{claim}'. Known: {', '.join(db)}. If the user described a case, call submit_case."}
        new = new_state.strip().lower().replace(" ", "_")
        allowed = [r["to_state"] for r in core.rules_from(wm, c["current_state"])]
        if new not in allowed:
            return {"error": f"{c['current_state']} -> {new} is not allowed by the world model. Allowed: {allowed}"}
        c["history"].append({"from": c["current_state"], "to": new, "reason": reason})
        c["current_state"] = new
        return {"claim": c["id"], "new_state": new}

    return [list_claims, get_claim, submit_case, recommend_next_state, explain_rules, move_claim]


def build_voice_agent(db: dict, wm: dict, evaluations: list):
    return create_agent(init_chat_model(core.MODEL, temperature=0), build_tools(db, wm, evaluations),
                        system_prompt=SYSTEM_PROMPT, checkpointer=InMemorySaver())


@traceable(name="speech_to_text", run_type="tool", tags=["voice", "stt"],
           process_inputs=lambda i: {"audio_bytes": len(i.get("audio") or b"")})
def transcribe(audio: bytes, filename: str = "speech.wav") -> str:
    r = Groq().audio.transcriptions.create(
        file=(filename, audio), model=STT_MODEL, language="en",
        prompt="Insurance claims. Claim IDs like N1, N2, N3. Customers: Grace, Hiro, Ivy, Jon, Kim, Leo. "
               "Under review, on hold, escalated, fraud check, policy lapsed, $60,000.")
    return r.text.strip()


def speakable(text: str) -> str:
    text = re.sub(r"[*#`_|>]", " ", text).replace("->", " to ").replace("→", " to ")
    return re.sub(r"\s+", " ", text).strip()


@traceable(name="text_to_speech", run_type="tool", tags=["voice", "tts"],
           process_outputs=lambda o: {"mp3_bytes": len(o) if isinstance(o, bytes) else 0})
def speak(text: str) -> bytes:
    buf = io.BytesIO()
    gTTS(speakable(text), lang="en").write_to_fp(buf)
    return buf.getvalue()


@traceable(name="voice_turn", tags=["voice-agent"],
           process_inputs=lambda i: {"text": i.get("text"), "audio_bytes": len(i.get("audio") or b""),
                                     "thread_id": i.get("thread_id")},
           process_outputs=lambda o: {k: v for k, v in o.items() if k != "reply_audio"})
def voice_turn(agent, thread_id: str, audio: bytes | None = None, text: str | None = None) -> dict:
    """One conversational turn: (speech ->) text -> agent with tools -> spoken reply."""
    heard = transcribe(audio) if audio else text
    result = agent.invoke({"messages": [{"role": "user", "content": heard}]},
                          config={"configurable": {"thread_id": thread_id}})
    msgs = result["messages"]
    last_user = max(i for i, m in enumerate(msgs) if m.type == "human")
    tool_calls = [{"tool": tc["name"], "args": tc["args"]} for m in msgs[last_user:] if m.type == "ai"
                  for tc in (m.tool_calls or [])]
    reply = msgs[-1].content
    return {"heard": heard, "reply": reply, "tool_calls": tool_calls, "reply_audio": speak(reply)}
