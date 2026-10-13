---
title: "Escalation Memo Writing"
category: 06-communication
level: advanced
stability: experimental
description: "Write escalation memos that state the blocked decision, options considered, the decision needed, and a response deadline without emotional framing."
added: "2026-10"
version: v1
related: [incident-communication, report-writing, stakeholder-status-updates]
tags: [escalation, writing, decisions]
---

# Escalation Memo Writing

## Description
Write escalation memos that state the blocked decision, options considered, the decision needed, and a response deadline without emotional framing. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an issue is blocked above your authority and a decision memo must be sent upward.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for escalation memo writing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the escalation memo writing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def memo(blocked, options, needed_by):
    if not options:
        raise ValueError("memo must present at least one option")
    return {"decision": blocked, "options": options, "needed_by": needed_by}

m = memo("vendor choice", ["renew", "switch"], "Friday")
assert m["needed_by"] == "Friday" and len(m["options"]) == 2
```

## Failure Modes
- Escalating a problem with no proposed options.
- Missing a response deadline so it is ignored.
- Blaming individuals instead of stating the blocker.
- Hiding the risk of the do-nothing option.
- Escalating everything so urgency loses meaning.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Decision escalation hygiene is a recurring 2026 organizational communication topic in public coverage; this is a dated signal, not an adoption metric.

## Related
- incident-communication.md
- report-writing.md
- stakeholder-status-updates.md
