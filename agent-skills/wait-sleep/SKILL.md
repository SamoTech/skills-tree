---
name: wait-sleep
description: Pause for a bounded duration or poll a condition with bounds, without treating elapsed time as proof of state.
metadata:
  source: skills/04-action-execution/wait-sleep.md
  category: 04-action-execution
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-wait-sleep.json)

# Wait Sleep

**Category:** `action-execution`
**Skill Level:** `basic`
**Stability:** `stable`
**Added:** 2026-09

### Description

Pause for a bounded duration or poll until a condition holds, inside explicit bounds. Elapsed time is never treated as proof of state: waits end either at a verified condition or at a declared bound that is reported as a failure.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `seconds` | number | Fixed pause duration, bounded above |
| Input | `condition` | callable returning bool | Optional poll predicate; preferred over fixed sleeps |
| Input | `max_wait` | number | Total bound across all polls; exceeded means failure |
| Output | `wait_result` | `{satisfied, waited}` | Whether the condition was verified and the time spent |

### Procedure
1. Prefer polling a condition over a fixed sleep whenever the goal is a state change.
2. Bound every wait: a maximum duration and a polling interval; both are declared before waiting.
3. Re-check the condition after each interval, not just once at the end.
4. When the bound expires without the condition holding, stop and report the timeout as a failure.
5. Never busy-wait in a tight loop; yield between polls.
6. Treat "waited long enough" as an unverified claim; only the condition check is evidence.

### Example

```python
import time

def bounded_wait(seconds: float, maximum: float = 30) -> float:
    if not 0 <= seconds <= maximum:
        raise ValueError(f"out of bounds: {seconds} > {maximum}")
    time.sleep(seconds)
    return seconds

def poll_until(condition, interval: float = 0.5, max_wait: float = 15) -> dict:
    deadline = time.monotonic() + max_wait
    while time.monotonic() < deadline:
        if condition():
            return {"satisfied": True, "waited": round(max_wait - (deadline - time.monotonic()), 3)}
        time.sleep(interval)
    return {"satisfied": False, "waited": max_wait}

result = poll_until(lambda: True, interval=0.1, max_wait=2)
print(result)
```

### Related Skills

- [Assertion](assertion.md)
- [Process Management](process-management.md)
- [Automation Review](../15-orchestration/automation-review.md)

## Failure Modes

- Long fixed waits that slow every run without adding certainty; poll a condition instead.
- Unbounded polling that never terminates; declare `max_wait` before polling.
- Busy waiting without yielding between checks.
- Treating elapsed time as proof that the expected state was reached.
- Swallowing the timeout and continuing as if the condition held.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, an explicit procedure, a bounded polling example, expanded failure modes, and version history.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
