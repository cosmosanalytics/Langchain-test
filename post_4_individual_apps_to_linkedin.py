# -*- coding: utf-8 -*-
"""
Publishes 4 separate LinkedIn posts, one for each application in the
LangChain & Agent Studio suite, with direct links and GitHub URLs.
"""
import sys
import time
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

TOKEN = 'AQUMlZr1hCCbt6otNDSlGTIQ9_0NImaIEx44nzuKW0cHLaRzNZ5fkcaT-wn-ss73mcLXwmAg6Xja4aT2izHOrm2Vl6NVBUDh9nBlRf_e2DaC87qyaZ2-0a0UDdQq-5LAseuE80LCE6XZ_iQ760Yt94FtORfAPh_f-bwvOx33OD0RzVIsTerHFTWUCVvbtZjPxw565cXQglfXyVpawUu8GhCI3tayZq56oU_badUpMAkq7mM8bqCmVu5eADt-qoXEvzelQ6vsDFlTqeOEzWwFkWdpd3QmnFYWDcJHqkFmm5hLSnfIiSnUsb6hmiPkqMzKUbyIZ4_oNpOOEScJfY0Tmjg1lH55AA'
MEMBER_URN = 'urn:li:person:muZwZNN9P9'
URL = "https://api.linkedin.com/v2/ugcPosts"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
}

