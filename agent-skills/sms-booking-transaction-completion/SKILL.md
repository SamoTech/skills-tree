---
name: sms-booking-transaction-completion
description: Complete a booking transaction end to end inside a text-message conversation, including availability checks, provider confirmation, and a recorded receipt.
metadata:
  source: skills/04-action-execution/sms-booking-transaction-completion.md
  category: 04-action-execution
  version: "v1"
---

# Sms Booking Transaction Completion

## Description
Complete a booking transaction end to end inside a text-message conversation, including availability checks, provider confirmation, and a recorded receipt. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A user asks an agent inside a messaging thread to secure a real reservation and a half-completed booking would strand them without confirmation.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the message thread state, the booking intent with constraints, the provider booking API, and the confirmation receipt contract. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Extract the booking intent and constraints from the thread before any external call.
2. Check availability with the provider and present the matched slot for explicit user confirmation.
3. Submit the booking only after confirmation and capture the provider reservation identifier.
4. Verify the reservation by reading it back from the provider before telling the user it is done.
5. On any failure, report the failed stage in the thread and preserve the intent for retry.
6. Emit a structured result with the reservation identifier, read-back, and receipt.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def complete_booking(provider, intent, confirmed):
    if not confirmed:
        return {"booked": False, "reason": "awaiting user confirmation"}
    slot = provider["availability"].get(intent["slot"])
    if slot is None:
        return {"booked": False, "reason": "slot unavailable"}
    rid = provider["book"](intent["slot"])
    if provider["fetch"](rid)["slot"] != intent["slot"]:
        return {"booked": False, "reason": "read-back mismatch"}
    return {"booked": True, "reservation": rid}
prov = {"availability": {"19:00": 1}, "book": lambda s: "RES-9", "fetch": lambda r: {"slot": "19:00"}}
assert complete_booking(prov, {"slot": "19:00"}, False)["reason"] == "awaiting user confirmation"
assert complete_booking(prov, {"slot": "19:00"}, True)["booked"] is True
assert complete_booking(prov, {"slot": "20:00"}, True)["reason"] == "slot unavailable"
```

## Failure Modes
- The booking is submitted before the user confirms the slot in the thread.
- The agent reports success without reading the reservation back from the provider.
- Availability from an earlier check is reused after time has passed.
- A failed booking is retried without telling the user the first attempt failed.
- The receipt is never delivered to the thread, so the user has no proof of booking.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Zest launching a personal AI restaurant concierge over text messages that checks availability and books through OpenTable, Resy, or SevenRooms without a separate app (AI Agent News Today, dated November 1, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Booking Provider Fallback Dispatch](booking-provider-fallback-dispatch.md)
- [Irreversible Transaction Confidence Gating](irreversible-transaction-confidence-gating.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
