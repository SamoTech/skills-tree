---
name: simulated-user-evaluation
description: Evaluate a conversational agent against scripted simulated users with recorded goals so dialogue regressions are caught before deployment.
metadata:
  source: skills/09-agentic-patterns/simulated-user-evaluation.md
  category: 09-agentic-patterns
  version: "v1"
---

# Simulated User Evaluation

## Description
Evaluate a conversational agent against scripted simulated users with recorded goals so dialogue regressions are caught before deployment. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a dialogue agent needs repeatable multi-turn testing without live users.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for simulated user evaluation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the simulated user evaluation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def simulate(script, agent_reply):
    goal_met = script['goal'] in agent_reply
    return {'persona': script['persona'], 'goal_met': goal_met}

r = simulate({'persona': 'new-user', 'goal': 'refund'}, 'here is your refund')
assert r['goal_met'] and r['persona'] == 'new-user'
```

## Failure Modes
- One simulated persona standing in for the whole user base.
- Scripts that leak the expected answer to the agent under test.
- No record of which script a failure traces to.
- Passing a run while the simulated user goal was never achieved.
- Never updating scripts after real-user failures.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Persona-based simulated-user testing recurs in 2026 agent evaluation tooling; this is a dated signal, not an adoption metric.

## Related
- agent-eval-harness-design.md
- agent-regression-testing.md
- critic-agent.md
