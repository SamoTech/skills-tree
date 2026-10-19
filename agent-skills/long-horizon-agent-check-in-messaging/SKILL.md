---
name: long-horizon-agent-check-in-messaging
description: Design check-in messages for long-horizon agents that surface decisions needing human input long before deadlines, with crisp options and consequences.
metadata:
  source: skills/06-communication/long-horizon-agent-check-in-messaging.md
  category: 06-communication
  version: "v1"
---

# Long-Horizon Agent Check-In Messaging

## Description
Design check-in messages for long-horizon agents that surface decisions needing human input long before deadlines, with crisp options and consequences. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A long-horizon agent reaches a decision point that needs human input while work continues.
- The outcome would change if the request arrived too late to act on.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the plan milestones, open decision list, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Identify the blocking decision, compute the response deadline from the plan, and send the check-in with options and deadline consequences.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A che
ck-in message with the decision, response deadline, options, and the consequence of no response. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def checkin(decision, days_left, opts):
    urgency = "now" if days_left <= 2 else "this-week"
    return {"decision": decision, "urgency": urgency, "options": opts}
m = checkin("pick-vendor", 1, ["a", "b"])
assert m["urgency"] == "now" and len(m["options"]) == 2
```

## Failure Modes
- Burying the blocking decision in a long status update nobody reads.
- Requesting input without stating what happens if no one responds in time.
- Sending the check-in after the decision deadline has already passed.
- Repeating the same check-in every cycle without escalating.
- Framing options in ways that presume one answer and bias the human.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 persistent-agent launches make long-horizon work with periodic human touchpoints a mainstream agent pattern ([public signal](https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Human Approval Request Drafting](../06-communication/human-approval-request-drafting.md)
- [Long Horizon Planning](../02-reasoning/long-horizon-planning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
