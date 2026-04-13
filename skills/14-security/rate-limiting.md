![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-14-security-rate-limiting.json)

**Category:** Security
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Throttles agent tool calls and API requests to prevent abuse, runaway loops, and cost overruns. Implements token-bucket, sliding-window, or fixed-window rate limiters per agent, tool, or endpoint.

### Example
```python
import time
from collections import defaultdict, deque

class SlidingWindowLimiter:
    def __init__(self, max_calls: int, window_sec: int):
        self.max_calls = max_calls
        self.window = window_sec
        self._log: dict[str, deque] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = time.time()
        q = self._log[key]
        while q and now - q[0] > self.window:
            q.popleft()
        if len(q) >= self.max_calls:
            return False
        q.append(now)
        return True

limiter = SlidingWindowLimiter(max_calls=5, window_sec=10)
for i in range(7):
    print(f"Call {i+1}: {'OK' if limiter.allow('agent-1') else 'BLOCKED'}", flush=True)
    time.sleep(0.1)
```

### Related Skills
- [Budget Management](../15-orchestration/budget-management.md)
- [Retry Backoff](../15-orchestration/retry-backoff.md)
