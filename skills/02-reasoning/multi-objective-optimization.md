---
title: "Multi-Objective Optimization"
category: 02-reasoning
level: basic
stability: experimental
description: "Reason about tasks with competing objectives by constructing a Pareto frontier and selecting a documented trade-off point instead of collapsing objectives into a single score."
added: "2026-10"
version: v1
related: [trade-off-analysis, pareto-analysis, decision-making]
tags: [multi, objective, optimization, reasoning]
---

# Multi-Objective Optimization

## Description
Reason about tasks with competing objectives by constructing a Pareto frontier and selecting a documented trade-off point instead of collapsing objectives into a single score. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- The task has explicit constraints such as time, budget, or safety that must gate the outcome.
- A silent failure mode exists that must be surfaced rather than swallowed.
- Verification evidence is required before the result is trusted.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for multi-objective optimization. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the multi-objective optimization procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Multi-Objective Optimization: deterministic check
candidates = [{"id": "a", "score": 0.8, "cost": 2}, {"id": "b", "score": 0.95, "cost": 9}]
eligible = [c for c in candidates if c["score"] >= 0.8]
selected = min(eligible, key=lambda c: c["cost"])
assert selected["id"] == "a"
print("selected:", selected["id"])
```

## Failure Modes
- Proceeding with multi-objective optimization without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Production agent teams in 2026 report competing accuracy, cost, and latency goals; published routing work treats objective trade-offs as explicit. These are dated public signals, not adoption metrics.

## Related
- trade-off-analysis.md
- pareto-analysis.md
- decision-making.md
