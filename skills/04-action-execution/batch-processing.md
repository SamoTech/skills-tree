---
title: "Batch Processing"
category: 04-action-execution
level: intermediate
stability: experimental
description: "Execute many homogeneous operations as a bounded batch — chunking, per-item status, partial-failure handling, and resumable checkpoints — instead of a fragile loop."
added: "2026-10"
version: v1
related: ["database-write", "api-call"]
---

# Batch Processing

Category: Action Execution | Level: intermediate | Stability: experimental | Version: v1

## Description

Bulk work fails in ways single operations do not: item four thousand of ten thousand errors, the connection drops at sixty percent, and a naive loop either stops the world or loses track of what happened. This skill structures bulk execution as bounded chunks with per-item status, so any run can resume from where it stopped and report exactly which items succeeded, failed, or were skipped.

## When to Use

Use when the same operation applies to many items — bulk API calls, mass file transforms, database migrations — and partial failure is expected rather than exceptional.

Do not run unbounded batches: without chunking and checkpoints, a bulk run is a single point of failure for the whole set.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `items` | `list` | Yes | The full item set to process |
| `operation` | `callable` | Yes | The operation applied to each item |
| `chunk` | `map` | No | Batch size and checkpoint interval |

## Procedure

1. Persist the item manifest before starting so progress survives interruption and is auditable afterwards.
2. Chunk the work: process bounded batches, not the full set in one unbounded pass.
3. Record per-item status — pending, succeeded, failed, skipped — with the error attached at failure time.
4. On interruption, resume from the last checkpoint by reading the manifest, not by re-deriving what was done.
5. Apply a failure budget: stop the batch when the failure rate crosses a stated bound instead of processing the full set into a known-bad state.
6. Reconcile at the end: counts of succeeded, failed, and skipped must sum to the manifest size.

## Outputs

| Output | Type | Description |
|---|---|---|
| `manifest` | `map` | Per-item status for the full set |
| `summary` | `map` | Counts by status plus timing per chunk |
| `resume` | `map` | Checkpoint state for resuming an interrupted run |

## Runnable Example

```python
def run_batch(items, operation, chunk_size=2, max_failures=1):
    status = {item["id"]: "pending" for item in items}
    failures = 0
    for start in range(0, len(items), chunk_size):
        for item in items[start:start + chunk_size]:
            try:
                operation(item)
                status[item["id"]] = "succeeded"
            except Exception as err:
                status[item["id"]] = f"failed: {err}"
                failures += 1
        if failures > max_failures:
            break
    return status

def double(item):
    if item["value"] == 3:
        raise ValueError("corrupt row")
    return item["value"] * 2

items = [{"id": f"row-{n}", "value": n} for n in range(5)]
print(run_batch(items, double))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| All-or-nothing stop | One failure halts the whole set | Record per-item status and continue within the failure budget |
| Lost progress | An interrupted run restarts from zero | Checkpoint against a persisted manifest |
| Unbounded chunks | The full set is processed in one pass | Chunk into bounded batches |
| Silent skips | Skipped items are never reported | Count and list skips in the summary |
| Count mismatch | Statuses do not sum to the manifest | Reconcile at run end |

## Security and Authority Boundary

Batch operations concentrate access — bulk reads and writes move data at a scale that interactive use never touches. Scope credentials to the batch job, log the manifest rather than the payloads, and do not let bulk jobs bypass per-item authorization checks.

## Evidence

This skill is grounded in dated public implementation references:

1. The Apache Kafka documentation on producer batching and consumer group mechanics (https://kafka.apache.org/documentation/).
2. Wikipedia's overview of stream processing, where bounded chunks are the unit of work (https://en.wikipedia.org/wiki/Stream_processing).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Database Write](database-write.md) — the write path that bulk operations stress.
- [API Call](api-call.md) — the network operation typically throttled in bulk.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
