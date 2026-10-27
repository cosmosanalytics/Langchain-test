# -*- coding: utf-8 -*-
"""
Publishes a LinkedIn post summarizing the 4 LangChain & Agent Studio apps
with the GitHub repository and live web demo links.
"""
import sys
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

POST_TEXT = """Excited to open-source 4 standalone, client-side web apps for building, tracing, and continuously improving AI agents! 🦜✨

Every app runs 100% in your browser (zero backend required) powered by Groq LPU (500+ tok/s) and local WebGPU (WebLLM):

1. 🕵️ StoryMine — Web UX Story Miner
Scrapes any website or forum (via CORS-friendly Jina Reader) and extracts structured user experience stories, friction points, "Aha!" moments, and sentiment scores into visual Bento cards.

2. 🛠️ GraphSmith — LangGraph & Claude 3.5 Studio
Generates production-grade LangGraph StateGraph architectures from plain natural language. Features interactive Mermaid diagrams, typed state schemas, and an in-browser step-by-step simulator.

3. 🔍 LangSmith Studio — LLM Observability & Tracing
Reproduces the iconic LangSmith developer platform client-side: hierarchical execution trace trees, Gantt waterfall latency charts, LLM-as-a-judge dataset evaluations, and prompt playground.

4. 🔄 LangFlywheel — Continuous Agent Optimizer
Demonstrates the trace-driven improvement flywheel: captures execution traces, diagnoses failure modes (e.g. unescaped SQL quotes), and auto-evolves agent code (v1 ➔ v2 ➔ v3) until reaching 100% Pass@1.

📂 GitHub Repository (Code & Standalone HTMLs):
https://github.com/cosmosanalytics/Langchain-test

🌐 Live Interactive Web Hub:
https://cosmosanalytics.github.io/Langchain-test/

#LangChain #LangGraph #AIAgents #Claude #Groq #WebGPU #OpenSource #LLMObservability #SoftwareEngineering"""

payload = {
    "author": MEMBER_URN,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": POST_TEXT
            },
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

print("Publishing post to LinkedIn...")
response = requests.post(URL, headers=HEADERS, json=payload)
print(f"Status Code: {response.status_code}")
if response.status_code == 201:
    post_id = response.json().get('id')
    print(f"Success! Post published with URN: {post_id}")
    print(f"Direct Post Link: https://www.linkedin.com/feed/update/{post_id}/")
else:
    print(f"Error publishing post: {response.text}")
