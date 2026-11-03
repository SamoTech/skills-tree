---
title: "Booking Confirmation Message Contracts"
category: 06-communication
level: advanced
stability: experimental
description: "Send booking confirmations with a fixed message contract covering venue, time, party size, and reservation identifier so the user can verify what was actually booked."
added: "2026-11"
version: v1
related: [booking-consent-error-messaging, session-handoff-status-messaging]
tags: [confirmation, message-contracts, booking, communication]
---
# Booking Confirmation Message Contracts

## Description
Send booking confirmations with a fixed message contract covering venue, time, party size, and reservation identifier so the user can verify what was actually booked. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A conversational booking agent confirms reservations and a vague confirmation has already left users at the wrong venue or time.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the confirmed reservation record, the message template contract, and the delivery channel. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the confirmation contract fields and require every field present before composing.
2. Compose the message strictly from the reservation record with no added assumptions.
3. Deliver the confirmation in the same thread the booking was requested in.
4. Verify the delivered message against the contract fields and record the match result.
5. On a missing field, withhold the confirmation and report the incomplete record.
6. Emit a structured result with the delivered message and the field-by-field verification.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def build_confirmation(res, contract):
    missing = [f for f in contract if f not in res]
    if missing:
        return {"sent": False, "missing": missing}
    msg = " | ".join(f"{f}: {res[f]}" for f in contract)
    return {"sent": True, "message": msg}
contract = ["venue", "time", "party", "reservation_id"]
ok = {"venue": "Sushi A", "time": "19:00", "party": 2, "reservation_id": "RES-9"}
assert build_confirmation(ok, contract)["sent"] is True
assert build_confirmation({"venue": "X"}, contract)["missing"] == ["time", "party", "reservation_id"]
```

## Failure Modes
- Confirmations are free-text and omit the reservation identifier, leaving no proof of booking.
- The message includes details that were never part of the reservation record.
- Confirmation is delivered to a different channel than the request thread.
- A missing field is filled with a default instead of withholding the message.
- The delivered message is never checked against the contract, so drift goes unnoticed.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Zest concierge completing restaurant bookings through OpenTable, Resy, or SevenRooms inside text messages, where the confirmation is the user's only receipt (AI Agent News Today, dated November 1, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Booking Consent Error Messaging](booking-consent-error-messaging.md)
- [Session Handoff Status Messaging](session-handoff-status-messaging.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
