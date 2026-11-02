---
title: "Governed Answer Explanation Writing"
category: 06-communication
level: advanced
stability: experimental
description: "Write agent answers that cite governed business sources and state what changed when the governed data changes."
added: "2026-11"
version: v1
related: [cloud-session-handoff-communication, shared-link-privacy-communication]
tags: [communication, answers, governance, attribution]
---

# Governed Answer Explanation Writing

## Description
Write agent answers that cite governed business sources and state what changed when the governed data changes. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An enterprise agent answers business questions and its answers must trace to governed data rather than generic model text.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the question, the governed source set per business concept, and the ambiguity marking policy. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Declare the governed source for each business concept the answer will touch and the policy for ambiguous cases.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Write the answer with source attribution per claim and explicit markers on ambiguous cases.
4. Compare the written answer against the governed source data and record deviations.
5. Where a claim has no governed source, mark it unverified, and never present it as grounded.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def write_answer(claims):
    grounded = [c for c in claims if c["source"]]
    return {"grounded": len(grounded), "unverified": len(claims) - len(grounded)}
r = write_answer([{"source": "ontology"}, {"source": None}])
assert r["grounded"] == 1 and r["unverified"] == 1
```

## Failure Modes
- Claims are written without a governed source and presented as grounded anyway.
- Deliberately ambiguous cases are presented as settled answers.
- Policies are cited from a stale governed version without a date check.
- Answers are not re-tested when the governed data changes underneath them.
- Attribution is decorative rather than structural so claims cannot be traced back.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- SAP announcing Joule Studio, Joule Work, and Business AI Platform tools with data-fabric and ontology capabilities intended to give agents trusted information about business entities, relationships, processes, and policies, with guidance to test answers against governed source data and deliberately ambiguous cases (AI Agent News Today, dated November 2, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Cloud Session Handoff Communication](cloud-session-handoff-communication.md)
- [Shared Link Privacy Communication](shared-link-privacy-communication.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
