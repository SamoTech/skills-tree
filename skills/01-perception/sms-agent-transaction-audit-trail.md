---
title: "Sms Agent Transaction Audit Trail"
category: 01-perception
level: advanced
stability: experimental
description: "Record every step of an agent transaction conducted over text messaging so booking actions, user consent, and errors can be audited later."
added: "2026-10"
version: v1
related: [agent-traffic-origin-identification, laboratory-instrument-request-parsing]
tags: [agents, transactions, audit, messaging]
---
# Sms Agent Transaction Audit Trail

## Description
Record every step of an agent transaction conducted over text messaging so booking actions, user consent, and errors can be audited later. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent completes a booking or purchase inside a messaging thread and the transaction record must be reconstructable end to end.
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
3. Capture each message, tool call, provider response, and consent statement into an append-only transaction record keyed by session and provider.
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
def record_step(ledger, step):
    ledger.append({"step": step["kind"], "provider": step["provider"], "ok": step["ok"]})
    return ledger
ledger = []
record_step(ledger, {"kind": "consent", "provider": "user", "ok": True})
record_step(ledger, {"kind": "booking", "provider": "resy", "ok": False})
assert ledger[-1]["ok"] is False and len(ledger) == 2
```

## Failure Modes
- The consent snapshot is missing so later disputes cannot show what the user approved.
- A provider response is dropped when a retry succeeds and the failed attempt disappears from the record.
- Only the final outcome is recorded so intermediate deviations are unrecoverable.
- Personally identifiable details are stored unredacted in a log shared beyond the audit boundary.
- The record carries no provider correlation identifier so entries cannot be matched to the booking system.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Zest restaurant concierge completing discovery and booking through text messages via OpenTable, Resy, and SevenRooms while its guidance calls for monitoring booking errors, user consent, and recommendation quality (undefined, dated October 31, 2026) ([public signal](undefined))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Traffic Origin Identification](agent-traffic-origin-identification.md)
- [Laboratory Instrument Request Parsing](laboratory-instrument-request-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
