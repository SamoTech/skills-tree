---
title: "Backpressure Handling"
category: 15-orchestration
level: intermediate
stability: experimental
description: "Detect and shed or buffer load when downstream consumers fall behind, using explicit queue limits, load-shedding policies, and honest propagation instead of unbounded queues."
added: "2026-10"
version: v1
related: ["task-queue","deadline-propagation"]
---

# Backpressure Handling

Category: Orchestration | Level: intermediate | Stability: experimental | Version: v1

## Description

Backpressure is the system admitting it is saturated instead of hiding the lag in a growing queue. The skill covers measuring consumer lag against explicit thresholds, choosing the response per queue type: bounded buffers for bursty-but-must-complete work, immediate shedding for latency-sensitive work, and degradation for work that has cheaper fallbacks. Pressure is propagated to callers honestly, because a lie here becomes a timeout there.

## When to Use

Use when producers can outrun consumers: agent fleets, ingestion pipelines, or request handlers where queue growth is worse than refusal.

Do not respond to saturation with an unbounded queue. It converts a visible overload into an invisible one that eventually fails bigger and later.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `queue_metrics` | `table` | Yes | Depth, arrival rate, and consumption rate per queue |
| `policy` | `object` | Yes | Thresholds and the response per queue type: buffer, shed, or degrade |
| `fallbacks` | `object` | No | Degraded-mode responses available when shedding is undesirable |

## Procedure

1. Instrument every queue with depth and arrival and consumption rates before tuning anything.
2. Classify each queue: must-complete, latency-sensitive, or degradable.
3. Set explicit thresholds for each queue marking normal, pressured, and saturated states.
4. Respond by class: bounded buffer, immediate shed with a clear refusal, or degraded fallback.
5. Propagate pressure upstream honestly so callers can slow down instead of guessing.
6. Alert on sustained pressure, not transient bursts, and record shed decisions for review.

## Outputs

| Output | Type | Description |
|---|---|---|
| `pressure_state` | `object` | Per-queue state: normal, pressured, or saturated |
| `shed_log` | `table` | What was shed or degraded, with reasons |
| `propagation_events` | `list` | Signals sent upstream to slow producers |

## Runnable Example

```python
def classify_queue(depth, capacity, arrival, consumption, bursts_ok=3):
    """depth/current; rates per second"""
    if arrival <= consumption and depth < capacity * 0.5:
        return {"state": "normal"}
    if depth >= capacity:
        return {"state": "saturated", "action": "shed"}
    return {"state": "pressured", "action": "buffer"}

print(classify_queue(depth=20, capacity=100, arrival=5, consumption=6))
print(classify_queue(depth=100, capacity=100, arrival=9, consumption=4))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Invisible overload | Unbounded queues hide growing lag | Bound every queue and alarm on depth |
| Shedding the wrong work | Uniform drop policy sheds critical requests | Classify queues and shed per policy |
| Silent degradation | Fallbacks served without disclosure | Mark degraded responses so callers can react |
| Pressure not propagated | Producers keep full send rate | Propagate explicit slow-down signals upstream |
| Threshold thrash | Alarm flapping at the boundary | Hysteresis between pressured and normal states |

## Security and Authority Boundary

Load shedding changes what work a system accepts, which is a policy decision with user impact. Keep shed policies in configuration with review, log what is refused, and never shed security-relevant work such as audit events or authentication under load.

## Evidence

This skill is grounded in dated public implementation references:

1. The Apache Kafka documentation on consumer lag and flow control semantics (https://kafka.apache.org/documentation/).
2. The Project Reactor reactive library with bounded buffering (https://projectreactor.io/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Task Queue](task-queue.md) — the queue structure whose depth drives every pressure signal.
- [Deadline Propagation](deadline-propagation.md) — the time budget that decides whether buffered work is still worth doing.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
