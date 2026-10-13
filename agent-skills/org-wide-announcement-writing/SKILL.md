---
name: org-wide-announcement-writing
description: Write organization-wide announcements with a single headline change, affected groups, required actions, and a question channel routed to owners.
metadata:
  source: skills/06-communication/org-wide-announcement-writing.md
  category: 06-communication
  version: "v1"
---

# Org Wide Announcement Writing

## Description
Write organization-wide announcements with a single headline change, affected groups, required actions, and a question channel routed to owners. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an announcement goes to the whole organization and must be unambiguous for every audience.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for org wide announcement writing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the org wide announcement writing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def route(section, owners):
    if section == "questions" and "owner" not in owners:
        raise ValueError("question channel needs an owner")
    return True

assert route("questions", {"owner": "team-a"}) is True
```

## Failure Modes
- Multiple unrelated changes buried in one message.
- No channel for follow-up questions.
- Jargon that only one team understands.
- Announcing before the change is actually live.
- No plain statement of who must act.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Clear org-wide messaging is a recurring 2026 internal-comms request in public discussion; this is a dated signal, not an adoption metric.

## Related
- audience-analysis.md
- faq-generation.md
- tone-adjustment.md
