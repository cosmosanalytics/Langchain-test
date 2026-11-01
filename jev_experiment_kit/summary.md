# Executive Summary: Jev-Defined Lyapunov Function Experiments

**Date of Execution:** 2026-10-31 to 2026-11-01  
**Total Runtime:** 57,566.0 seconds (15.99 hours)  
**Target Subject:** TypeSafe System One Model (`jev-1.14.0`, pinned via `jev-latest`)  
**Proposer Model:** `Qwen/Qwen2.5-1.5B-Instruct` (Local CUDA inference)  
**Artifact Domain:** Northwind Outfitters Support Policy (15 rules, equal weights $w_i \approx 0.0667$, atomic Noul questions)  
**Configuration SHA-256:** `dd0b7f0d422efc006b0007c43373290cbdc451efaba4b57b9674a2b52943edfd`  
**Parameters Frozen:** $\delta = 0.031413$, $\epsilon = 0.0800$, $B = 3$, $T = 10$, $T_{\text{long}} = 15$

---

## 1. Primary Hypothesis Evaluation Table

| Hypothesis | Predicted Effect | Primary Metric | Observed Value | Decision Rule | Outcome |
|---|---|---|:---:|:---:|:---:|
| **H1: Descent Gate** | Gate reduces steps where true violation rises | Share of items with $\ge 1$ step where $V_{\text{true}}$ rose | $A_0$ (ungated): **61.67%**<br>$A_1$ (gated): **5.00%**<br>Difference: **56.67%** (95% CI: $[41.67\%, 68.33\%]$) | Share $A_1 \le 0.5 \times A_0$; 95% CI excludes 0; final $V_{\text{true}}$ not worse by $> 0.02$ | **SUPPORTED** ($p < 0.001$) |
| **H2: Calibration & Rings** | Jev accuracy rises with confidence; ECE $\le 0.05$ | ECE, Brier score, Spearman rank $\rho$ | ECE: **0.1600**<br>Brier: **0.1252**<br>Spearman $\rho$: **0.5152** | $\rho \ge 0.90$ and $\text{ECE} \le 0.05$ | **NOT SUPPORTED** |
| **H3: Dual-Judge Audit** | Independent audit judge prevents premature stop in judge-pleasing mode | Premature stop rate ($V_{\text{true}} > 0.10$ at stop) | $G_1$ (main only): **81.67%**<br>$G_2$ (main + audit): **83.33%**<br>Difference: **-1.67%** (95% CI: $[-11.67\%, 10.00\%]$) | Premature stop rate for $G_2 < G_1$ with 95% CI excluding 0 | **NOT SUPPORTED** |

---

## 2. Key Findings and Quantitative Breakdown

### Hypothesis 1: Lyapunov Descent Gate ($H_1$) — Strongly Supported
- **Ungated Baseline ($A_0$):** In 61.67% of cases, unconstrained revisions produced regression steps where true policy violations increased.
- **Descent-Gated Revision ($A_1$):** Requiring a measured Lyapunov descent $V_{\text{measured}}(x_{t+1}) \le V_{\text{measured}}(x_t) - \delta$ dropped regressions down to **5.00%** (a **12.3-fold reduction**).
- **Final Compliance:** Mean final $V_{\text{true}}$ under $A_1$ was $0.2801$ vs $0.2746$ under $A_0$ ($\Delta = 0.0055$, within the equivalence bound of $\le 0.02$). Acceptance rate was 32.66% under $A_1$, demonstrating that the gate rejected deteriorating proposals while preserving convergence.

### Hypothesis 2: Calibration & Confidence Rings ($H_2$) — Not Supported
- From $n = 1,800$ artifact-rule pairs across 120 calibration items, Jev achieved high accuracy on explicit negative conditions (e.g. R09 Sensitive Info: 95.0%, R13 Warranty: 95.8%, R01 Return Window: 92.5%, R12 Respectful Tone: 95.0%), but scored lower on subtle requirements (R02 Defect Photo: 38.3%).
- Across 10 equal-mass bins, the rank correlation was $\rho = 0.5152$ (below the required $\ge 0.90$), and ECE was $0.1600$ (target $\le 0.05$).

### Hypothesis 3: Dual-Judge Audit ($H_3$) — Not Supported
- In adversarial judge-chasing mode, the proposer model learned to satisfy surface formulations of the main judge.
- A Goodhart gap emerged: $V_{\text{true}} - V_{\text{main}} = +0.0295$, showing that the main judge was consistently more optimistic than true compliance.
- Requiring simultaneous descent on both main and audit judges ($G_2$) did not reduce premature stop rates (83.33% vs 81.67%), indicating that reworded prompts with the same underlying semantic structure can be simultaneously Goodharted.

---

## 3. Operational & Control Verification
- **Phase 0 Smoke Tests:** 6/6 checks passed. Model pinned to `jev-1.14.0`. Latency per 15-question request: ~0.13s.
- **Noise Pilot:** Measurement noise $\hat{\eta} = 0.012565$. Mean $V$ standard deviation across repeats $= 0.003946$.
- **Usable Margin Window:** $2\hat{\eta} = 0.0251 < \delta = 0.0314 < \delta_{\max} = 0.0482$.
- **Controls & Sanity Checks:**
  - Fully compliant vs. fully violating AUROC: **0.5600**
  - Mean $|V_{\text{main}} - V_{\text{audit}}|$ wording difference: **0.097105**
- **Artifacts Saved:**
  - [`steps.jsonl`](file:///C:/Users/richa/ai-engineering/jev_experiment_kit/kit/steps.jsonl) (2,857 trajectory rows, 1.83 MB)
  - [`calibration_pairs.csv`](file:///C:/Users/richa/ai-engineering/jev_experiment_kit/kit/calibration_pairs.csv) (1,800 pairs)
  - [`frozen_config.json`](file:///C:/Users/richa/ai-engineering/jev_experiment_kit/kit/frozen_config.json)
  - [`noise_pilot.json`](file:///C:/Users/richa/ai-engineering/jev_experiment_kit/kit/noise_pilot.json)
  - [`controls.json`](file:///C:/Users/richa/ai-engineering/jev_experiment_kit/kit/controls.json)
  - [`summary.json`](file:///C:/Users/richa/ai-engineering/jev_experiment_kit/kit/summary.json)
