---
name: stream-processing
description: Process unbounded event streams with windowed aggregation, watermarking, and exactly-once handling, keeping results correct under late arrival, replay, and backpressure.
metadata:
  source: skills/12-data/stream-processing.md
  category: 12-data
  version: "v1"
---

# Stream Processing

Category: Data | Level: advanced | Stability: experimental | Version: v1

## Description

Stream processing computes over data that never stops arriving. The skill covers partitioning by key, defining windows with explicit late-arrival policy, advancing watermarks to bound results, emitting windowed aggregates, and handling replay and failure through idempotent sinks. Correctness comes from declared semantics: at-least-once delivery with idempotent writes, or exactly-once where the engine supports transactional state.

## When to Use

Use when events must be aggregated, joined, or alerted on as they arrive rather than in batch: telemetry, click streams, sensor feeds, or transaction flows.

Do not treat an unbounded stream as if it were a growing table. Without windows and watermarks, results never finalize and memory grows without bound.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `stream` | `object` | Yes | Partitioned, append-only event source with per-key ordering |
| `window_spec` | `object` | Yes | Window type, size, allowed lateness, and watermark policy |
| `sink` | `object` | Yes | Idempotent or transactional output destination |

## Procedure

1. Declare delivery semantics first: at-least-once with idempotent sinks, or exactly-once with transactional state.
2. Partition by key so per-key ordering holds; record the partitioner choice.
3. Define windows with an explicit type, size, and allowed lateness; never use defaults silently.
4. Advance watermarks from event time and emit window results when the watermark closes the window.
5. Handle late events per policy: update the result if the sink allows, or route them to a side output.
6. On failure, restore state from the checkpoint and replay from the committed offset, proving no double emission.

## Outputs

| Output | Type | Description |
|---|---|---|
| `window_results` | `table` | Closed-window aggregates with event-time bounds |
| `late_events` | `array` | Events that missed their window, routed to a side output |
| `watermark_log` | `list` | Watermark progression used to close each window |

## Runnable Example

```python
def close_windows(events, max_lateness):
    """events: [(event_time, value)] in arrival order"""
    watermarks = []
    closed = []
    for t, _ in events:
        wm = t - max_lateness
        watermarks.append(wm)
    seen_windows = {}
    for t, v in events:
        window = (t // 10) * 10
        seen_windows.setdefault(window, []).append(v)
    final_wm = max(watermarks)
    for window, values in sorted(seen_windows.items()):
        if window + 10 <= final_wm:
            closed.append({"window": window, "sum": sum(values)})
    return {"closed": closed, "watermark": final_wm}

print(close_windows([(1, 1.0), (7, 2.0), (15, 3.0), (25, 4.0)], max_lateness=5))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Window never closes | Watermark stalls on sparse partitions | Idle-source watermarks or wall-clock fallback |
| Late events lost or double-counted | Replay without idempotent sink | Idempotent writes keyed by window and offset |
| Unbounded state growth | Keys accumulate without retention | Set state TTL sized to the window policy |
| Skew stalls the pipeline | One hot key dominates a partition | Key salting or pre-aggregation before partitioning |
| Event-time vs processing-time confusion | Late data read as anomalies | Carry event time end to end and watermark on it |

## Security and Authority Boundary

Streams often carry personal or operational data at high velocity. Scope access at the topic or partition level, avoid enriching events with unrelated lookups mid-stream, and make sinks tamper-evident because stream outputs frequently drive automated decisions.

## Evidence

This skill is grounded in dated public implementation references:

1. The Apache Kafka documentation covering consumer semantics and delivery guarantees (https://kafka.apache.org/documentation/).
2. The Apache Flink documentation on event time and watermarks (https://nightlies.apache.org/flink/flink-docs-stable/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [ETL Pipeline](etl-pipeline.md) — the batch counterpart for data that does not need sub-daily latency.
- [Anomaly Detection](anomaly-detection.md) — the downstream decision layer that consumes windowed stream features.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
