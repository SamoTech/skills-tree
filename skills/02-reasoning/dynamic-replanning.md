---
title: "Dynamic Replanning"
category: 02-reasoning
level: advanced
stability: experimental
description: "Detect when execution has diverged from the plan, decide between replanning and continuing with recorded criteria, and preserve completed work during replanning."
added: "2026-10"
version: v1
related: [self-correction, planning, react]
tags: [replanning, agents, execution]
---

# Dynamic Replanning

## Description
Detect when execution has diverged from the plan, decide between replanning and continuing with recorded criteria, and preserve completed work during replanning. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- execution feedback shows the current plan is no longer valid before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for dynamic replanning work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the dynamic replanning steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def should_replan(divergence, threshold=0.5):
    return divergence >= threshold

def preserved(completed, new_plan):
    return [s for s in new_plan if s in completed]

assert should_replan(0.7) is True and should_replan(0.2) is False
assert preserved(["a", "b"], ["b", "c"]) == ["b"]
```

## Failure Modes
- Replanning away completed and verified work.
- Replanning on noise rather than real divergence.
- Flapping between two plans.
- Replanning without recording the divergence evidence.
- Continuing past a divergence that invalidates the goal.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Replanning under feedback is a recurring 2026 long-running-agent concern in public coverage; this is a dated signal, not an adoption metric.

## Related
- self-correction.md
- planning.md
- react.md
