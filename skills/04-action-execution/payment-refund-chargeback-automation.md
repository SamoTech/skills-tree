---
title: "Payment Refund and Chargeback Automation"
category: 04-action-execution
level: advanced
stability: experimental
description: "Execute agentic-commerce refunds and chargeback responses through declared mandate checks so that money moves only within the recorded authorization."
added: "2026-10"
version: v1
related: [agent-payment-initiation, micropayment-batching]
tags: [payments, refunds, chargebacks, agentic-commerce]
---
# Payment Refund and Chargeback Automation

## Description
Execute agentic-commerce refunds and chargeback responses through declared mandate checks so that money moves only within the recorded authorization. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent must issue refunds or respond to chargebacks without improvising authorization.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Match the refund request to its original mandate and settlement record, verify the amount against the mandate balance, and execute the refund only when every check passes on record.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def refundable(mandate, requested):
    if mandate["status"] != "active":
        return False
    return requested <= mandate["remaining_minor_units"]
m = {"status": "active", "remaining_minor_units": 500}
assert refundable(m, 400) and not refundable(m, 600)
```

## Failure Modes
- A refund is issued against a mandate that was already expired or revoked.
- Partial refunds are double-counted against the same mandate balance.
- A chargeback response is filed after the network deadline and counted as handled.
- The refund amount is taken in major units while the mandate tracks minor units.
- Refund records are written after execution, so a crash between pay and record loses the audit trail.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 agentic-commerce coverage reports agent-mediated payment operations including disputes as an active ecosystem direction (aiagentstore.ai weekly news, dated October 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Payment Initiation](../04-action-execution/agent-payment-initiation.md)
- [Micropayment Batching](../04-action-execution/micropayment-batching.md)

## Changelog
| Version | Date | Notes |
|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
