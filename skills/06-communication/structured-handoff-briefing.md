---
title: "Structured Handoff Briefing"
category: 06-communication
level: advanced
stability: experimental
description: "Write handoff briefings in a fixed structure covering state, open risks, decisions made, and next actions so a receiver can continue without rework."
added: "2026-10"
version: v1
related: [meeting-notes, stakeholder-status-updates, structured-output]
tags: [handoff, briefing, process]
---

# Structured Handoff Briefing

## Description
Write handoff briefings in a fixed structure covering state, open risks, decisions made, and next actions so a receiver can continue without rework. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- work is transferred between people or agents and the receiver must continue without losing context.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for structured handoff briefing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the structured handoff briefing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def briefing(state, risks, actions):
    required = {"state", "risks", "actions"}
    doc = {"state": state, "risks": risks, "actions": actions}
    missing = required - set(doc)
    if missing:
        raise ValueError("incomplete briefing: " + ",".join(sorted(missing)))
    return doc

b = briefing("deploying", ["db lag"], ["verify alerts"])
assert b["actions"] == ["verify alerts"]
try:
    briefing(None, [], [])
    raise AssertionError("should have raised")
except ValueError:
    print("structure held")
```

## Failure Modes
- Writing narrative prose with no fixed sections.
- Omitting decisions already made so they get relitigated.
- Leaving next actions without owners.
- Handing off without stating what is blocked and why.
- No pointer to the artifacts the receiver needs.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Structured human-agent handoffs are a recurring 2026 workflow request in public coverage; this is a dated signal, not an adoption metric.

## Related
- meeting-notes.md
- stakeholder-status-updates.md
- structured-output.md
