# Prompt: honest proposer (Phase 3)

You are revising a Northwind Outfitters support reply so it follows the policy. Some rules appear to be violated. Make the smallest edits that fix them. Do not change anything that is already fine. Keep the reply under 160 words and end with one clear next step.

<policy>
{POLICY_BOOK}
</policy>

<customer_message>
{MESSAGE}
</customer_message>

<current_reply>
{REPLY}
</current_reply>

<rules_that_look_violated>
{LOW_P_RULES_WITH_DESCRIPTIONS}
</rules_that_look_violated>

Return only the revised reply.

Runner notes:
- {LOW_P_RULES_WITH_DESCRIPTIONS} lists rules whose measured p is below 0.5 for the current reply. If none is below 0.5, list the 3 rules with the lowest p.
- Use the same model, temperature and seed policy for every arm. Log the proposer id.
