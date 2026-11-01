# Prompt: ground-truth grader (grader model, NOT Jev, never shown Jev outputs)

You check one support reply against one policy rule. Decide whether the reply COMPLIES with the rule. A rule that is not triggered by the customer's situation is satisfied.

<policy>
{POLICY_BOOK}
</policy>

<customer_message>
{MESSAGE}
</customer_message>

<situation_facts>
{SITUATION_JSON}
</situation_facts>

<reply>
{REPLY}
</reply>

<rule>
{RULE_ID}: {RULE_DESCRIPTION}
</rule>

Answer with JSON only:
{"rule_id": "{RULE_ID}", "compliant": true|false, "evidence": "<short quote or reason>"}

Runner notes:
- Run each rule as a separate call so rules do not influence each other.
- Validate this grader on the seeded labels (artifacts with injected violations) and report its accuracy, per rule. If overall accuracy is below 90%, stop and report.
- For R09 and R11 also compute the regex in rules.json (programmatic_hint) and log any disagreement with the grader.
