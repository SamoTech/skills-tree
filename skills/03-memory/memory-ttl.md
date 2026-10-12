---
title: "Memory TTL"
category: 03-memory
level: intermediate
stability: experimental
description: "Attach explicit time-to-live policies to stored memories so entries expire by design, with expiry sweeps and refresh rules instead of unbounded accumulation."
added: "2026-10"
version: v1
related: ["cache-management", "forgetting"]
---

# Memory TTL

Category: Memory | Level: intermediate | Stability: experimental | Version: v1

## Description

Memory without expiry becomes a landfill of stale facts: yesterday's price, last month's availability, a user status that quietly stopped being true. This skill attaches a time-to-live to each stored memory at write time, sweeps expired entries on a schedule, and defines when a TTL refreshes — so the agent recalls recent truth and forgets expired claims by design rather than by accident.

## When to Use

Use when memory entries have a natural freshness horizon — prices, availability, user status, cache-like facts — where an old value is worse than no value.

Do not give long-lived identity facts a short TTL; expiring stable knowledge wastes retrieval and erodes trust in the memory layer.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `entry` | `map` | Yes | The memory being written |
| `ttl` | `duration` | Yes | Time-to-live applied at write time |
| `refresh_on` | `enum` | No | Access pattern that extends or resets the TTL |

## Procedure

1. Set the TTL at write time from the fact class, not as an afterthought — statuses decay faster than identity facts.
2. Store the expiry timestamp explicitly with the entry rather than computing it lazily at read time.
3. Sweep expired entries on a fixed schedule instead of relying on reads to trigger deletion.
4. Define the refresh rule explicitly: a read refreshes, an update resets, or the TTL is fixed regardless of access.
5. Keep expired entries observable — log sweep counts and categories rather than silently deleting.
6. Audit classes that never expire and justify each one; permanent entries are the exception, not the default.

## Outputs

| Output | Type | Description |
|---|---|---|
| `stored` | `map` | Entry with its expiry timestamp |
| `sweeps` | `map` | Expired-entry counts per period |
| `audit` | `list` | Never-expiring classes and their justification |

## Runnable Example

```python
from datetime import datetime, timedelta

def with_ttl(entry, hours):
    expiry = datetime.utcnow() + timedelta(hours=hours)
    return {**entry, "expires_at": expiry.isoformat()}

def sweep(entries, now=None):
    now = now or datetime.utcnow()
    kept, expired = [], []
    for e in entries:
        if datetime.fromisoformat(e["expires_at"]) > now:
            kept.append(e)
        else:
            expired.append(e["id"])
    return kept, sorted(expired)

entries = [with_ttl({"id": "price", "value": 42}, 24), with_ttl({"id": "user-name", "value": "Sam"}, 24 * 30)]
print(sweep(entries, now=datetime.utcnow() + timedelta(hours=25)))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Read-only expiry | Entries are deleted only when read, so stale-but-unread entries persist | Sweep on a fixed schedule |
| Refresh ambiguity | Unclear rules quietly extend stale data | Define refresh semantics at write time |
| Unbounded growth | Nothing ever expires | Default to a TTL with permanent as the exception |
| Silent deletion | Sweeps are invisible to operators | Log expired counts per category |
| Wrong TTL class | Identity facts decay like volatile facts | Classify facts by stability at write time |

## Security and Authority Boundary

TTLs bound how long sensitive statements about users persist, which supports deletion obligations — but expiry is not deletion compliance. A TTL that removes entries from active recall may still leave them in backups or logs; treat expiry as one layer of a deletion policy.

## Evidence

This skill is grounded in dated public implementation references:

1. The Redis EXPIRE command documentation for key time-to-live semantics (https://redis.io/docs/latest/commands/expire/).
2. Wikipedia's overview of caches, where TTL-based staleness bounds are standard (https://en.wikipedia.org/wiki/Cache_(computing)).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Cache Management](cache-management.md) — the bounded-cache discipline this skill generalizes to memory.
- [Forgetting](forgetting.md) — the retention-decision layer that sets what should expire.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
