---
title: "Review Comment Resolution Planning"
category: 05-code
level: advanced
stability: experimental
description: "Turn code review comments into a tracked resolution plan with explicit accept, reject, and defer decisions recorded per comment."
added: "2026-10"
version: v1
related: [code-review, bug-fixing, requirement-tracing]
tags: [code-review, planning, process]
---

# Review Comment Resolution Planning

## Description
Turn code review comments into a tracked resolution plan with explicit accept, reject, and defer decisions recorded per comment. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a pull request has many review comments and each one needs an explicit recorded decision before the change can be merged.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for review comment resolution planning work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the review comment resolution planning steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def plan(comments):
    out = []
    for c in comments:
        decision = "accept" if c["actionable"] else "defer"
        out.append({"id": c["id"], "decision": decision, "reason": c.get("reason", "")})
    return out

comments = [{"id": 1, "actionable": True}, {"id": 2, "actionable": False, "reason": "style"}]
assert plan(comments)[0]["decision"] == "accept"
assert plan(comments)[1]["decision"] == "defer"
```

## Failure Modes
- Marking threads resolved without a recorded decision.
- Batch-accepting all comments without reading them.
- Losing rejected comments because they are deleted.
- No mapping from comment to the commit that answers it.
- Deferring indefinitely without an owner.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Scaling review-comment triage is a recurring 2026 developer workflow request in public discussion; this is a dated signal, not an adoption metric.

## Related
- code-review.md
- bug-fixing.md
- requirement-tracing.md
