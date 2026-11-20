"""Streamlit app: Voice Claims Agent with Model-Based Evaluation.  Run: streamlit run app.py"""
import hashlib
import hmac
import os
import uuid

import pandas as pd
import streamlit as st
from langsmith import Client

import agent as va
import core

st.set_page_config(page_title="Voice Claims Agent", layout="wide")

APP_PASSWORD = os.getenv("APP_PASSWORD")
if APP_PASSWORD and not st.session_state.get("authed"):
    st.title("Voice Claims Agent with Model-Based Evaluation")
    pw = st.text_input("Password", type="password")
    if pw and hmac.compare_digest(pw.encode(), APP_PASSWORD.encode()):
        st.session_state["authed"] = True
        st.rerun()
    elif pw:
        st.error("Wrong password")
    st.stop()

PROJECT = os.getenv("LANGSMITH_PROJECT", "voice-agent")
TRACING = os.getenv("LANGSMITH_TRACING", "").lower() == "true" and bool(os.getenv("LANGSMITH_API_KEY"))
EXAMPLES = ["Which claims do I have?", "What should happen with Ivy's claim?",
            "Why can a claim be escalated?", "Move Grace's claim to approved."]


@st.cache_resource
def ls_client():
    return Client() if TRACING else None


def reset():
    st.session_state.update(db=va.new_claims_db(), evals=[], chat=[], thread=str(uuid.uuid4()), last_audio=None)
    st.session_state.agent = va.build_voice_agent(st.session_state.db, core.load_world_model(),
                                                  st.session_state.evals)


if "agent" not in st.session_state:
    reset()
S = st.session_state


def run_turn(audio: bytes | None = None, text: str | None = None):
    run_id, n_evals = uuid.uuid4(), len(S.evals)
    with st.spinner("Listening and thinking..."):
        out = va.voice_turn(S.agent, S.thread, audio=audio, text=text,
                            langsmith_extra={"run_id": run_id, "project_name": PROJECT,
                                             "metadata": {"thread_id": S.thread}})
    new_evals = S.evals[n_evals:]
    url = None
    if TRACING:
        c = ls_client()
        for e in new_evals:
            for s in e["scores"]:
                c.create_feedback(run_id, key=s["key"], score=s["score"], comment=s["comment"])
        try:
            c.flush()
            url = c.read_run(run_id).url
        except Exception:
            pass
    S.chat.append({"role": "user", "content": out["heard"], "voice": audio is not None})
    S.chat.append({"role": "assistant", "content": out["reply"], "audio": out["reply_audio"],
                   "tools": out["tool_calls"], "evals": new_evals, "trace": url})


# ---------------- sidebar ----------------
with st.sidebar:
    st.subheader("Stack")
    st.markdown(f"- **Speech to text:** Groq `{va.STT_MODEL}`\n- **Agent:** LangChain `create_agent` "
                f"(LangGraph loop + memory), `{core.MODEL}`\n- **Text to speech:** gTTS\n"
                f"- **Scoring:** world-model judge, plus ground truth when present\n"
                f"- **Tracing:** {'LangSmith, project `' + PROJECT + '`' if TRACING else 'off (set LANGSMITH_TRACING)'}")
    st.subheader("Claims (live)")
    st.dataframe(pd.DataFrame([{"id": c["id"], "customer": c["customer"], "state": c["current_state"],
                                "ground truth": c["ground_truth"] or "none"} for c in S.db.values()]),
                 hide_index=True, use_container_width=True)
    if st.button("Reset conversation and claims"):
        reset()
        st.rerun()
    st.caption("[Request changes](https://app.devin.ai/sessions/3c2a71bed27641c98da4db72bae3ab93)")

# ---------------- main ----------------
st.title("Voice Claims Agent with Model-Based Evaluation")
st.caption("Talk to a claims agent. It looks up claims, recommends next steps with a world-model score, "
           "and moves claims only along world-model transitions. Replies are spoken back.")

c1, c2 = st.columns([2, 3])
with c1:
    audio = st.audio_input("Press the mic and speak")
    if audio is not None:
        data = audio.getvalue()
        digest = hashlib.sha256(data).hexdigest()
        if digest != S.last_audio:
            S.last_audio = digest
            run_turn(audio=data)
with c2:
    st.write("Or try:")
    cols = st.columns(2)
    for i, ex in enumerate(EXAMPLES):
        if cols[i % 2].button(ex, use_container_width=True):
            run_turn(text=ex)

typed = st.chat_input("...or type a message")
if typed:
    run_turn(text=typed)

last = len(S.chat) - 1
for i, m in enumerate(reversed(S.chat)):
    idx = last - i
    with st.chat_message(m["role"]):
        st.markdown(("🎙️ " if m.get("voice") else "") + m["content"].replace("$", "\\$"))
        if m["role"] == "assistant":
            st.audio(m["audio"], format="audio/mp3", autoplay=idx == last)
            if m["tools"]:
                st.caption("Tools: " + " → ".join(f"{t['tool']}({', '.join(f'{k}={v}' for k, v in t['args'].items())})"
                                                  for t in m["tools"]))
            for e in m["evals"]:
                d = e["decision"]
                score = next(s["score"] for s in e["scores"] if s["key"] == "wm_score")
                with st.expander(f"Evaluation of {e['claim']}: {d['current_state']} → {d['next_state']}, "
                                 f"wm_score = {score}", expanded=score < 1):
                    st.dataframe(pd.DataFrame([{"check": s["key"], "score": s["score"], "reason": s["comment"]}
                                               for s in e["scores"]]), hide_index=True, use_container_width=True)
            if m.get("trace"):
                st.caption(f"[Open trace in LangSmith]({m['trace']})")
