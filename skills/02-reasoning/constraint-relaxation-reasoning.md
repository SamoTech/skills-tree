---
title: "Constraint Relaxation Reasoning"
category: 02-reasoning
level: advanced
stability: experimental
description: "Determine which constraints to relax when a problem is infeasible, relax the minimum set with recorded justification, and re-check that remaining constraints still hold."
added: "2026-10"
version: v1
related: [constraint-satisfaction, satisficing-decision-making, problem-decomposition]
tags: [constraints, planning, reasoning]
---

# Constraint Relaxation Reasoning

## Description
Determine which constraints to relax when a problem is infeasible, relax the minimum set with recorded justification, and re-check that remaining constraints still hold. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an infeasible problem must be made feasible by explicit, minimal relaxation before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for constraint relaxation reasoning work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the constraint relaxation reasoning steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def relax(order, constraints):
    for c in order:
        constraints = {k: v for k, v in constraints.items() if k != c}
        if feasible(constraints):
            return c, constraints
    return None, constraints

def feasible(c): return c.get("budget", 0) > 0 and "deadline" not in c
relaxed, rest = relax(["deadline", "budget"], {"deadline": "today", "budget": 5})
assert relaxed == "deadline" and rest == {"budget": 5}
```

## Failure Modes
- Relaxing constraints before proving infeasibility.
- Relaxing more than the minimum set.
- Relaxing safety or security constraints.
- Losing the justification record for later review.
- Failing to re-check remaining constraints after relaxation.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Over-constrained task negotiation is a recurring 2026 agent-planning topic in public discussion; this is a dated signal, not an adoption metric.

## Related
- constraint-satisfaction.md
- satisficing-decision-making.md
- problem-decomposition.md
