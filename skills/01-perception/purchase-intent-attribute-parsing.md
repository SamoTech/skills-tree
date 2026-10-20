---
title: "Purchase Intent Attribute Parsing"
category: 01-perception
level: advanced
stability: experimental
description: "Parse purchase-intent attributes from AI shopping agent orders so merchants can verify the agent followed the shopper approved instructions."
added: "2026-10"
version: v1
related: [agent-runtime-action-event-parsing, webhook-payload-parsing]
tags: [parsing, purchase-intent, payments, agentic-commerce]
---
# Purchase Intent Attribute Parsing

## Description
Parse purchase-intent attributes from AI shopping agent orders so merchants can verify the agent followed the shopper approved instructions. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A merchant receives an order placed by a shopping agent and must verify it against the recorded shopper instructions before fulfillment.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Extract the intent attributes (requested item, constraints, spend limit) from the order record, compare them with the shopper instruction record, and emit the verification result with the compared fields and any deviations.
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
def verify(order, intent):
    return order["item"] == intent["item"] and order["price"] <= intent["limit"]
intent = {"item": "blue-shirt-m", "limit": 50}
assert verify({"item": "blue-shirt-m", "price": 40}, intent) is True
assert verify({"item": "red-shirt-l", "price": 40}, intent) is False
```

## Failure Modes
- The order is accepted without any recorded instruction to compare against.
- Deviation checks compare only the item and miss quantity, color, or size changes.
- The intent record is summarized instead of quoted and the comparison cannot be re-run.
- Time-of-check to time-of-fulfillment drift is ignored and the intent record ages out silently.
- The verification result is not linked to the dispute record when a mismatch appears later.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 American Express publishes its Intent Intelligence framework so card issuers can verify purchases made by AI shopping agents (digitalcommerce360.com, dated October 16 2026) ([public signal](https://www.digitalcommerce360.com/2026/10/16/american-express-ai-framework/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Runtime Action Event Parsing](../01-perception/agent-runtime-action-event-parsing.md)
- [Webhook Payload Parsing](../01-perception/webhook-payload-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
