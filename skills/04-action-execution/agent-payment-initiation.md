---
title: "Agent Payment Initiation"
category: 04-action-execution
level: advanced
stability: experimental
description: "Initiate payments under explicit mandates with amount caps, idempotency keys, and human approval above declared thresholds, and verify settlement state before reporting success."
added: "2026-10"
version: v1
related: [idempotent-retries, compensating-actions, quota-management]
tags: [payments, authorization, agents]
---

# Agent Payment Initiation

## Description
Initiate payments under explicit mandates with amount caps, idempotency keys, and human approval above declared thresholds, and verify settlement state before reporting success. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a payment must be initiated by an agent under a recorded, capped mandate before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agent payment initiation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent payment initiation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def authorize(amount, mandate):
    if amount > mandate["cap"]:
        raise ValueError("amount exceeds mandate cap")
    if amount > mandate["auto_approve_below"]:
        return "needs-human-approval"
    return "approved"

m = {"cap": 500, "auto_approve_below": 100}
assert authorize(50, m) == "approved"
assert authorize(400, m) == "needs-human-approval"
try:
    authorize(600, m)
    raise AssertionError("should have raised")
except ValueError:
    print("mandate cap held")
```

## Failure Modes
- Initiating payment without an explicit mandate.
- Reusing idempotency keys across different payments.
- Reporting success before settlement is verified.
- Raising caps under pressure to complete the task.
- Retrying a failed payment without deduplicating the attempt.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Cryptographically accountable payment mandates for agents are a documented 2026 protocol-stack theme; this is a dated public signal, not an adoption metric.

## Related
- idempotent-retries.md
- compensating-actions.md
- quota-management.md
