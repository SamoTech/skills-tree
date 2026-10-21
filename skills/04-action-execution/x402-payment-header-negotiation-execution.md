---
title: "x402 Payment Header Negotiation Execution"
category: 04-action-execution
level: advanced
stability: experimental
description: "Execute x402 HTTP payment header negotiation so agent payments are bound to responses with verified access tokens."
added: "2026-10"
version: v1
related: [agent-payment-initiation, agent-payment-mandate-signing]
tags: [x402, payments, negotiation, http]
---
# x402 Payment Header Negotiation Execution

## Description
Execute x402 HTTP payment header negotiation so agent payments are bound to responses with verified access tokens. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A paying agent must complete an x402 HTTP payment negotiation and verify the response token before consuming the resource.
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
3. Send the payment offer with declared amount and scheme, validate the returned access token against the response payload, and fail closed when the token does not verify.
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
def negotiate(offer, response):
    if response["amount"] != offer["amount"]:
        raise ValueError("amount mismatch")
    return response["token"] if response["token"].startswith("x402-") else None
r = {"amount": 500, "token": "x402-tok"}
assert negotiate({"amount": 500}, r) == "x402-tok"
```

## Failure Modes
- The access token is not verified against the response payload before use.
- Amount fields are compared as strings and unit mismatches slip through.
- Failed negotiations are retried with doubled amounts instead of failing closed.
- Tokens are stored unscoped and reused across unrelated resources.
- The offer omits the payment scheme and the server guesses the flow.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Reactify documents agentic commerce in production with AP2, ACP, x402, and MPP payment flows (reactify-solutions.com, dated 2026) ([public signal](https://www.reactify-solutions.com/articles/agentic-commerce-protocols-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Payment Initiation](../04-action-execution/agent-payment-initiation.md)
- [Agent Payment Mandate Signing](../04-action-execution/agent-payment-mandate-signing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
