---
name: skill-composition-chaining
description: Chain multiple existing skills into a composed workflow with explicit handoffs, preconditions, and rollback points instead of one monolithic procedure.
metadata:
  source: skills/09-agentic-patterns/skill-composition-chaining.md
  category: 09-agentic-patterns
  version: "v1"
---

# Skill Composition Chaining

## Description
Chain multiple existing skills into a composed workflow with explicit handoffs, preconditions, and rollback points instead of one monolithic procedure. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a task needs several existing skills in sequence and a failure mid-chain must leave a recoverable state.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for skill composition chaining work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the skill composition chaining steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def run_chain(steps, state):
    log = []
    for name, step in steps:
        state = step(state)
        log.append(name)
        if state is None:
            raise ValueError('step %s produced invalid state' % name)
    return state, log

state, log = run_chain([('load', lambda s: s + [1]), ('save', lambda s: s + [2])], [])
assert log == ['load', 'save'] and state == [1, 2]
```

## Failure Modes
- Chaining skills whose preconditions were never checked at handoff.
- Hiding intermediate failures so later skills consume garbage.
- Composing without a shared result schema between steps.
- No rollback point, leaving partial state on failure.
- Hard-coding an order that a precondition analysis contradicts.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Composing packaged Agent Skills into larger workflows is a recurring 2026 ecosystem request; this is a dated signal, not an adoption metric.

## Related
- skill-gap-detection.md
- skill-quality-evaluation.md
- agent-handoffs.md
