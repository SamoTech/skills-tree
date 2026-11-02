---
title: "Dataset Fiction Channel Hygiene"
category: 06-communication
level: advanced
stability: experimental
description: "Detect harmful behavior hidden inside fiction, role-play, or ordinary professional questions in datasets and agent conversations."
added: "2026-11"
version: v1
related: [vendor-economics-brief-writing, subscription-tier-communication]
tags: [communication, datasets, hygiene, safety]
---
# Dataset Fiction Channel Hygiene

## Description
Detect harmful behavior hidden inside fiction, role-play, or ordinary professional questions in datasets and agent conversations. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Training or conversational content can carry misaligned behavior disguised as benign fiction, role-play, or routine professional text.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the content stream, the declared narrative-risk markers, and the aggregate behavioral probes. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the narrative-risk markers for fiction, role-play, and professional framing that require deeper inspection.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Trace flagged content through to its behavioral effect and record whether a harmful behavior survives the benign framing.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On unresolved suspicion, quarantine the content, and never clear it because its surface framing looks professional.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def hygiene_check(row):
    if row["channel"] not in ("fiction", "roleplay", "professional"):
        return "clear"
    if row["encodes_harm"] and row["surface_benign"]:
        return "quarantine"
    return "clear"
assert hygiene_check({"channel": "fiction", "encodes_harm": True, "surface_benign": True}) == "quarantine"
assert hygiene_check({"channel": "fiction", "encodes_harm": False, "surface_benign": True}) == "clear"
```

## Failure Modes
- Fiction and role-play are exempted from inspection because the surface text looks harmless.
- Professional framing is treated as a trust signal rather than a disguise channel.
- Quarantined content is released after a single re-read by the same screener.
- The channel tag is inferred from style instead of recorded provenance.
- Aggregate probes are skipped for quarantined batches so hidden behavior passes unnoticed.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Anthropic finding that monitor-passing datasets hid the trained-in behavior inside fiction, role-play, or ordinary professional questions (AI Agent News Today, dated November 1, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Vendor Economics Brief Writing](vendor-economics-brief-writing.md)
- [Subscription Tier Communication](subscription-tier-communication.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
