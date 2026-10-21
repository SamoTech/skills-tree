---
name: x402-payment-retry-idempotency-pattern
description: Apply the retry idempotency pattern to x402 payments so replays settle exactly once under ambiguous failures.
metadata:
  source: skills/09-agentic-patterns/x402-payment-retry-idempotency-pattern.md
  category: 09-agentic-patterns
  version: "v1"
---

# X402 Payment Retry Idempotency Pattern

## Description
Apply the retry idempotency pattern to x402 payments so replays settle exactly once under ambiguous failures. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An x402 payment returns an ambiguous failure and the retry must not double-charge.
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
3. Derive the idempotency key from the payment intent, record the attempt before sending, and reconcile the settlement state before any retry.
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
def retry_x402(attempts, ledger):
    last = attempts[-1]
    if ledger.get(last["key"]) == "settled":
        raise ValueError("already settled; retry would double-charge")
    if last["status"] == "in_flight":
        return {"retry": False, "reason": "await settlement state"}
    return {"retry": True, "key": last["key"]}
ledger = {"pay-7": "failed"}
attempts = [{"key": "pay-7", "status": "failed"}]
assert retry_x402(attempts, ledger) == {"retry": True, "key": "pay-7"}
```

## Failure Modes
- Retries mint a fresh idempotency key and each attempt becomes a new payment.
- The settlement ledger is not consulted and a settled payment is retried.
- In-flight attempts are retried immediately and both completions settle.
- The attempt is recorded after sending and a crash loses the payment trace.
- Retry counts are unbounded and a persistent failure loops at cost.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- PatTech Labs publishes a 2026 guide to x402, AP2, and Mastercard Move agent payment integrations with Visa and Mastercard (patechlabs.com, dated October 9, 2026) ([public signal](https://www.patechlabs.com/news/ai-agent-payments-guide-x402-ap2-mpp-visa-mastercard))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Checkpoint Restore Patterns](../09-agentic-patterns/agent-checkpoint-restore-patterns.md)
- [Agent Cost Accounting](../09-agentic-patterns/agent-cost-accounting.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
