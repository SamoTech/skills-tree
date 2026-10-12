---
title: "Problem Classification"
category: 02-reasoning
level: intermediate
stability: experimental
description: "Classify an incoming problem into a known type using explicit criteria before selecting a solving method, and abstain when no type matches."
added: "2026-10"
version: v1
related: [prioritization, task-decomposition, decision-making]
tags: [problem, classification, reasoning]
---

# Problem Classification

## Description
Classify an incoming problem into a known type using explicit criteria before selecting a solving method, and abstain when no type matches. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires problem classification before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for problem classification. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the problem classification procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Problem Classification: deterministic check
options = [{"name": "x", "gain": 5, "cost": 1}, {"name": "y", "gain": 4, "cost": 1}]
ranked = sorted(options, key=lambda o: (o["cost"], -o["gain"]))
assert ranked[0]["name"] == "x"
print("best:", ranked[0]["name"])
```

## Failure Modes
- Proceeding with problem classification without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Model- and skill-routing work in 2026 depends on task classification as the first routing stage; classification before dispatch is published across agent frameworks. These are dated public signals, not adoption metrics.

## Related
- prioritization.md
- task-decomposition.md
- decision-making.md
