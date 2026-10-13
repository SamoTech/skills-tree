---
name: agent-reputation-scoring
description: Score and rank peer agents from recorded task outcomes so delegation and routing decisions use measured reliability rather than claims.
metadata:
  source: skills/09-agentic-patterns/agent-reputation-scoring.md
  category: 09-agentic-patterns
  version: "v1"
---

# Agent Reputation Scoring

## Description
Score and rank peer agents from recorded task outcomes so delegation and routing decisions use measured reliability rather than claims. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- delegation choices among peer agents must be based on recorded outcomes.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agent reputation scoring work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent reputation scoring steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def score(history, window=10):
    recent = history[-window:]
    if not recent:
        return 0.0
    return sum(recent) / len(recent)

assert score([1, 1, 0, 1]) == 0.75
assert score([]) == 0.0
assert score([0] * 20 + [1]) == 0.1
```

## Failure Modes
- Ranking peers on self-reported success rates.
- Ignoring task-type match when comparing scores.
- Letting one noisy failure dominate a long history without weighting.
- Never expiring stale reputation evidence.
- Routing to a peer with no recorded outcomes.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
A2A multi-agent deployment questions in 2026 repeatedly ask how to judge peer reliability before handoff; this is a dated signal, not an adoption metric.

## Related
- agent-handoffs.md
- agent-fleet-monitoring.md
- subagent-delegation.md
