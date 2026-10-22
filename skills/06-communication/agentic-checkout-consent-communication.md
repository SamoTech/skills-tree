---
title: "Agentic Checkout Consent Communication"
category: 06-communication
level: advanced
stability: experimental
description: "Write consent prompts and confirmations for agent checkout steps so purchase authority is explicit and recorded."
added: "2026-10"
version: v1
related: [user-intent-restatement-confirmation, human-approval-request-drafting]
tags: [consent, checkout, communication, commerce]
---
# Agentic Checkout Consent Communication

## Description
Write consent prompts and confirmations for agent checkout steps so purchase authority is explicit and recorded. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A shopping agent reaches a purchase decision point and must ask the user for explicit consent in wording the user can actually evaluate.
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
3. Draft the consent request from the order facts, state the exact amount, items, and payment rail, and record the consent response with its wording digest for audit.
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
def build_consent_prompt(order):
    if not order.get("items") or "total" not in order:
        raise ValueError("cannot request consent without items and total")
    items = ", ".join(order["items"])
    return "Approve paying " + order["total"] + " for " + items + " via " + order["rail"] + "?"
def record_consent(prompt, answer):
    return {"prompt_digest": hash(prompt), "answer": answer}
order = {"items": ["socks", "shoes"], "total": "45.00 USD", "rail": "agent-pay"}
prompt = build_consent_prompt(order)
consent = record_consent(prompt, "approved")
assert "45.00 USD" in prompt and consent["answer"] == "approved"
```

## Failure Modes
- The consent prompt hides the payment rail and the user approves a charge they cannot recognize later.
- Consent wording changes silently between sessions and the recorded approval cannot be tied to what the user saw.
- The prompt bundles several purchases into one yes and consent is stretched beyond its scope.
- Silence or timeout is treated as consent and purchases proceed without an explicit answer.
- Consent records store the answer but not the wording digest and cannot be audited.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Coverage of the agentic-commerce protocol and ChatGPT checkout explains the consent points an agent checkout passes through, which the communication must make explicit to the user (swell.is, dated 2026) ([public signal](https://www.swell.is/content/agentic-commerce-protocol-explained))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [User Intent Restatement Confirmation](../06-communication/user-intent-restatement-confirmation.md)
- [Human Approval Request Drafting](../06-communication/human-approval-request-drafting.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
