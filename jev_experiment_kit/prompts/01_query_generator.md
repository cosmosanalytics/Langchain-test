# Prompt: generate customer queries

You write realistic customer messages to Northwind Outfitters support. Use the policy only to decide which situations to cover; do not mention rule numbers in the messages.

Produce {N} messages as a JSON list. Each item:
```
{"query_id": "Q001", "message": "...", "situation": {
   "defective": true|false, "days_since_delivery": int,
   "final_sale": true|false, "gift": true|false,
   "refund_amount_usd": number, "item_category": "electronics|apparel|footwear|camping|other",
   "item_used": true|false, "asks_for_cash_or_other_payout": true|false}}
```

Requirements:
- Cover a spread: about 25% defect reports, 15% outside the 30-day window, 10% final sale, 10% gifts, 10% large refunds (over 500 dollars), 10% warranty questions, 20% ordinary returns. Situations may overlap.
- Vary tone (polite, angry, confused) and length (one line to a short paragraph).
- Do not include real personal data, card numbers, or passwords.
- Messages must be in English.
