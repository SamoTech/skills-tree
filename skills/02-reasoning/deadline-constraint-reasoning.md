---
title: "Deadline Constraint Reasoning"
category: 02-reasoning
level: advanced
stability: experimental
description: "Reason about task feasibility and ordering under explicit deadlines, propagate due dates through dependencies, and report infeasible schedules instead of silently dropping constraints."
added: "2026-10"
version: v1
related: [temporal-reasoning, constraint-satisfaction, multi-step-planning]
tags: [scheduling, constraints, planning]
---

# Deadline Constraint Reasoning

## Description
Reason about task feasibility and ordering under explicit deadlines, propagate due dates through dependencies, and report infeasible schedules instead of silently dropping constraints. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- work must be sequenced under real due dates and feasibility must be provable before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for deadline constraint reasoning work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the deadline constraint reasoning steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def latest_start(tasks):
    # tasks: list of (name, duration, dependency_latest_finish)
    plan = {}
    for name, dur, dep_lf in tasks:
        ls = dep_lf - dur
        if ls < 0:
            return None, "infeasible %s" % name
        plan[name] = ls
    return plan, "ok"

plan, status = latest_start([("a", 2, 10), ("b", 3, plan_a := 10)])
assert status == "ok"
assert plan["b"] == 7
_, status2 = latest_start([("a", 2, 1)])
assert status2.startswith("infeasible")
```

## Failure Modes
- Dropping a deadline to make the schedule feasible.
- Ignoring dependency chains when propagating due dates.
- Treating soft targets as hard deadlines without confirmation.
- Hiding infeasibility behind optimistic duration estimates.
- Forgetting calendar holidays and working-hour windows.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Deadline-aware orchestration is a recurring 2026 agent-workflow request in public developer discussion; this is a dated signal, not an adoption metric.

## Related
- temporal-reasoning.md
- constraint-satisfaction.md
- multi-step-planning.md
