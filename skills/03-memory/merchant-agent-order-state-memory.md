---
title: "Merchant Agent Order State Memory"
category: 03-memory
level: advanced
stability: experimental
description: "Maintain merchant order-state memory so shopping agents can resume a checkout from recorded order facts."
added: "2026-10"
version: v1
related: [agent-payment-spend-history-memory, episodic-memory]
tags: [commerce, orders, memory, checkout]
---
# Merchant Agent Order State Memory

## Description
Maintain merchant order-state memory so shopping agents can resume a checkout from recorded order facts. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A shopping agent returns to a checkout it started earlier and must rebuild the order state from recorded merchant and cart facts.
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
3. Record cart contents, merchant identifiers, price evidence, and checkout progress under a stable order key, and resolve conflicts by preferring the most recent verified record with provenance.
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
def merge_order_state(old, new):
    if new["order_key"] != old["order_key"]:
        raise ValueError("state belongs to a different order")
    if new["seq"] <= old["seq"]:
        return old
    merged = dict(old)
    merged.update(new)
    merged["seq"] = new["seq"]
    return merged
old = {"order_key": "o-77", "seq": 2, "cart": ["socks"], "step": "cart"}
new = {"order_key": "o-77", "seq": 3, "cart": ["socks", "shoes"], "step": "payment"}
assert merge_order_state(old, new)["step"] == "payment"
assert merge_order_state(old, new)["cart"] == ["socks", "shoes"]
```

## Failure Modes
- Order state is keyed by session id and the same cart is loaded after the session rotates.
- Stale price memories are trusted and the agent pays a recorded price the merchant no longer offers.
- Conflicting states are merged field-by-field without sequence checks and produce a mixed-order record.
- Checkout progress is remembered but the consent decisions behind it are not, and a payment resumes without authority.
- Merchant identifiers are stored loosely and receipts cannot be reconciled with the ledger later.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Agentic-commerce production reporting records verifiable intent and live agent payments, which require agents to keep resumable, provable order state across checkout steps (the-agent-report.com, dated October 2026) ([public signal](https://the-agent-report.com/2026/10/agentic-commerce-production-rails-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Payment Spend History Memory](../03-memory/agent-payment-spend-history-memory.md)
- [Episodic Memory](../03-memory/episodic-memory.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
