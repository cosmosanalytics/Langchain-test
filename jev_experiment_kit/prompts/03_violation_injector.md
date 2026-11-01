# Prompt: inject exactly one violation (proposer model)

Below is a support reply that follows the policy. Make the smallest edit to the reply that makes it violate EXACTLY ONE rule, {RULE_ID} ({RULE_NAME}), and no other rule. Keep the tone and length. Do not mention that you made an edit.

<policy>
{POLICY_BOOK}
</policy>

<rule>
{RULE_ID}: {RULE_DESCRIPTION}
</rule>

<reply>
{REPLY}
</reply>

Return only the edited reply.

Runner notes (not part of the prompt):
- For multi-violation variants, apply this prompt once per rule in sequence.
- After each injection, call the grader (04_grader.md) on all 15 rules. Keep the variant only if the grader marks exactly the intended rules violated. Otherwise regenerate (at most 3 tries) and log the failure.
- If the situation makes the rule non-triggerable (for example R04 when the item is not final sale), choose a different rule.
