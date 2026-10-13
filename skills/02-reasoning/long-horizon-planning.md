---
title: "Long-Horizon Planning"
category: 02-reasoning
level: advanced
stability: experimental
description: "Structure plans spanning many steps or long durations with staged checkpoints, milestone verification, and re-planning triggers as conditions change."
added: "2026-10"
version: v1
related: [multi-step-planning, planning, scenario-planning]
tags: [planning, long-horizon, agents]
---

# Long-Horizon Planning

## Description
Structure plans spanning many steps or long durations with staged checkpoints, milestone verification, and re-planning triggers as conditions change. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a task spans dozens of steps or long durations and needs staged verification before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for long horizon planning work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the long horizon planning steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def next_milestone(progress, milestones):
    for m in milestones:
        if progress < m:
            return m
    return None

assert next_milestone(2, [3, 6, 9]) == 3
assert next_milestone(9, [3, 6, 9]) is None

def replan_needed(verified, expected):
    return verified != expected

assert replan_needed(True, False) is True
```

## Failure Modes
- Planning every detail up front and never revisiting.
- Missing checkpoint evidence that a milestone is real.
- Continuing on stale plans after the environment changed.
- Treating elapsed time as progress.
- Planning horizons beyond reliable information.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Long-horizon autonomous agents are a dominant 2026 agentic-AI theme in public coverage; this is a dated signal, not an adoption metric.

## Related
- multi-step-planning.md
- planning.md
- scenario-planning.md
