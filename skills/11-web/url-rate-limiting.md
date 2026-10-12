---
title: "URL Rate Limiting"
category: 11-web
level: intermediate
stability: experimental
description: "Apply per-host token-bucket rate limiting with declared burst capacity and an injectable clock so fetching stays inside polite budgets and backpressure is observable, not discovered."
added: "2026-10"
version: v1
related: ["web-crawling", "url-fetching"]
---

# URL Rate Limiting

Category: Web | Level: intermediate | Stability: experimental | Version: v1

## Description

Every fetcher needs a throttle it can explain: a rate, a burst, and a per-host scope, enforced by a token bucket rather than by sleeps between calls. This skill defines that bucket — capacity and refill rate per host, an injectable clock for deterministic tests, and an allow/deny answer per request — so a crawl’s politeness is a recorded contract that can be measured, tuned, and logged.

## When to Use

Use whenever an agent fetches from hosts it does not own, when a host declares a crawl delay, or before any parallel fetch loop could otherwise stampede a single origin.

Do not use to throttle your own outbound API quota when the platform enforces it already; double throttling wastes time without adding politeness.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `rate_per_second` | `number` | Yes | Sustained refill rate of the bucket |
| `capacity` | `number` | Yes | Burst size: tokens available at once |
| `host` | `string` | Yes | Per-host bucket key; budgets never share |
| `clock` | `function -> number` | No | Injectable time source for deterministic tests |

## Procedure

1. Create one bucket per host; a shared bucket lets one fast host starve every other.
2. Refill tokens by elapsed time multiplied by the declared rate, capped at the burst capacity.
3. Admit a request only when a full token is available; deny without consuming.
4. Honour host-declared crawl delays by treating them as a lower bound on the rate.
5. Log allow and deny decisions with timestamps so backpressure is measured, not inferred.
6. Never bypass the bucket on error paths; retries consume tokens like any other request.
7. Inject the clock in tests so refill arithmetic replays deterministically.

## Outputs

| Output | Type | Description |
|---|---|---|
| `allowed` | `boolean` | Whether the request may proceed now |
| `tokens` | `number` | Remaining tokens after the decision |
| `denied_total` | `integer` | Cumulative denials for observability |

## Runnable Example

```python
class TokenBucket:
    """Per-host token bucket with an injectable clock."""

    def __init__(self, rate_per_second, capacity, clock):
        self.rate = rate_per_second
        self.capacity = capacity
        self.tokens = capacity
        self.updated = clock()
        self.clock = clock
        self.denied = 0

    def allow(self):
        now = self.clock()
        self.tokens = min(self.capacity, self.tokens + (now - self.updated) * self.rate)
        self.updated = now
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        self.denied += 1
        return False

times = [0.0, 0.1, 0.2, 1.0, 3.0]
clock = iter(times).__next__
bucket = TokenBucket(rate_per_second=0.5, capacity=2, clock=clock)
for now in times:
    print(f"t={now} allowed={bucket.allow()}")
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Stampede | Parallel fetches share no throttle | Route every fetch through one per-host bucket |
| Refill drift | Tokens computed from wall clock in tests | Inject the clock so refill arithmetic is deterministic |
| Burst abuse | Capacity larger than the host tolerates | Set burst from the host’s crawl delay and measured limits |
| Retry bypass | Error-retry paths skip the bucket | Charge retries the same tokens as first attempts |
| Invisible pressure | Denials never logged | Count denials per host and surface the metric |

## Security and Authority Boundary

Rate limiting is a politeness boundary, not an authorization one. Passing the bucket grants no right to fetch; robots rules, terms of service, and authentication still apply, and denial must degrade gracefully rather than escalate.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s overview of the token bucket algorithm (https://en.wikipedia.org/wiki/Token_bucket).
2. MDN documentation for the Retry-After response header (https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Web Crawling](web-crawling.md) — the traversal whose politeness budget this bucket enforces.
- [URL Fetching](url-fetching.md) — the transport that must consult the bucket before every request.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
