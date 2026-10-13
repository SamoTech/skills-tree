---
name: parquet-processing
description: Read, write, and validate Parquet datasets with schema checks, column pruning, and row-group statistics instead of full scans.
metadata:
  source: skills/12-data/parquet-processing.md
  category: 12-data
  version: "v1"
---

# Parquet Processing

## Description
Read, write, and validate Parquet datasets with schema checks, column pruning, and row-group statistics instead of full scans. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- large columnar datasets must be processed without full scans.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for parquet processing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the parquet processing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def prune_columns(schema, wanted):
    unknown = [c for c in wanted if c not in schema]
    if unknown:
        raise ValueError('unknown columns %s' % unknown)
    return wanted

schema = {'id', 'ts', 'user', 'amount'}
assert prune_columns(schema, ['id', 'amount']) == ['id', 'amount']
```

## Failure Modes
- Reading all columns when two would answer the query.
- Writing files whose schema differs from the declared contract.
- Ignoring row-group statistics that could skip scans.
- Assuming row order in a format that does not promise it.
- Mixing compression codecs across a dataset silently.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Parquet-aware processing with column pruning recurs in 2026 data-engineering requests; this is a dated signal, not an adoption metric.

## Related
- csv-processing.md
- etl-pipeline.md
- schema-inference.md
