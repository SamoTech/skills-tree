---
name: cache-management
description: Operate a bounded cache with explicit admission, TTL expiry, deterministic LRU eviction, and a measured hit rate so memory stays capped and staleness stays bounded by policy.
metadata:
  source: skills/03-memory/cache-management.md
  category: 03-memory
  version: "v1"
---

# Cache Management

Category: Memory | Level: intermediate | Stability: experimental | Version: v1

## Description

A cache becomes a correctness risk the moment it has no policy: unbounded growth exhausts memory, and stale entries serve wrong answers with no bound. This skill defines an explicit cache contract — capacity, TTL, eviction order, and a measured hit rate — so behavior is predictable and observable. It covers in-process caches; distributed cache coherence is out of scope.

## When to Use

Use when an agent or service keeps derived or fetched values in memory and either the memory footprint or the staleness window must stay bounded.

Do not use for long-lived stores of record; use the memory and retrieval skills for durable state.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `capacity` | `integer` | Yes | Maximum number of live entries |
| `ttl_seconds` | `number` | Yes | Expiry window applied to every entry |
| `now` | `number` | No | Injectable clock value for deterministic tests |
| `on_evict` | `function` | No | Callback invoked with each evicted key |

## Procedure

1. Declare capacity and TTL before the first write; never admit an entry without both bounds set.
2. On write, store the value with its absolute expiry timestamp and move the key to the most-recently-used position.
3. Evict least-recently-used entries whenever the live count exceeds capacity; eviction order must be deterministic.
4. On read, treat an expired entry as a miss, delete it, and count it as a miss; never serve a value past its expiry.
5. Count hits and misses on every access so the hit rate is measured, not assumed.
6. Re-measure the hit rate after any capacity or TTL change; an unmeasured cache is a liability, not an optimization.
7. Expose the live size, the measured hit rate, and the eviction count for monitoring.
8. Fail closed on unbounded configurations: a cache without capacity or TTL is rejected, not silently tolerated.

## Outputs

| Output | Type | Description |
|---|---|---|
| `value` | `any` | The stored value, or a miss indicator when absent or expired |
| `hits` | `integer` | Accesses served from the cache within expiry |
| `misses` | `integer` | Accesses not served, including expiry misses |
| `hit_rate` | `number` | Measured hits divided by total accesses over the window |

## Runnable Example

```python
from collections import OrderedDict

class BoundedCache:
    """A bounded LRU cache with TTL expiry and a measured hit rate."""

    def __init__(self, capacity, ttl_seconds):
        self.capacity = capacity
        self.ttl = ttl_seconds
        self.store = OrderedDict()
        self.hits = 0
        self.misses = 0

    def put(self, key, value, now):
        self.store[key] = (value, now + self.ttl)
        self.store.move_to_end(key)
        while len(self.store) > self.capacity:
            self.store.popitem(last=False)

    def get(self, key, now):
        entry = self.store.get(key)
        if entry is None:
            self.misses += 1
            return None
        value, expires_at = entry
        if now >= expires_at:
            del self.store[key]
            self.misses += 1
            return None
        self.store.move_to_end(key)
        self.hits += 1
        return value

cache = BoundedCache(capacity=2, ttl_seconds=60)
cache.put("a", 1, now=0)
cache.put("b", 2, now=0)
print(cache.get("a", now=10))
print(cache.get("a", now=100))
print("hits:", cache.hits, "misses:", cache.misses)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Unbounded growth | Capacity was never set | Reject cache creation without a capacity bound |
| Stale serve | Expiry checked lazily or not at all | Check expiry on every read and delete expired entries |
| Eviction thrash | Capacity sits below the working set | Measure the hit rate and resize on evidence |
| Silent cache | No hit or miss counters exist | Count every access and expose the measured rate |
| Clock coupling | Tests read the wall clock directly | Inject the clock so expiry behavior is deterministic |

## Security and Authority Boundary

Operating a cache grants no authority over the source of truth. Cached values are read-only projections; writes flow to the underlying store through its normal controls. Entries holding sensitive data inherit the source’s retention rules: TTL and eviction must not become a way to keep data past its declared lifetime.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s survey of cache replacement policies (https://en.wikipedia.org/wiki/Cache_replacement_policies).
2. Python’s collections module documentation covering OrderedDict (https://docs.python.org/3/library/collections.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Working Memory](working-memory.md) — governs what is held for the current task; this skill bounds how long held values stay valid.
- [Forgetting](forgetting.md) — defines when unneeded state is dropped; TTL expiry is its time-bounded form.
- [Vector Store Retrieval](vector-store-retrieval.md) — retrieves durable representations; this skill governs the ephemeral layer in front of them.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
