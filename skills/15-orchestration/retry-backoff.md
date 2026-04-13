---
title: "Retry Backoff"
category: 15-orchestration
level: advanced
stability: stable
description: "Apply retry backoff in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-retry-backoff.json)

**Category:** Orchestration
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Automatically retries failed tool calls or agent steps with configurable exponential backoff, jitter, and maximum attempt limits. Distinguishes transient errors (worth retrying) from permanent failures (abort immediately).

### Example
```python
import time, random

TRANSIENT = {429, 500, 502, 503, 504}

def retry(fn, max_attempts=5, base_delay=1.0, max_delay=60.0):
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception as e:
            code = getattr(e, "status_code", None)
            if code not in TRANSIENT:
                raise
            if attempt == max_attempts - 1:
                raise
            delay = min(base_delay * 2 ** attempt, max_delay)
            jitter = random.uniform(0, delay * 0.1)
            print(f"Retry {attempt+1}/{max_attempts} after {delay+jitter:.1f}s")
            time.sleep(delay + jitter)

call_count = 0
def flaky_call():
    global call_count
    call_count += 1
    if call_count < 3:
        e = Exception("service unavailable")
        e.status_code = 503
        raise e
    return "success"

print(retry(flaky_call))
```

### Related Skills
- [Budget Management](budget-management.md)
- [Rate Limiting](../14-security/rate-limiting.md)
