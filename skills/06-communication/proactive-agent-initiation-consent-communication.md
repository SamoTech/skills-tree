---
title: "Proactive Agent Initiation Consent Communication"
category: 06-communication
level: advanced
stability: experimental
description: "Write the consent and announcement messages a proactive agent sends before initiating an action, with explicit waits, risk-tiered consent, and no pressure phrasing."
added: "2026-10"
version: v1
related: [permission-request-plain-language-writing, user-intent-restatement-confirmation]
tags: [proactive, agent, initiation, consent]
---
# Proactive Agent Initiation Consent Communication

## Description
Write the consent and announcement messages a proactive agent sends before initiating an action, with explicit waits, risk-tiered consent, and no pressure phrasing. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A proactive agent must announce an intended action and obtain explicit consent without manipulating the user.
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
3. Draft the initiation message naming the exact action and its first observable effect, tie the required consent level to the risk tier, and record the message with the consent outcome before acting.
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
def initiation_message(action, risk):
    msg = f"May I {action}? I will wait for your yes before starting."
    return {"text": msg, "requires_explicit_consent": risk == "high"}
m = initiation_message("email the vendor list", "high")
assert m["requires_explicit_consent"] and "wait" in m["text"]
```

## Failure Modes
- The agent announces and acts in the same message and consent is never actually collected.
- Pressure phrasing pushes the user to accept and consent is manufactured.
- The risk tier is omitted and a high-risk action gets a low-friction yes.
- The announcement names a vague action and the user consents to something other than what runs.
- Consent is recorded without the message that produced it and audits cannot verify what was agreed.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The launch of Claude Duet, a proactive agent app that initiates actions for users, is the dated public signal for this communication contract. ([public signal](https://aibriefs.news/ai-news-today))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Permission Request Plain Language Writing](../06-communication/permission-request-plain-language-writing.md)
- [User Intent Restatement Confirmation](../06-communication/user-intent-restatement-confirmation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
