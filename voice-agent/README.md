# Voice Claims Agent with Model-Based Evaluation

A voice version of [`explainable-agent/`](../explainable-agent): talk to a claims agent, hear the answer, and see
every recommendation scored against the world model.

```
mic ──► Groq Whisper (speech to text) ──► LangChain create_agent (LangGraph tool loop + memory) ──► gTTS (speech) ──► speaker
                                                   │
             tools: list_claims · get_claim · explain_rules · move_claim · recommend_next_state
                                                                                   │
                                     explainable agent (core.run_agent) ──► world-model judge (core.judge)
                                                                          world model + ground truth when present
```

- **Speech to text:** Groq `whisper-large-v3-turbo` (same `GROQ_API_KEY`).
- **Agent:** `create_agent` builds a LangGraph agent loop; `InMemorySaver` keeps the conversation, so
  "move **it** to escalated" knows which claim you mean.
- **Guardrail:** `move_claim` only allows transitions that exist in the world model.
- **Model-based evaluation:** `recommend_next_state` runs the unchanged explainable agent and scores it with the
  world-model judge (ground truth is used when the claim has one; otherwise the world model alone).
- **Text to speech:** gTTS (free, no key).
- **Tracing:** each turn is one `voice_turn` trace in LangSmith (`speech_to_text` → agent → tools → `text_to_speech`),
  with the evaluation scores attached as feedback.

## Run

```bash
cd voice-agent
pip install -r requirements.txt
cp .env.example .env   # add GROQ_API_KEY and LANGSMITH_API_KEY
streamlit run app.py
```

Try saying: "Which claims do I have?", "What should happen with Ivy's claim?", "Move it to escalated."

## Share it on Streamlit Community Cloud

share.streamlit.io → Create app → repo `cosmosanalytics/Langchain-test`, main file `voice-agent/app.py`.
Paste the `.env.example` keys as TOML into Advanced settings → Secrets and set `APP_PASSWORD`.
The mic needs HTTPS, which Streamlit Cloud provides.
