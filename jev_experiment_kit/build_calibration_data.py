import json
import os
import time
import random
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
rule_dict = {r['id']: r for r in rules}

with open('C:/Users/richa/ai-engineering/jev_experiment_kit/kit/queries.json', 'r', encoding='utf-8') as f:
    all_queries = json.load(f)

cal_queries = all_queries[:120]

def generate_compliant_reply(query):
    prompt = f"""You are a Northwind Outfitters support agent. Write a reply to the customer message that follows EVERY rule in the policy below. Keep it under 150 words. Be friendly, accurate and concise. Always end with one clear next step for the customer.

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
        config=types.GenerateContentConfig(temperature=0.2)
    )
    return resp.text.strip()

def inject_rule_violation(reply, rule_id):
    r = rule_dict[rule_id]
    prompt = f"""Below is a support reply that follows the policy. Make the smallest edit to the reply that makes it violate EXACTLY ONE rule: {rule_id} ({r['name']}).
Rule description: {r['main_question']}
Ensure you keep the tone and length under 150 words. Do not mention that an edit was made.

<policy>
{policy_book}
</policy>

<reply>
{reply}
</reply>

Return only the edited reply."""
    resp = client.models.generate_content(
        model=PROPOSER_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.3)
    )
    return resp.text.strip()

def grade_reply(query, reply):
    prompt = f"""You check a support reply against the 15 policy rules.
For each rule, decide if the reply COMPLIES with the rule (true) or VIOLATES it (false).
Note: A rule not triggered by the situation is compliant (true).

<policy>
{policy_book}
</policy>

<customer_message>
{query['message']}
</customer_message>

<situation_facts>
{json.dumps(query['situation'])}
</situation_facts>

<reply>
{reply}
</reply>

Respond with JSON only, an object mapping each rule ID (R01 to R15) to a boolean:
{{"R01": true, "R02": false, ...}}
"""
    resp = client.models.generate_content(
        model=GRADER_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.0
        )
    )
    try:
        grades = json.loads(resp.text)
        return {r_id: bool(grades.get(r_id, True)) for r_id in rule_dict}
    except Exception as e:
        print("Grader parse error:", e)
        return {r_id: True for r_id in rule_dict}

out_file = 'C:/Users/richa/ai-engineering/jev_experiment_kit/kit/calibration_artifacts.json'
if os.path.exists(out_file):
    print("Calibration artifacts already exist at", out_file)
    with open(out_file, 'r', encoding='utf-8') as f:
        artifacts = json.load(f)
else:
    artifacts = []
    print(f"Generating 120 calibration artifacts...")
    for idx, q in enumerate(cal_queries):
        reply = generate_compliant_reply(q)
        injected = []
        
        # Invert/inject violations in items 60-119
        if idx >= 60:
            target_r = f"R{(idx % 15) + 1:02d}"
            reply = inject_rule_violation(reply, target_r)
            injected.append(target_r)
            if idx % 2 == 0:
                second_r = f"R{((idx + 5) % 15) + 1:02d}"
                reply = inject_rule_violation(reply, second_r)
                injected.append(second_r)
                
        # Get ground truth from grader
        s_dict = grade_reply(q, reply)
        # Ensure injected rules are recorded as violated
        for r_id in injected:
            s_dict[r_id] = False
            
        artifacts.append({
            "artifact_id": f"CAL_{q['query_id']}",
            "query_id": q["query_id"],
            "message": q["message"],
            "situation": q["situation"],
            "reply": reply,
            "injected_violations": injected,
            "s_true": s_dict
        })
        
        if (idx + 1) % 15 == 0:
            print(f"Generated {idx + 1}/120 calibration artifacts...")
            time.sleep(1)

    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(artifacts, f, indent=2)
    print(f"Saved {len(artifacts)} artifacts to {out_file}")
