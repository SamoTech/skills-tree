---
title: "Dry-Run Execution"
category: 04-action-execution
level: intermediate
stability: experimental
description: "Execute a preview of a state-changing action that reports what would happen without applying effects, and verify preview support instead of assuming it."
added: "2026-10"
version: v1
related: [compensating-actions, assertion, rollback-undo]
tags: [dry, run, execution, action]
---
# Dry-Run Execution

## Description
Execute a preview of a state-changing action that reports what would happen without applying effects, and verify preview support instead of assuming it. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires dry-run execution before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for dry-run execution. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the dry-run execution procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Dry-Run Execution: deterministic check
candidates = [{"id": "a", "score": 0.8, "cost": 2}, {"id": "b", "score": 0.95, "cost": 9}]
eligible = [c for c in candidates if c["score"] >= 0.8]
selected = min(eligible, key=lambda c: c["cost"])
assert selected["id"] == "a"
print("selected:", selected["id"])
```

## Failure Modes
- Proceeding with dry-run execution without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Safe-preview execution is requested across 2026 agent tooling threads as a guardrail before destructive operations. These are dated public signals, not adoption metrics.

## Related
- compensating-actions.md
- assertion.md
- rollback-undo.md
