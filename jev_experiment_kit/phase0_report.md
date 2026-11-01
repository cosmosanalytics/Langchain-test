# Phase 0 Smoke Test Report

**Execution Date:** 2026-10-31 16:43:40
**Pinned Jev Model:** `jev-1.14.0` (from `jev-latest`)

## Summary of Checks

| Check # | Requirement | Status | Observed Values / Notes |
|---|---|---|---|
| 1 | Auth & model listing | **PASS** | Successfully listed models: ['jev-latest', 'jev-preview']. Model pinned to `jev-1.14.0`. |
| 2 | All 15 Noul questions in one call, $p_i \in [0, 1]$ | **PASS** | Exactly 15 answers returned per call. All probabilities bounded in [0.0, 1.0]. |
| 3 | Repeatability (same input twice) | **PASS** | $\Delta V = 0.001334$, $\max |\Delta p_i| = 0.050000$. Responses are highly consistent. |
| 4 | State limits, latency & token usage | **PASS** | Mean latency: 0.13s per call (15 questions). Mean input tokens: 1478, mean output tokens: 274. |
| 5 | Obvious cases behave sensibly | **PASS** | Fully compliant artifact $V = 0.1094$. Violations systematically trigger drops in targeted $p_i$. |
| 6 | Question order invariance | **PASS** | Shuffled vs unshuffled $\Delta V = 0.000001$. |

## Detailed Artifact Evaluations

| Artifact ID | Target Violation | Target $p_i$ | Total $V$ | Detection ($p_i < 0.5$) |
|---|---|---|---|---|
| `A01_compliant` | `None (Compliant)` | N/A | 0.1094 | N/A |
| `A02_violate_R01` | `R01` | 0.01 | 0.2014 | YES |
| `A03_violate_R02` | `R02` | 0.03 | 0.1567 | YES |
| `A04_violate_R03` | `R03` | 0.02 | 0.2141 | YES |
| `A05_violate_R04` | `R04` | 0.02 | 0.2508 | YES |
| `A06_violate_R05` | `R05` | 0.01 | 0.2661 | YES |
| `A07_violate_R06` | `R06` | 0.02 | 0.3195 | YES |
| `A08_violate_R07` | `R07` | 0.02 | 0.2314 | YES |
| `A09_violate_R09` | `R09` | 0.01 | 0.2761 | YES |
| `A10_violate_R15` | `R15` | 0.20 | 0.1693 | YES |

## Key Conclusions
- Jev API responds rapidly (~0.13s) to evaluate all 15 rules concurrently in a single request.
- Pinned Model ID: `jev-1.14.0`.
- Decision: **PROCEED TO DATA GENERATION & PHASE 1.**
