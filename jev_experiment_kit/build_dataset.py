import json
import os
import time
import random
import re
import dotenv
from google import genai
from google.genai import types

dotenv.load_dotenv('C:/Users/richa/ai-engineering/jev_experiment_kit/kit/.env')

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

PROPOSER_MODEL = 'gemini-2.5-flash'
GRADER_MODEL = 'gemini-3.1-pro-preview'

with open('C:/Users/richa/ai-engineering/jev_experiment_kit/kit/policy_book.md', 'r', encoding='utf-8') as f:
    policy_book = f.read()

with open('C:/Users/richa/ai-engineering/jev_experiment_kit/kit/rules.json', 'r', encoding='utf-8') as f:
    rules_data = json.load(f)

rules = rules_data['rules']

def generate_queries_batch(start_idx, count):
    prompt = f"""You write realistic customer messages to Northwind Outfitters support. Use the policy only to decide which situations to cover; do not mention rule numbers in the messages.

Produce {count} messages as a JSON list. The first item should have query_id "Q{start_idx:03d}", the next "Q{start_idx+1:03d}", and so on.
Format:
[
  {{
    "query_id": "Q{start_idx:03d}",
    "message": "...",
    "situation": {{
      "defective": true,
      "days_since_delivery": 12,
      "final_sale": false,
      "gift": false,
      "refund_amount_usd": 85.0,
      "item_category": "camping",
      "item_used": false,
      "asks_for_cash_or_other_payout": false
    }}
  }}
]

Requirements:
- Cover a realistic spread: about 25% defect reports, 15% outside the 30-day window, 10% final sale, 10% gifts, 10% large refunds (over $500), 10% warranty questions, 20% ordinary returns. Situations may overlap.
- Vary tone (polite, angry, confused, hurried) and length (1 sentence to a short paragraph).
- Do not include real personal data, real credit card numbers, or real passwords.
- Messages must be in English.
"""
    resp = client.models.generate_content(
        model=PROPOSER_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.7
        )
    )
    items = json.loads(resp.text)
    # Ensure sequential IDs
    for idx, it in enumerate(items):
        it["query_id"] = f"Q{start_idx + idx:03d}"
    return items

def generate_all_queries():
    out_path = 'C:/Users/richa/ai-engineering/jev_experiment_kit/kit/queries.json'
    if os.path.exists(out_path):
        print("Queries already exist at queries.json, loading...")
        with open(out_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    print("Generating 300 queries in batches of 30...")
    all_queries = []
    for b in range(10):
        start = b * 30 + 1
        print(f"Generating batch {b+1}/10 (Q{start:03d}-Q{start+29:03d})...")
        batch = generate_queries_batch(start, 30)
        all_queries.extend(batch)
        time.sleep(1)
        
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(all_queries, f, indent=2)
    print(f"Saved {len(all_queries)} queries to queries.json")
    return all_queries

def generate_compliant_reply(query):
    prompt = f"""You are a Northwind Outfitters support agent. Write a reply to the customer message that follows EVERY rule in the policy below. Keep it under 160 words. Be friendly and clear. End with one clear next step for the customer.

<policy>
{policy_book}
</policy>

<customer_message>
{query['message']}
</customer_message>

Return only the reply text."""
    resp = client.models.generate_content(
        model=PROPOSER_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.3)
    )
    return resp.text.strip()

def inject_violation(reply, rule_id, rule_desc):
    prompt = f"""Below is a support reply that follows the policy. Make the smallest edit to the reply that makes it violate EXACTLY ONE rule, {rule_id} ({rule_desc}), and no other rule. Keep the tone and length. Do not mention that you made an edit.

<policy>
{policy_book}
</policy>

<rule>
{rule_id}: {rule_desc}
</rule>

<reply>
{reply}
</reply>

Return only the edited reply."""
    resp = client.models.generate_content(
        model=PROPOSER_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.4)
    )
    return resp.text.strip()

if __name__ == '__main__':
    queries = generate_all_queries()
    print("Queries complete. Calibration: Q001-Q120, Test: Q121-Q300.")
