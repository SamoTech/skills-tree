---
title: "Tool Result Caching"
category: 07-tool-use
level: intermediate
stability: experimental
description: "Reuse identical tool calls that already succeeded — keyed by operation and arguments — so repeat work costs a lookup instead of another remote round trip."
added: "2026-10"
version: v1
related: ["tool-review-loops", "function-calling"]
---

# Tool Result Caching

Category: Tool Use | Level: intermediate | Stability: experimental | Version: v1

## Description

Every tool call that returns the same answer for the same arguments is a cache wearing a network costume. This skill makes that explicit: a deterministic operation gets a cache key built from its identity and its arguments, responses are stored with a time-to-live and a staleness policy, and a hit must be marked as cached so downstream consumers know what they are reading. The discipline is deciding which calls are cacheable — deterministic and side-effect-free — before caching anything.

## When to Use

Use for deterministic, read-only calls whose arguments repeat across a session or pipeline — enrichment lookups, reference data fetches, idempotent reads.

Do not cache calls whose results depend on hidden state, side effects, wall-clock time, or caller identity, and do not let a cache silently answer after the underlying data contract changes underneath it.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `operation` | `string` | Yes | The tool operation being cached |
| `arguments` | `map` | Yes | The call arguments that form part of the cache key |
| `ttl` | `duration` | Yes | How long a cached response may be served |
| `stale_policy` | `enum` | No | What happens on expiry — refetch, or serve-stale-while-refreshing |

## Procedure

1. Confirm the operation is deterministic and side-effect-free; anything with hidden state is disqualified before a key is built.
2. Build the cache key from the operation identity and the full, normalized argument set, so two calls that differ only in formatting still share an entry.
3. Store the response with its time-to-live and the timestamp of the fetch, not the timestamp of the read.
4. On a hit, return the cached value marked as cached, with its original fetch time, so consumers can reason about staleness.
5. On expiry, refetch — or serve stale while refreshing when the policy allows — and record the miss rate per operation.
6. Invalidate by key when the underlying data is known to change, and treat a change in the data contract as a full invalidation.

## Outputs

| Output | Type | Description |
|---|---|---|
| `cache_key` | `string` | The deterministic key for the operation and arguments |
| `cached_response` | `map` | The stored response with fetch timestamp and provenance |
| `metrics` | `map` | Hit rate, miss rate, and staleness served per operation |

## Runnable Example

```python
import json

class ResultCache:
    def __init__(self):
        self.store = {}

    @staticmethod
    def key_for(operation, arguments):
        normalized = json.dumps(arguments, sort_keys=True)
        return f"{operation}:{normalized}"

    def get(self, operation, arguments, ttl_seconds, now):
        key = self.key_for(operation, arguments)
        entry = self.store.get(key)
        if entry and now - entry["fetched_at"] <= ttl_seconds:
            return {"value": entry["value"], "cached": True}
        return None

    def put(self, operation, arguments, value, now):
        key = self.key_for(operation, arguments)
        self.store[key] = {"value": value, "fetched_at": now}

cache = ResultCache()
cache.put("lookup_region", {"id": "eu-1"}, "europe", now=100)
print(cache.get("lookup_region", {"id": "eu-1"}, ttl_seconds=60, now=110))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Stale answers | The underlying source changed within the TTL | Keep TTLs short for volatile data and invalidate on known writes |
| Key collisions | Different calls normalized into one key | Include the full argument set and operation in the key |
| Side-effect caching | A non-deterministic call got cached | Cache only deterministic, read-only operations |
| Silent provenance | Consumers cannot tell a hit from a fetch | Mark every served value as cached with its fetch time |
| Unbounded growth | Entries accumulate without eviction | Bound the cache and evict on a replacement policy |

## Security and Authority Boundary

A cache is a copy of data outside its origin's access control: cache stores inherit the sensitivity of what they hold, so entries holding user-scoped or restricted data must be keyed to the caller's scope and evicted on scope change, never shared across principals.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of caching in computing (https://en.wikipedia.org/wiki/Cache_%28computing%29).
2. Wikipedia's overview of cache replacement policies (https://en.wikipedia.org/wiki/Cache_replacement_policies).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Tool Review Loops](tool-review-loops.md) — deciding whether a tool call is worth making at all.
- [Function Calling](function-calling.md) — the calling convention whose results get cached.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
