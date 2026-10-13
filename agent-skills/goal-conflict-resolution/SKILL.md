---
name: goal-conflict-resolution
description: Detect competing goals, rank them with explicit criteria and stakeholder input where available, and document the resolution rationale instead of merging incompatible goals.
metadata:
  source: skills/02-reasoning/goal-conflict-resolution.md
  category: 02-reasoning
  version: "v1"
---

# Goal Conflict Resolution

## Description
Detect competing goals, rank them with explicit criteria and stakeholder input where available, and document the resolution rationale instead of merging incompatible goals. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- two active goals cannot both be satisfied and the conflict must be surfaced before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for goal conflict resolution work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the goal conflict resolution steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def detect_conflict(goals, interference):
    conflicts = []
    for a, b in interference:
        if goals.get(a, False) and goals.get(b, False):
            conflicts.append((a, b))
    return conflicts

goals = {"privacy": True, "personalization": True, "speed": True}
interference = [("privacy", "personalization"), ("speed", "privacy")]
assert detect_conflict(goals, interference) == [("privacy", "personalization"), ("speed", "privacy")]
```

## Failure Modes
- Merging incompatible goals into a vague compromise.
- Resolving conflicts without recording the rationale.
- Assuming the loudest stakeholder defines priority.
- Missing latent conflicts between downstream goals.
- Treating one resolution as permanent when context changes.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Multi-goal agent behavior is a recurring 2026 alignment concern in public coverage; this is a dated signal, not an adoption metric.

## Related
- multi-objective-optimization.md
- prioritization.md
- decision-making.md
