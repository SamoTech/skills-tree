---
title: "Metrics Cardinality Management"
category: 12-data
level: advanced
stability: experimental
description: "Control metrics label cardinality with budgets, top-label tracking, and rejection rules so dashboards stay queryable and cheap."
added: "2026-10"
version: v1
related: [data-pipeline-observability, query-optimization, anomaly-detection]
tags: [metrics, cardinality, observability]
---

# Metrics Cardinality Management

## Description
Control metrics label cardinality with budgets, top-label tracking, and rejection rules so dashboards stay queryable and cheap. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- metric label growth must be bounded before dashboards degrade.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for metrics cardinality management work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the metrics cardinality management steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def admit_labels(new, current, budget):
    would = current | set(new)
    return len(would) <= budget, len(would)

ok, size = admit_labels(['a', 'b'], {'a', 'z'}, 3)
assert ok and size == 3
ok2, size2 = admit_labels(['b', 'c'], {'a', 'z'}, 3)
assert not ok2 and size2 == 4
```

## Failure Modes
- Unbounded user or request IDs flowing into labels.
- Discovering cardinality blowup only when queries time out.
- No budget per metric family.
- Silently dropping labels without recording what was rejected.
- Aggregating away labels the dashboards actually need.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Cardinality blowups recur in 2026 observability cost discussions; this is a dated signal, not an adoption metric.

## Related
- data-pipeline-observability.md
- query-optimization.md
- anomaly-detection.md
