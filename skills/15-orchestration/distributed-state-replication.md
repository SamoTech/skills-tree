---
title: "Distributed State Replication"
category: 15-orchestration
level: advanced
stability: experimental
description: "Replicate shared workflow and memory state across agent workers with a consistency model, quorum acknowledgment, and deterministic merge so any worker can resume after failure."
added: "2026-10"
version: v1
related: ["stateful-agent-graphs","thread-based-resume"]
---

# Distributed State Replication

Category: Orchestration | Level: advanced | Stability: experimental | Version: v1

## Description

Replication turns local state into a survivable one. The skill covers choosing a consistency model appropriate to the workload, serializing state with deterministic ordering, replicating with quorum acknowledgment before declaring a write durable, and merging concurrent updates with a deterministic rule so all replicas converge without a human referee. The test of the design is whether a fresh worker can resume the workflow from replicated state alone.

## When to Use

Use when multi-agent or multi-node execution must survive worker failure without losing workflow progress, or when several workers need a consistent view of shared state.

Do not replicate state with wall-clock timestamps as the ordering key. Clock skew across workers produces last-write-wins on the wrong write.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `state_object` | `object` | Yes | The workflow or shared state to replicate |
| `consistency_model` | `enum` | Yes | `quorum` (default) or `single-leader` as the ordering authority |
| `replicas` | `int` | No | Replica count; defaults to a majority-of-workers quorum |

## Procedure

1. Define the state object and its write paths before choosing replication mechanics.
2. Choose the consistency model and the ordering authority: a leader or a quorum rule.
3. Serialize updates with a deterministic order: sequence numbers or version vectors, never wall clocks.
4. Replicate each update and declare durability only after quorum acknowledgment.
5. Merge concurrent updates with a deterministic conflict rule so replicas converge.
6. Recover failed workers by rebuilding their state from the acknowledged replica log.

## Outputs

| Output | Type | Description |
|---|---|---|
| `replicated_state` | `object` | State as acknowledged by a quorum of replicas |
| `update_log` | `table` | Ordered updates with sequence numbers and acknowledgments |
| `recovery_plan` | `object` | How a failed worker rebuilds from the replica set |

## Runnable Example

```python
def quorum_ack(update, acks, replicas, majority=None):
    """acks: number of replicas that acknowledged"""
    m = majority if majority is not None else replicas // 2 + 1
    return {"durable": acks >= m, "acked": acks, "required": m}

def merge_concurrent(a, b, rule="higher-seq"):
    if rule != "higher-seq":
        raise ValueError("unknown merge rule")
    winner = a if a["seq"] >= b["seq"] else b
    return {"winner": winner["value"], "seq": winner["seq"]}

print(quorum_ack({"seq": 12}, acks=2, replicas=3))
print(merge_concurrent({"seq": 5, "value": "draft-a"}, {"seq": 6, "value": "draft-b"}))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Split-brain state | Two authorities accepted conflicting writes | Single leader or quorum rule with fencing |
| Clock-skew corruption | Wall-clock ordering across workers | Sequence numbers or version vectors for ordering |
| False durability | Write acknowledged locally only | Quorum acknowledgment before declaring durable |
| Non-deterministic merge | Conflicts resolved differently per replica | One deterministic merge rule applied everywhere |
| Unbounded log | Replica history grows without compaction | Snapshot and compact behind acknowledged progress |

## Security and Authority Boundary

Replicated state widens exposure: every replica holds the full state, including anything sensitive the workflow carries. Encrypt replication traffic, scope replica membership through authenticated membership, and compact secrets out of snapshots where the workflow no longer needs them.

## Evidence

This skill is grounded in dated public implementation references:

1. The Raft consensus algorithm reference (https://raft.github.io/).
2. The etcd distributed key-value store implementing Raft replication (https://github.com/etcd-io/etcd).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Stateful Agent Graphs](stateful-agent-graphs.md) — the workflow structure whose state replication protects.
- [Thread-Based Resume](thread-based-resume.md) — the recovery path that consumes replicated state.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
