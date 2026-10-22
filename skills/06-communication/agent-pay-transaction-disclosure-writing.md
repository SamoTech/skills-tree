---
title: "Agent Pay Transaction Disclosure Writing"
category: 06-communication
level: advanced
stability: experimental
description: "Write user-facing disclosures for agent-initiated payments with amount, rail, and reversibility facts."
added: "2026-10"
version: v1
related: [payment-protocol-merchant-integration-faq-writing, capability-limitation-disclosure-writing]
tags: [payments, disclosure, writing, transparency]
---
# Agent Pay Transaction Disclosure Writing

## Description
Write user-facing disclosures for agent-initiated payments with amount, rail, and reversibility facts. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A paying agent must tell its user exactly what was purchased, for how much, on which rail, and whether it can be reversed.
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
3. Compose the disclosure from the verified transaction record, covering itemized amount, payment rail, authorization scope, and reversibility, and require each fact to trace to the ledger record.
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
def write_payment_disclosure(tx):
    required = {"amount", "currency", "rail", "reversible", "authorization_scope"}
    missing = required - set(tx)
    if missing:
        raise ValueError("disclosure missing facts: " + ", ".join(sorted(missing)))
    head = "Paid " + tx["amount"] + " " + tx["currency"] + " via " + tx["rail"] + " for " + tx["authorization_scope"] + ". "
    if tx["reversible"]:
        return head + "Reversible within the rail window."
    return head + "Not reversible once settled."
text = write_payment_disclosure({"amount": "10.00", "currency": "USD", "rail": "agent-pay", "reversible": True, "authorization_scope": "groceries basket 77"})
assert "10.00 USD" in text and "agent-pay" in text and "Reversible" in text
```

## Failure Modes
- The disclosure omits reversibility and the user cannot judge refund risk.
- Amounts are rounded for readability and the disclosed total no longer matches the ledger.
- The rail is described by marketing name and the user cannot recognize the charge on their statement.
- A missing fact is filled with a plausible default instead of failing the disclosure.
- Disclosure copy is generated before the transaction settles and later amendments are never re-sent.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Agentic-commerce production coverage of live agent payments makes explicit user disclosure of what agents pay, on which rail, with what reversibility a stated production requirement (the-agent-report.com, dated October 2026) ([public signal](https://the-agent-report.com/2026/10/agentic-commerce-production-rails-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Payment Protocol Merchant Integration Faq Writing](../06-communication/payment-protocol-merchant-integration-faq-writing.md)
- [Capability Limitation Disclosure Writing](../06-communication/capability-limitation-disclosure-writing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
