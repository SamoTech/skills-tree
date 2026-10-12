---
title: "Idempotency Keys"
category: 15-orchestration
level: intermediate
stability: experimental
description: "Assign client-generated idempotency keys to state-changing requests so retries and at-least-once delivery produce one effect, with duplicate calls returning the recorded first result."
added: "2026-10"
version: v1
related: ["task-queue", "state-machine"]
---

# Idempotency Keys

Category: Orchestration | Level: intermediate | Stability: experimental | Version: v1

## Description

At-least-once delivery means the same request will sometimes arrive twice; idempotency keys turn that from a bug into a non-event. The client attaches a unique key to each operation intent, the server checks the key before executing, and a replayed key returns the stored first response instead of executing again. The stored response plus a payload fingerprint closes the gap between "same key" and "same request".

## When to Use

Use for any state-changing request that may be retried — payment calls, task creation, webhook handlers, queue consumers under at-least-once semantics.

Do not bother for pure reads or naturally idempotent operations; the machinery earns its cost only where duplicates have effects.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `key` | `string` | Yes | Client-generated unique key for this operation intent |
| `request_fingerprint` | `hash` | Yes | Digest of the payload the key refers to |
| `results_store` | `map[key -> record]` | Yes | Server-side record of executed keys |
| `ttl` | `duration` | Yes | How long replayed keys resolve to stored results |

## Procedure

1. Generate the key client-side, unique per operation intent — not per session, not per process.
2. Before executing, look the key up: a hit with a matching fingerprint returns the stored response; a hit with a mismatching fingerprint is an error.
3. On a miss, execute once, then store the response keyed by the key and fingerprint.
4. Keep the TTL at least as long as the client's longest retry window; shorter expiry quietly reintroduces duplicates.
5. Keep keys out of URLs and logs; they identify operations and may correlate to sensitive intents.
6. Treat in-flight keys as locked: concurrent duplicate calls wait for the first execution rather than racing it.

## Outputs

| Output | Type | Description |
|---|---|---|
| `response` | `any` | The first execution's response, returned on every replay |
| `replayed` | `boolean` | Whether this call returned a stored result |
| `stored_until` | `timestamp` | When the key record expires |

## Runnable Example

```python
def execute_once(key, fingerprint, store, fn):
    """Execute fn once per key; replays return the stored response."""
    record = store.get(key)
    if record is not None:
        if record["fingerprint"] != fingerprint:
            raise ValueError("key reuse for a different payload")
        return record["response"], True
    response = fn()
    store[key] = {"fingerprint": fingerprint, "response": response}
    return response, False

store = {}
for _ in range(2):
    response, replayed = execute_once("order-42-create", "abc123", store, lambda: "created")
    print(response, replayed)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Key reuse across payloads | Same key sent with different request bodies | Store and compare a payload fingerprint |
| Server-generated keys | Key minted per attempt, not per intent | Generate the key client-side per operation intent |
| No stored response | Key existence recorded, result discarded | Store the response, not just the key |
| TTL shorter than retries | Key expires while the client is still retrying | Keep the TTL above the retry window |
| Keys in URLs | Idempotency keys landing in access logs | Send keys in headers or bodies, never the path |

## Security and Authority Boundary

Idempotency protects the server's effect from duplication; it does not order distinct operations. Sequencing two different calls — even related ones — needs explicit ordering, which this skill does not provide.

## Evidence

This skill is grounded in dated public implementation references:

1. Stripe's API documentation on idempotent requests (https://docs.stripe.com/api/idempotent_requests).
2. Wikipedia's overview of idempotence (https://en.wikipedia.org/wiki/Idempotence).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Task Queue](task-queue.md) — the at-least-once delivery layer that makes keys necessary.
- [State Machine](state-machine.md) — guarded state transitions that pair naturally with keys.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
