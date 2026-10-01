---
title: "Rate Limiting"
category: 14-security
level: advanced
stability: stable
description: "Bound agent and tool request frequency to control abuse, runaway loops, concurrency spikes, and resource cost."
added: "2025-03"
updated: "2026-10"
version: v2
related: [retry-backoff, budget-management, permission-checking]
---

# Rate Limiting

## Description

Rate limiting constrains how frequently an agent, user, tool, or endpoint may perform an operation during a defined interval. In agent systems it is also a control against runaway tool loops and unbounded external API cost.

Choose a limiter according to the failure mode: token bucket for bursts, sliding windows for straightforward request counts, or provider-side quotas when the external service is authoritative.

## Inputs / Outputs

| Input | Type | Required | Description |
|---|---|---:|---|
| `key` | string | yes | Identity/resource bucket |
| `limit` | int | yes | Maximum allowed rate |
| `window_seconds` | float | yes | Time window or refill interval |
| `cost` | int | no | Weighted request cost |

| Output | Type | Description |
|---|---|---:|
| `allowed` | bool | Whether the request may proceed |
| `retry_after` | float | Approximate delay when blocked |

## Runnable Example

```python
import time
from collections import defaultdict, deque

class SlidingWindow:
    def __init__(self, limit: int, window: float):
        self.limit, self.window = limit, window
        self.events = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        q = self.events[key]
        while q and now - q[0] >= self.window:
            q.popleft()
        if len(q) >= self.limit:
            return False
        q.append(now)
        return True

limiter = SlidingWindow(3, 1.0)
print([limiter.allow("agent-1") for _ in range(5)])
```

For distributed systems, use an atomic shared store or the upstream provider's quota mechanism; an in-memory limiter is process-local.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Bypass | Key can be changed by the caller | Derive identity from authenticated context |
| Burst overload | Fixed window allows boundary bursts | Use sliding window or token bucket |
| Distributed race | Multiple workers update counters independently | Use atomic centralized state |
| Retry storm | Clients retry immediately after denial | Return bounded retry information and use backoff |
| Starvation | One tenant consumes the whole quota | Partition limits by tenant/agent/resource |
| Clock issues | Wall-clock adjustments | Use monotonic time for local windows |

## Design Rules

- Apply limits at the earliest authoritative boundary.
- Rate-limit expensive tools separately from cheap operations.
- Combine request limits with concurrency and budget limits.
- Make blocked requests observable without logging sensitive payloads.
- Use provider-specific quotas when they are stricter than local limits.

## References

- RFC 6585 (HTTP 429 Too Many Requests): https://www.rfc-editor.org/rfc/rfc6585
- OWASP API Security: https://owasp.org/API-Security/

Evidence status: implementation guidance is grounded in HTTP/API rate-control conventions; no universal safe limit is claimed.

## Related Skills

- [Budget Management](../15-orchestration/budget-management.md)
- [Retry Backoff](../15-orchestration/retry-backoff.md)
- [Permission Checking](permission-checking.md)
