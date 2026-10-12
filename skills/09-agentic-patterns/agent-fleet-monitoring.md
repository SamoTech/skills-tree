---
title: "Agent Fleet Monitoring"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Monitor a fleet of running agents with health, cost, and task-progress signals, and alert on stall, runaway cost, or repeated failure."
added: "2026-10"
version: v1
related: [logging-observability, agent-observability-tracing, budget-management]
tags: [agent, fleet, monitoring, agentic]
---

# Agent Fleet Monitoring

## Description
Monitor a fleet of running agents with health, cost, and task-progress signals, and alert on stall, runaway cost, or repeated failure. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agent fleet monitoring. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent fleet monitoring steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Agent Fleet Monitoring: deterministic check
candidates = [{"id": "a", "score": 0.8, "cost": 2}, {"id": "b", "score": 0.95, "cost": 9}]
eligible = [c for c in candidates if c["score"] >= 0.8]
selected = min(eligible, key=lambda c: c["cost"])
assert selected["id"] == "a"
print("selected:", selected["id"])
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
Production multi-agent operation is a 2026 theme; fleet monitoring recurs in published agent-ops guidance. These are dated public signals, not adoption metrics.

## Related
- logging-observability.md
- agent-observability-tracing.md
- budget-management.md
