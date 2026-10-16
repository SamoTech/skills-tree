---
title: "X402 Payment Flow Execution"
category: 04-action-execution
level: advanced
stability: experimental
description: "Execute x402 crypto payment flows for agent purchases by validating the payment request, confirming spend limits, and recording the transaction reference and verification evidence before completing the action."
added: "2026-10"
version: v1
related: [agent-payment-initiation, micropayment-batching]
tags: [x402, payments, execution]
---
# X402 Payment Flow Execution

## Description
Execute x402 crypto payment flows for agent purchases by validating the payment request, confirming spend limits, and recording the transaction reference and verification evidence before completing the action. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent must pay for a resource using the x402 protocol within an explicit spend limit.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | an x402 payment request, a spend-limit policy, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the x402 payment flow steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A payment record with the validated request, the spend decision, the transaction reference, and verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def approve_payment(req, limit):
    if req["amount"] > limit:
        return {"decision": "deny", "reason": "over limit"}
    return {"decision": "approve", "ref": req["ref"]}
d = approve_payment({"amount": 5, "ref": "x1"}, 10)
assert d["decision"] == "approve" and d["ref"] == "x1"
```

## Failure Modes
- Approving a payment whose request fields fail validation against the advertised resource.
- Paying without a pre-declared spend limit and treating the denial as a blocker to invent later.
- Losing the transaction reference, making the purchase unverifiable after the fact.
- Retrying a failed payment repeatedly instead of recording the failure and stopping.
- Reporting a completed purchase without confirming the resource was delivered.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- AI agents made 138 million crypto payments via x402 in dated October 2026 reporting. ([public signal](https://www.coindesk.com/business/2026/10/14/ai-agents-make-138-million-crypto-payments-as-u-s-dominates-spending-on-ai-models))
- x402 payment flow design is part of 2026 agentic-commerce protocol coverage. ([public signal](https://agenticplug.ai/current-state-of-agentic-commerce))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [agent payment initiation](../04-action-execution/agent-payment-initiation.md)
- [micropayment batching](../04-action-execution/micropayment-batching.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

