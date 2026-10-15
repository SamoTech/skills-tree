---
title: "Agent Payment Mandate Signing"
category: 04-action-execution
level: advanced
stability: experimental
description: "Create and verify signed payment mandates that bind an intent to a cart and payment evidence chain before any charge."
added: "2026-10"
version: v1
related: [agent-payment-initiation, signed-webhook-verification, short-lived-credential-acquisition]
tags: [agent, payment, mandate, signing]
---
# Agent Payment Mandate Signing

## Description
Create and verify signed payment mandates that bind an intent to a cart and payment evidence chain before any charge. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires agent payment mandate signing before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agent payment mandate signing. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent payment mandate signing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def mandate_valid(intent, cart, signature):
    return intent["cart_id"] == cart["id"] and signature == "sig:" + cart["id"]
assert mandate_valid({"cart_id": "c1"}, {"id": "c1"}, "sig:c1") is True
assert mandate_valid({"cart_id": "c1"}, {"id": "c1"}, "sig:c2") is False
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
AP2 agentic commerce defines signed mandates as the proof that an agent purchase was authorized. These are dated public signals, not adoption metrics.

## Related
- agent-payment-initiation.md
- signed-webhook-verification.md
- short-lived-credential-acquisition.md
