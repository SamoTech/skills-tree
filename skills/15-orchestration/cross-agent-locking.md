---
title: "Cross-Agent Locking"
category: 15-orchestration
level: advanced
stability: experimental
description: "Coordinate exclusive access to shared resources across distributed agents using leases with fencing tokens, preventing deadlocks and torn writes from concurrent mutation."
added: "2026-10"
version: v1
related: ["shared-memory","idempotency-keys"]
---

# Cross-Agent Locking

Category: Orchestration | Level: advanced | Stability: experimental | Version: v1

## Description

When two agents can mutate the same resource, correctness needs a lock, and distributed locks need more than mutual exclusion. The skill covers choosing lock granularity, issuing time-bounded leases with fencing tokens so a stalled holder cannot corrupt later writers, ordering acquisition to prevent deadlock, and handling the crash case: leases expire, the next holder proceeds, and the fencing token rejects the zombie. Lock state lives in a coordinator both sides can see, never in agent memory.

## When to Use

Use when multiple agents operate on shared state or resources that must not be mutated concurrently: shared files, external accounts, or single-instance workflows.

Do not treat advisory flags in a shared document as locks. Without a coordinator, expiry, and fencing, two agents will both believe they hold the resource.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `resource_id` | `string` | Yes | Identifier of the shared resource to protect |
| `lease_ttl` | `int` | Yes | Maximum lease duration before forced expiry |
| `coordinator` | `object` | Yes | Shared lease store both acquiring agents can observe |

## Procedure

1. Choose lock granularity: the smallest scope that prevents the conflict, not the whole task.
2. Acquire a lease from the coordinator with a bounded TTL and a fencing token number.
3. Record the token with every mutation so stale writes can be rejected downstream.
4. Acquire multiple locks in a fixed global order to prevent deadlock cycles.
5. Release the lease immediately after the critical section; never hold across waits.
6. Handle expiry: renew in-flight if needed, and accept rejection when a higher token exists.

## Outputs

| Output | Type | Description |
|---|---|---|
| `lease` | `object` | Holder identity, token, TTL, and expiry time |
| `acquisition_log` | `list` | Ordered acquisition and release events |
| `conflict_report` | `object` | Contested acquisitions and fencing rejections |

## Runnable Example

```python
def check_fencing(incoming_token, last_applied):
    """returns whether a write may proceed"""
    if incoming_token > last_applied:
        return {"apply": True, "last_applied": incoming_token}
    return {"apply": False, "reason": "stale token", "last_applied": last_applied}

def detect_deadlock(waits):
    """waits: {agent: [agents it waits for]}"""
    def cycle(node, seen):
        if node in seen:
            return True
        for nxt in waits.get(node, []):
            if cycle(nxt, seen | {node}):
                return True
        return False
    return {a: cycle(a, set()) for a in waits}

print(check_fencing(7, last_applied=9))
print(detect_deadlock({"a": ["b"], "b": ["a"], "c": []}))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Split-brain hold | Lease expiry unobserved by a stalled holder | Fencing tokens rejected at the resource |
| Deadlock | Locks acquired in different orders | Fixed global acquisition order |
| Lock leak | Crashed agent never released | Bounded TTL with automatic expiry |
| Over-broad locking | Whole-task locks serialize everything | Lock the smallest conflicting scope |
| Advisory lock ignored | A rogue agent bypasses the coordinator | Enforce at the resource with token checks, not trust |

## Security and Authority Boundary

Lock coordinators become shared infrastructure with availability impact. Authenticate lease acquisition, scope tokens to the resource, and audit the acquisition log, because the log is the evidence in any post-incident dispute over who held what.

## Evidence

This skill is grounded in dated public implementation references:

1. The etcd distributed key-value store used for leases and coordination (https://etcd.io/).
2. The Apache ZooKeeper coordination service (https://zookeeper.apache.org/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Shared Memory](shared-memory.md) — the shared state layer locking exists to protect.
- [Idempotency Keys](idempotency-keys.md) — the companion discipline that makes repeated writes safe.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
