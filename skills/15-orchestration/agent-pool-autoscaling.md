---
title: "Agent Pool Autoscaling"
category: 15-orchestration
level: advanced
stability: experimental
description: "Autoscale pools of worker agents on queue depth and per-agent cost with warm capacity and scale-in hysteresis."
added: "2026-10"
version: v1
related: [dynamic-replanning, resource-allocation, inference-endpoint-autoscaling]
tags: [agent, pool, autoscaling]
---
# Agent Pool Autoscaling

## Description
Autoscale pools of worker agents on queue depth and per-agent cost with warm capacity and scale-in hysteresis. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires agent pool autoscaling before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agent pool autoscaling. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent pool autoscaling steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def scale(queue_depth, per_agent, floor, ceiling):
    want = max(floor, min(ceiling, -(-queue_depth // per_agent)))
    return want
assert scale(25, 10, 1, 3) == 3
assert scale(0, 10, 1, 3) == 1
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
Agent pool scaling on queue depth is requested for production multi-agent fleets in 2026. These are dated public signals, not adoption metrics.

## Related
- dynamic-replanning.md
- resource-allocation.md
- inference-endpoint-autoscaling.md
