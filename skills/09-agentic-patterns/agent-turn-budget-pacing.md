---
title: "Agent Turn Budget Pacing"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Pace an agent turn budget against milestones so early over-spending is caught and corrected before the budget is exhausted."
added: "2026-10"
version: v1
related: [agent-cost-accounting, agent-halt-conditions, plan-and-execute]
tags: [budget, pacing, planning]
---

# Agent Turn Budget Pacing

## Description
Pace an agent turn budget against milestones so early over-spending is caught and corrected before the budget is exhausted. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a run has a fixed turn or time budget and progress must stay proportional to spend.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agent turn budget pacing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent turn budget pacing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def pacing_action(turns_used, budget, milestones_done, milestones_total):
    if turns_used >= budget:
        return 'halt'
    if milestones_total and milestones_done / milestones_total < turns_used / budget:
        return 'compress'
    return 'continue'

assert pacing_action(80, 100, 1, 4) == 'compress'
assert pacing_action(20, 100, 2, 4) == 'continue'
```

## Failure Modes
- Discovering budget exhaustion only at the final turn.
- Spending most turns on the first sub-goal.
- Not recording per-milestone turn cost for future pacing.
- Ignoring wall-clock limits that bind tighter than turns.
- Pacing on averages instead of per-milestone baselines.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Deadline-aware and budget-aware reasoning is a recurring 2026 agent-framework request; this is a dated signal, not an adoption metric.

## Related
- agent-cost-accounting.md
- agent-halt-conditions.md
- plan-and-execute.md
