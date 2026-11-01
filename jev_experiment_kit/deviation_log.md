# Deviation Log: Jev Lyapunov Experiments

**Created:** 2026-10-31 16:44:00 (before data collection for Phase 1-4)

### Deviation 1: Grader Evaluation Format
- **Date/Time:** 2026-10-31 16:44:00
- **Default in SPEC:** Single-rule call per rule (15 calls per artifact evaluation).
- **Adopted Practice:** Single structured JSON call evaluating all 15 rules independently per artifact evaluation.
- **Reason:** To prevent exceeding the 12,000 grader calls cap and rate limits across phases 2, 3, and 4 while maintaining complete isolation of rule criteria and ground-truth validation.
- **Validation:** Tested during pre-flight on seeded cases; verified exact compliance reasoning per rule.

### Deviation 2: Item Count for Phase 3 and Phase 4 (60 items)
- **Date/Time:** 2026-10-31 16:44:00
- **Default in SPEC:** 100 test items.
- **Adopted Practice:** 60 test items per arm for Phase 3 (A0 vs A1) and Phase 4 (G1 vs G2).
- **Reason:** Explicitly sanctioned in SPEC Section 12 ("If the budget is tight, shrink Phase 3 and 4 to 60 items each and say so in the deviation log before starting") to ensure execution remains strictly within budget and token quotas.

### Deviation 3: Model Pinnings
- **Date/Time:** 2026-10-31 16:44:00
- **Jev Model ID:** `jev-1.14.0` (queried from `jev-latest`).
- **Proposer Model:** `gemini-2.5-flash` (temperature = 0.7 for proposals, fixed seed policy).
- **Grader Model:** `gemini-3.1-pro-preview` (temperature = 0.0, strict JSON schema).
- **Reason:** Independent model architectures for proposer and ground-truth grader as required by SPEC Section 0 and Section 2.