POSTS = [
    {
        "title": "App 1: StoryMine 🕵️✨ — Web UX Story Miner",
        "text": """How do you instantly turn raw web feedback into actionable product design stories? 🕵️✨

I built StoryMine — a 100% client-side web application that scrapes any live website or review thread and extracts structured User Experience (UX) stories using Groq LPU & in-browser WebGPU:

• 🌐 Smart Scraping: Uses CORS-friendly Jina Reader to strip boilerplate, ads, and navigation from any URL into clean text.
• 👤 Persona Extraction: Automatically maps target user roles, core needs, friction points, and "Aha!" breakthrough moments.
• 📊 Visual Bento Cards: Generates sentiment scores (1–100), emotion meters (🤩 Delight vs 😫 Friction), and first-person soundbites.
• 🛠️ Actionable UX Recommendations: Translates user complaints into concrete product improvements.
• ⚡ Dual Engine: Switch between Groq LPU (500+ tok/s) and local WebGPU (100% private, zero data leaves your device).

👉 Try it live in your browser:
https://cosmosanalytics.github.io/Langchain-test/ux_story_miner.html

📂 GitHub Repository (Open Source):
https://github.com/cosmosanalytics/Langchain-test

#UXResearch #ProductDesign #AIAgents #WebGPU #Groq #OpenSource #SoftwareEngineering"""
    },
    {
        "title": "App 2: GraphSmith 🛠️🦜 — LangGraph & Claude 3.5 Studio",
        "text": """Turn natural language ideas into production-ready LangGraph state machines in seconds! 🛠️🦜

I built GraphSmith — an interactive studio for designing, visualizing, and simulating LangChain & LangGraph agents powered by Anthropic Claude 3.5 Sonnet:

• 💬 Prompt to StateGraph: Describe your workflow (e.g. Self-Reflective RAG, Human-in-the-Loop Approval, Multi-Agent Supervisor), and it generates idiomatic Python code.
• 📊 Live Mermaid Canvas: Renders an interactive state machine diagram with color-coded Agent nodes, ToolNode harnesses, and conditional routing edges.
• 🐍 Complete Python Code: Produces typed state schemas (class AgentState(TypedDict)), message reducers, tool bindings, and MemorySaver checkpointers with 1-click copy/download.
• 🧪 In-Browser Simulator: Step through the execution graph node-by-node right in the browser while inspecting live memory dictionary snapshots.

👉 Try it live in your browser:
https://cosmosanalytics.github.io/Langchain-test/langgraph_agent_studio.html

📂 GitHub Repository:
https://github.com/cosmosanalytics/Langchain-test

#LangChain #LangGraph #Claude #Anthropic #AIAgents #Groq #WebGPU #OpenSource"""
    },
    {
        "title": "App 3: LangSmith Studio 🔍 — LLM Observability & Tracing",
        "text": """What does your agent actually do inside its execution loop? 🔍🦜

I built LangSmith Studio — a zero-backend, client-side reproduction of the iconic LangSmith developer platform for autonomous LLM agents:

• 📈 Hierarchical Trace Trees: Inspect the full execution hierarchy from root StateGraph chains down to ChatAnthropic completions and ToolNode spans.
• ⏱️ Gantt Waterfall: Visual duration bars comparing child span latency and pinpointing execution bottlenecks.
• 🧪 Dataset Evaluations (LLM-as-a-Judge): Run automated benchmark suites evaluating contract invariants, pass rate %, and zero silent failures.
• 🛝 Prompt Playground: Test system prompts with live streaming output that automatically commits executed runs into the active trace log.
• ⚡ 100% Client-Side: Runs entirely in your browser using Groq LPU or local WebGPU!

👉 Try it live in your browser:
https://cosmosanalytics.github.io/Langchain-test/langsmith_studio.html

📂 GitHub Repository:
https://github.com/cosmosanalytics/Langchain-test

#LangSmith #LLMObservability #LangChain #MLOps #AIEngineering #Groq #OpenSource"""
    },
    {
        "title": "App 4: LangFlywheel 🔄 — Continuous Agent Improvement Loop",
        "text": """Can an AI agent use its own execution traces to fix its own code and architecture? 🔄🦜

I built LangFlywheel — an interactive demonstration of the Flywheel of Continuous Agent Optimization:

• 🏃 Stage 1 (Run & Trace): Executes baseline agents against workloads and captures full LangChain execution traces.
• 🔍 Stage 2 (Trace Diagnostic): Automatically parses execution logs to isolate failure modes (e.g. unescaped SQL quotes, loop timeouts, unconstrained markdown output).
• 🧬 Stage 3 (Auto-Evolve Architecture): Synthesizes upgraded LangGraph Python code (v1 ➔ v2 ➔ v3) adding input sanitizers, tool schemas, and read-only proctor sandboxes.
• 📊 Stage 4 (Verify & Lift): Measures quantitative benchmark gains:
  - Pass@1 Accuracy: 42% (v1) ➔ 81% (v2) ➔ 100% (v3)
  - Latency: 1,240 ms ➔ 620 ms ➔ 310 ms (75% faster)
  - Cost: 78% reduction ($0.0018 ➔ $0.0004)
  - Silent Failures: 3 ➔ 1 ➔ 0

👉 Try it live in your browser:
https://cosmosanalytics.github.io/Langchain-test/continuous_agent_optimizer.html

📂 GitHub Repository:
https://github.com/cosmosanalytics/Langchain-test

#AIAgents #SelfHealingCode #LangChain #LangGraph #EvalDrivenDevelopment #WebGPU #Groq"""
    }
]

published_results = []

for i, post in enumerate(POSTS):
    print(f"\n[{i+1}/4] Publishing: {post['title']}...")
    payload = {
        "author": MEMBER_URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post["text"]
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    resp = requests.post(URL, headers=HEADERS, json=payload)
    if resp.status_code == 201:
        post_urn = resp.json().get('id')
        post_url = f"https://www.linkedin.com/feed/update/{post_urn}/"
        print(f"  ✅ Published! URN: {post_urn}")
        print(f"  🔗 URL: {post_url}")
        published_results.append({
            "title": post["title"],
            "urn": post_urn,
            "url": post_url
        })
    else:
        print(f"  ❌ Error: {resp.status_code} - {resp.text}")

    # Brief pause between posts
    if i < len(POSTS) - 1:
        time.sleep(2)

print("\n=== SUMMARY OF PUBLISHED POSTS ===")
for res in published_results:
    print(f"• {res['title']}: {res['url']}")
