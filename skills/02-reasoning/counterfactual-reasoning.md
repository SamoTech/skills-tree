![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-counterfactual-reasoning.json)

# Counterfactual Reasoning

**Category:** `reasoning`  
**Skill Level:** `advanced`  
**Stability:** `stable`  
**Added:** 2025-03  
**Version:** v2

---

## Description

Reason about hypothetical alternative histories: "What would have happened if X had been different?" Counterfactual reasoning underpins causal inference, debugging, root-cause analysis, and policy evaluation. It requires building a causal model of the world and then intervening on specific variables.

---

## Counterfactual vs. Hypothetical

| Type | Premise | Example |
|---|---|---|
| **Counterfactual** | Contrary to known fact | "If I hadn't deployed Friday, the outage wouldn't have happened" |
| **Hypothetical** | Unknown outcome | "If we launch in Q3, will revenue increase?" |
| **Semifactual** | Same outcome under changed antecedent | "Even if the tests had passed, the bug would still ship" |

---

## Reasoning Steps

1. **Identify the factual world** — what actually happened
2. **Define the intervention** — which variable to change
3. **Build a causal model** — what depends on what (DAG)
4. **Propagate the change** — follow causal edges forward
5. **Compare outcomes** — contrast actual vs. counterfactual world

---

## Example — Root Cause Analysis

```
Fact: Service latency spiked at 14:32. Deployment happened at 14:30.

Counterfactual question: Would latency have spiked if the deployment hadn't occurred?

Causal chain:
  deployment → new DB query pattern → full table scan → high latency

Counterfactual world (no deployment):
  No new query pattern → no full table scan → latency stays normal

Conclusion: Deployment IS the root cause (latency spike counterfactually depends on it).
```

---

## Prompt Pattern

```
Given the following situation:
[ACTUAL EVENTS]

Answer this counterfactual question:
[WHAT IF X HAD BEEN DIFFERENT?]

Steps:
1. Identify what changed
2. Trace the causal chain forward
3. State what would be different in the outcome
4. Note any confounders that might weaken the counterfactual
```

---

## Failure Modes

- **Ignoring confounders** — a third variable causes both X and Y; changing X wouldn't change Y
- **Butterfly effect fallacy** — over-extending the causal chain to implausible extremes
- **Hindsight bias** — assuming the counterfactual was obvious before the fact
- **Underdetermination** — multiple interventions could produce the same counterfactual outcome

---

## Related Skills

- [Causal Reasoning](causal.md)
- [Hypothesis Generation](hypothesis-generation.md)
- [Risk Assessment](risk-assessment.md)
- [Self-Correction](self-correction.md)
