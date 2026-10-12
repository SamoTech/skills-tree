---
title: "Action Precondition Checking"
category: 04-action-execution
level: advanced
stability: experimental
description: "Verify declared preconditions such as existence, permissions, quotas, and states before executing an action, and fail closed with reasons when one does not hold."
added: "2026-10"
version: v1
related: [assertion, quota-management, permission-checking]
tags: [action, precondition, checking, action]
---

# Action Precondition Checking

## Description
Verify declared preconditions such as existence, permissions, quotas, and states before executing an action, and fail closed with reasons when one does not hold. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for action precondition checking. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the action precondition checking steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Action Precondition Checking: deterministic check
def validate(record, required):
    missing = [k for k in required if k not in record]
    return (True, []) if not missing else (False, missing)

ok, missing = validate({"id": "x", "source": "y"}, ["id", "source"])
assert ok and not missing
print("validated")
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
Fail-closed pre-execution authorization is named in OWASP-style 2026 agentic guidance; precondition checks are a published requirement. These are dated public signals, not adoption metrics.

## Related
- assertion.md
- quota-management.md
- permission-checking.md
