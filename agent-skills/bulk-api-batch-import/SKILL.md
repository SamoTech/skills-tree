---
name: bulk-api-batch-import
description: Import large record sets through batch APIs with chunk sizing, per-record error capture, and resumable checkpoints so a failed run restarts without duplicating writes.
metadata:
  source: skills/04-action-execution/bulk-api-batch-import.md
  category: 04-action-execution
  version: "v1"
---

# Bulk API Batch Import

## Description
Import large record sets through batch APIs with chunk sizing, per-record error capture, and resumable checkpoints so a failed run restarts without duplicating writes. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- thousands of records must be imported through a rate-limited batch API before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for bulk api batch import work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the bulk api batch import steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def chunk(records, size):
    return [records[i:i+size] for i in range(0, len(records), size)]

def resume_from(checkpoints, batches):
    done = sum(checkpoints)
    return batches[done:]

records = list(range(25))
batches = chunk(records, 10)
assert len(batches) == 3 and len(batches[0]) == 10
assert resume_from([1, 1, 0], batches) == [batches[2]]
```

## Failure Modes
- Resuming without a checkpoint and duplicating earlier batches.
- Swallowing per-record errors into a single failure.
- Choosing chunk sizes that trip provider limits.
- Treating a partial batch as fully imported.
- No idempotency on individual record writes.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Bulk ingestion through provider APIs is a recurring 2026 integration request for agent workflows; this is a dated signal, not an adoption metric.

## Related
- batch-processing.md
- api-call.md
- action-result-verification.md
