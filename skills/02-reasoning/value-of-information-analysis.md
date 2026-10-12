---
title: "Value of Information Analysis"
category: 02-reasoning
level: intermediate
stability: experimental
description: "Decide whether gathering a piece of information is worth its cost by comparing expected decision improvement against acquisition cost before acting."
added: "2026-10"
version: v1
related: [cost-benefit-analysis, decision-making, sensitivity-analysis]
tags: [value, of, information, analysis, reasoning]
---
# Value of Information Analysis

## Description
Decide whether gathering a piece of information is worth its cost by comparing expected decision improvement against acquisition cost before acting. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires value of information analysis before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for value of information analysis. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the value of information analysis steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Value of Information Analysis: deterministic check
def check_budget(estimate, limit):
    if estimate > limit:
        raise ValueError("estimate %s exceeds limit %s" % (estimate, limit))
    return "approved"

assert check_budget(3, 5) == "approved"
try:
    check_budget(7, 5)
    raise AssertionError("should have raised")
except ValueError:
    print("guard held")
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Cost-aware agent behavior is a 2026 theme; public runaway-cost incidents drive requests for pre-acquisition value analysis. These are dated public signals, not adoption metrics.

## Related
- cost-benefit-analysis.md
- decision-making.md
- sensitivity-analysis.md
