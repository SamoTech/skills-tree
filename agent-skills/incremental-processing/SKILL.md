---
name: incremental-processing
description: Process new data as it arrives instead of reprocessing the whole corpus — checkpoints, watermarks, and late-arrival handling — so cost stays flat as history grows.
metadata:
  source: skills/12-data/incremental-processing.md
  category: 12-data
  version: "v1"
---

# Incremental Processing

Category: Data | Level: intermediate | Stability: experimental | Version: v1

## Description

A pipeline that recomputes everything on every run is a pipeline with a half-life: the corpus grows, the run lengthens, and the day arrives where the run no longer fits between the arrivals. This skill switches the unit of work from the dataset to the delta: the process tracks what it has already consumed, takes only the new records past that mark, and handles the stragglers — late, out-of-order, or corrected records — by explicit rule rather than by accident.

## When to Use

Use when data arrives continuously or the corpus is large enough that full recomputation no longer fits its window — event streams, append-only logs, growing tables.

Do not add incremental machinery to small, fully recomputable datasets; a full pass over a small table is simpler, idempotent by construction, and easier to reason about.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `source` | `stream` | Yes | The arriving data with an ordering or event time |
| `checkpoint` | `record` | Yes | The consumed position the run resumes from |
| `late_policy` | `enum` | Yes | Window wait, watermark, or drop for late arrivals |

## Procedure

1. Pick the position marker — an offset, a timestamp, or a sequence column — that strictly advances as new data arrives.
2. Persist a checkpoint after each processed unit, and make downstream updates idempotent so a replay from the checkpoint is safe.
3. Process only records past the checkpoint, committing the new checkpoint only after the unit is durably processed.
4. Handle late arrivals by rule: bounded wait behind a watermark, correction events, or explicit drop — never by silent overwrite.
5. Measure lag — arrival time to processed time — and alarm when the checkpoint stops advancing, because a stalled marker is the failure mode.
6. Periodically reconcile the incremental result against a full recomputation, so drift between the two is caught at a known cost.

## Outputs

| Output | Type | Description |
|---|---|---|
| `processed` | `list` | Records consumed since the previous checkpoint |
| `checkpoint` | `record` | The new resume position, durable after commit |
| `lag` | `map` | Arrival-to-processed delay and stall detection |

## Runnable Example

```python
def process_incremental(events, consumed_offset):
    new_events = [e for e in events if e["offset"] > consumed_offset]
    if not new_events:
        return consumed_offset, []
    new_offset = max(e["offset"] for e in new_events)
    return new_offset, new_events

events = [
    {"offset": 1, "kind": "click"},
    {"offset": 2, "kind": "click"},
    {"offset": 3, "kind": "order"},
]
offset, batch = process_incremental(events, consumed_offset=1)
print("processed:", [e["kind"] for e in batch], "new offset:", offset)
offset2, batch2 = process_incremental(events, consumed_offset=offset)
print("second pass empty:", batch2 == [], "offset unchanged:", offset2 == offset)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Checkpoint stalls | The marker stops advancing and data piles up | Alarm on lag and on checkpoint age |
| Replay damage | Reprocessing a unit double-counts downstream | Make downstream updates idempotent per event |
| Late-arrival chaos | Out-of-order records dropped or duplicated silently | Apply an explicit watermark and late policy |
| Full-scan relapse | The incremental path quietly recomputing everything | Track processed volume per run |
| Unverified drift | Incremental result slowly diverges from truth | Reconcile periodically against a full recomputation |

## Security and Authority Boundary

Incremental state is attack surface: checkpoints record positions and the process holds partial aggregates, so both must inherit the access scope of the source data, and late-arrival or correction paths — which can rewrite aggregates — deserve the same authorization checks as the primary path.

## Evidence

This skill is grounded in dated public implementation references:

1. The Apache Kafka documentation (https://kafka.apache.org/documentation/).
2. Wikipedia's overview of stream processing (https://en.wikipedia.org/wiki/Stream_processing).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [ETL Pipeline](etl-pipeline.md) — the batch framework incremental runs extend.
- [Data Aggregation](data-aggregation.md) — the downstream aggregates watermarks bound.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
