![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-wait-sleep.json)

# Wait / Sleep

**Category:** `action-execution`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Pause agent execution for a fixed duration or until a condition is met — used for rate limiting, polling, and timing coordination.

### Example

```python
import time

# Fixed wait
time.sleep(2)

# Poll until condition
for _ in range(30):
    if job_is_done():
        break
    time.sleep(1)
```

### Related Skills

- [Retry / Backoff](../15-orchestration/retry-backoff.md)
- [Process Management](process-management.md)
