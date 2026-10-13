---
title: "Migration Communication Writing"
category: 06-communication
level: advanced
stability: experimental
description: "Write migration communications that state what changes, who is affected, when, what action is required, and where to get help."
added: "2026-10"
version: v1
related: [changelog-writing, release-notes-generation, onboarding-guide-writing]
tags: [migration, writing, change-management]
---

# Migration Communication Writing

## Description
Write migration communications that state what changes, who is affected, when, what action is required, and where to get help. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a system migration affects many users and each message must be explicit about required actions.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for migration communication writing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the migration communication writing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def message(audience, change, action, when):
    missing = [k for k, v in {"audience": audience, "change": change, "action": action, "when": when}.items() if not v]
    if missing:
        raise ValueError("missing: " + ",".join(missing))
    return f"{audience}: {change}. Action: {action} by {when}."

assert "Action: opt in" in message("users", "new login", "opt in", "May 1")
```

## Failure Modes
- Announcing the change without the required action.
- One message for all audiences with different duties.
- No date or a vague timeline.
- No support channel named in the message.
- Sending the notice only after the migration ran.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Migration and deprecation communication is a recurring 2026 platform engineering topic in public discussion; this is a dated signal, not an adoption metric.

## Related
- changelog-writing.md
- release-notes-generation.md
- onboarding-guide-writing.md
