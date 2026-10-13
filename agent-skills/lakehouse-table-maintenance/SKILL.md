---
name: lakehouse-table-maintenance
description: Maintain lakehouse tables with compaction, snapshot expiry, and orphan-file cleanup driven by measured metrics rather than a fixed schedule.
metadata:
  source: skills/12-data/lakehouse-table-maintenance.md
  category: 12-data
  version: "v1"
---

# Lakehouse Table Maintenance

## Description
Maintain lakehouse tables with compaction, snapshot expiry, and orphan-file cleanup driven by measured metrics rather than a fixed schedule. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- table health must be maintained before small files and snapshots degrade queries.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for lakehouse table maintenance work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the lakehouse table maintenance steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def maintenance_plan(small_files, threshold, snapshots, max_snapshots):
    actions = []
    if small_files > threshold:
        actions.append('compact')
    if snapshots > max_snapshots:
        actions.append('expire-snapshots')
    return actions

assert maintenance_plan(500, 100, 20, 10) == ['compact', 'expire-snapshots']
assert maintenance_plan(5, 100, 2, 10) == []
```

## Failure Modes
- Compacting on a calendar schedule instead of measured need.
- Expiring snapshots that time-travel queries still reference.
- Deleting files that later prove to be in-use but unreferenced.
- Running maintenance without a pre-action backup point.
- Not recording what maintenance actually improved.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Table maintenance driven by measured metrics appears in 2026 lakehouse operations requests; this is a dated signal, not an adoption metric.

## Related
- etl-pipeline.md
- incremental-processing.md
- query-optimization.md
