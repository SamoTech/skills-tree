---
title: "Press Statement Drafting"
category: 06-communication
level: advanced
stability: experimental
description: "Draft external statements with verified facts only, a single approved quote, and a defined holding line for unverified questions."
added: "2026-10"
version: v1
related: [audience-analysis, tone-adjustment, conflict-de-escalation-writing]
tags: [pr, writing, governance]
---

# Press Statement Drafting

## Description
Draft external statements with verified facts only, a single approved quote, and a defined holding line for unverified questions. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an external statement must be issued and every fact in it must be verified before release.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for press statement drafting work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the press statement drafting steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def statement(facts, quote, holding):
    unverified = [f for f in facts if not f.get("verified")]
    return {"publishable": not unverified, "unverified": [f["text"] for f in unverified], "quote": quote, "holding": holding}

s = statement([{"text": "a", "verified": True}, {"text": "b", "verified": False}], "we are looking into it", "no comment yet")
assert s["publishable"] is False and s["unverified"] == ["b"]
```

## Failure Modes
- Publishing a fact that no one verified.
- Admitting or denying legal exposure in prose.
- Multiple quotes from different drafts circulating.
- No agreed holding line for follow-up calls.
- Letting the draft leak before approval.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Careful external statement drafting is a recurring 2026 communications-governance topic in public coverage; this is a dated signal, not an adoption metric.

## Related
- audience-analysis.md
- tone-adjustment.md
- conflict-de-escalation-writing.md
