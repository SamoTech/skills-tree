---
title: "Opportunity Cost Analysis"
category: 02-reasoning
level: advanced
stability: experimental
description: "Evaluate what a chosen course of action displaces, compare selected and rejected alternatives on explicit criteria, and record the cost of the road not taken."
added: "2026-10"
version: v1
related: [trade-off-analysis, cost-benefit-analysis, expected-utility-analysis]
tags: [decisions, tradeoffs, analysis]
---

# Opportunity Cost Analysis

## Description
Evaluate what a chosen course of action displaces, compare selected and rejected alternatives on explicit criteria, and record the cost of the road not taken. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a decision between alternatives must show what the rejected option would have delivered before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for opportunity cost analysis work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the opportunity cost analysis steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def opportunity_cost(chosen, alternative, criteria_weights):
    delta = {}
    for c, w in criteria_weights.items():
        delta[c] = round((alternative[c] - chosen[c]) * w, 4)
    return delta

delta = opportunity_cost({"value": 10, "risk": 2}, {"value": 14, "risk": 5}, {"value": 1.0, "risk": -1.0})
assert delta["value"] == 4.0 and delta["risk"] == -3.0
```

## Failure Modes
- Ignoring the value of rejected alternatives.
- Weighing criteria without stated justification.
- Counting only monetary costs.
- Presenting opportunity cost as realized loss.
- Retro-fitting criteria to justify a prior choice.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Explicit tradeoff accounting is a recurring 2026 decision-support request for agent assistants; this is a dated signal, not an adoption metric.

## Related
- trade-off-analysis.md
- cost-benefit-analysis.md
- expected-utility-analysis.md
