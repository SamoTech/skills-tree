---
title: "Action Cost Estimation"
category: 04-action-execution
level: advanced
stability: experimental
description: "Estimate the expected cost of an action before execution and require explicit approval when the estimate exceeds a declared budget threshold."
added: "2026-10"
version: v1
related: [quota-management, batch-processing, budget-management]
tags: [action, cost, estimation, action]
---
# Action Cost Estimation

## Description
Estimate the expected cost of an action before execution and require explicit approval when the estimate exceeds a declared budget threshold. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for action cost estimation. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the action cost estimation procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Action Cost Estimation: deterministic check
allowed = {"idle": {"running"}, "running": {"done", "failed"}, "failed": {"idle"}}

def transition(state, nxt):
    return nxt in allowed.get(state, set())

assert transition("idle", "running")
assert not transition("idle", "done")
print("transitions checked")
```

## Failure Modes
- Proceeding with action cost estimation without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Public 2026 incidents of runaway agent spend drive demand for pre-execution cost estimation and spend guardrails. These are dated public signals, not adoption metrics.

## Related
- quota-management.md
- batch-processing.md
- budget-management.md
