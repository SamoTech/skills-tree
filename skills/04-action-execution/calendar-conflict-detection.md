---
title: "Calendar Conflict Detection"
category: 04-action-execution
level: intermediate
stability: experimental
description: "Check proposed calendar changes against existing events for overlaps and constraints, and propose concrete alternatives rather than silently double-booking."
added: "2026-10"
version: v1
related: [calendar-event, scheduled-execution, deadline-propagation]
tags: [calendar, conflict, detection, action]
---

# Calendar Conflict Detection

## Description
Check proposed calendar changes against existing events for overlaps and constraints, and propose concrete alternatives rather than silently double-booking. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires calendar conflict detection before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for calendar conflict detection. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the calendar conflict detection steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Calendar Conflict Detection: deterministic check
seen = {}
conflicts = []
for item in [{"k": "a", "v": 1}, {"k": "a", "v": 2}, {"k": "b", "v": 3}]:
    if item["k"] in seen and seen[item["k"]] != item["v"]:
        conflicts.append(item["k"])
    seen[item["k"]] = item["v"]
assert conflicts == ["a"]
print("conflicts:", conflicts)
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Scheduling agents are a common 2026 deployment; conflict handling recurs in public integration threads. These are dated public signals, not adoption metrics.

## Related
- calendar-event.md
- scheduled-execution.md
- deadline-propagation.md
