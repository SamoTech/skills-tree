---
title: "Verifiable Intent Token Presentation Execution"
category: 04-action-execution
level: advanced
stability: experimental
description: "Present and verify verifiable purchase-intent tokens during agent checkout so payment authority is provable."
added: "2026-10"
version: v1
related: [purchase-intent-verification-actions, agent-payment-initiation]
tags: [payments, intent, tokens, verification]
---
# Verifiable Intent Token Presentation Execution

## Description
Present and verify verifiable purchase-intent tokens during agent checkout so payment authority is provable. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A paying agent completes a checkout step that requires presenting a signed intent token and verifying the merchant response.
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
3. Present the signed intent token bound to the order digest, verify the merchant response signature and order binding, and abort when either fails.
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
def present_intent_token(token, order_digest, verify):
    if token.get("order_digest") != order_digest:
        raise ValueError("intent token is bound to a different order")
    if not token.get("signature"):
        raise ValueError("intent token is unsigned")
    return verify(token["signature"], order_digest)
def merchant_response_ok(response, order_digest):
    return bool(response.get("accepted")) and response.get("order_digest") == order_digest
order_digest = "sha256:order-77"
token = {"order_digest": order_digest, "signature": "sig-123"}
assert present_intent_token(token, order_digest, lambda s, d: True)
assert merchant_response_ok({"accepted": True, "order_digest": order_digest}, order_digest)
assert not merchant_response_ok({"accepted": True, "order_digest": "sha256:other"}, order_digest)
```

## Failure Modes
- The intent token is presented without binding it to the order digest and can be replayed against another order.
- Merchant responses are accepted without signature verification and a forged acceptance authorizes payment.
- Token reuse across sessions is permitted and a stale intent token completes a second purchase.
- Verification failures are retried by re-presenting the token instead of aborting the checkout.
- Order digests are compared case-sensitively and valid hex-cased digests are rejected.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Agentic-commerce production reporting describes verifiable intent as a live payment rail requirement, making deterministic intent-token presentation and verification a concrete agent action (the-agent-report.com, dated October 2026) ([public signal](https://the-agent-report.com/2026/10/agentic-commerce-production-rails-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Purchase Intent Verification Actions](../04-action-execution/purchase-intent-verification-actions.md)
- [Agent Payment Initiation](../04-action-execution/agent-payment-initiation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
