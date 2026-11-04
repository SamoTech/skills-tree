---
title: "Plain Language Analysis Scope Clarification"
category: 06-communication
level: advanced
stability: experimental
description: "Clarify plain-language analysis requests by binding each spoken term to a data scope, time range, and metric before analysis starts."
added: "2026-11"
version: v1
related: [lead-qualification-messaging-communication, booking-consent-confirmation-communication]
tags: [communication, clarification, plain-language, analysis]
---
# Plain Language Analysis Scope Clarification

## Description
Clarify plain-language analysis requests by binding each spoken term to a data scope, time range, and metric before analysis starts. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A business user delegating analysis in plain language must have their terms bound to data scope first.
- The outcome would change if the analyst agent guessed at an undefined term.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The plain-language request, the data dictionary, and the permitted metric set. |
| Outputs | A clarified request with per-term bindings and the unanswerable parts named. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Split the request into its analytical terms, filters, and expected outputs.
2. Bind each term to a data dictionary entry or mark it unbindable.
3. Bind each time range to an explicit interval with its data freshness.
4. Bind each metric to the permitted metric set and reject improvised metrics.
5. Present the binding back to the user for confirmation before analysis starts.
6. Record the confirmed bindings as the contract the analysis must answer.

## Outputs
| Area | Contract |
|---|---|
| Primary | A clarified request binding each term to scope, time range, and metric, with unanswerable parts named for the user. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def clarify_request(terms, dictionary):
    bound = {t: dictionary.get(t) for t in terms}
    unbindable = [t for t, v in bound.items() if v is None]
    return {"bindable": not unbindable, "unbindable": unbindable}
d = {"revenue": "sum(net_amount)", "churn": "rate(cancelled)"}
r = clarify_request(["revenue", "growth"], d)
assert r["bindable"] is False and r["unbindable"] == ["growth"]
```

## Failure Modes
- An unbindable term is mapped to the closest dictionary entry without telling the user.
- Time ranges are left implicit and the analysis silently picks a default window.
- The bindings are never presented back, so the user cannot correct a wrong scope.
- Improvised metrics are computed instead of rejecting non-permitted definitions.
- The analysis starts before the user confirms the presented bindings.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Jedify launching Data Agents to let business teams set up autonomous AI analysts using plain-language instructions, with unanticipated questions the detail to watch (Agentic AI News, dated November 2, 2026) ([public signal](https://agentic.ai/news))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Lead Qualification Messaging Communication](lead-qualification-messaging-communication.md)
- [Booking Consent Confirmation Communication](booking-consent-confirmation-communication.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
