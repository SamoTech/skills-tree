---
name: bottleneck-analysis
description: Locate the constraint that bounds a pipeline or workflow, quantify its capacity relative to demand, and prioritize interventions by measured effect rather than intuition.
metadata:
  source: skills/02-reasoning/bottleneck-analysis.md
  category: 02-reasoning
  version: "v1"
---

# Bottleneck Analysis

## Description
Locate the constraint that bounds a pipeline or workflow, quantify its capacity relative to demand, and prioritize interventions by measured effect rather than intuition. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a workflow is slower than needed and the true constraint must be identified before tuning before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for bottleneck analysis work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the bottleneck analysis steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def bottleneck(stations):
    rates = [s["rate"] for s in stations]
    idx = rates.index(min(rates))
    return stations[idx]["name"], min(rates)

stations = [{"name": "fetch", "rate": 50}, {"name": "parse", "rate": 10}, {"name": "rank", "rate": 40}]
name, rate = bottleneck(stations)
assert name == "parse" and rate == 10
```

## Failure Modes
- Optimizing a stage that is not the constraint.
- Measuring throughput without demand context.
- Confusing latency of one stage with system capacity.
- Fixing a bottleneck and ignoring the next constraint.
- Using stale measurements after a topology change.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Agent pipeline performance tuning is a recurring 2026 operations request signal in public coverage; this is a dated signal, not an adoption metric.

## Related
- systems-thinking.md
- sensitivity-analysis.md
- root-cause-analysis.md
