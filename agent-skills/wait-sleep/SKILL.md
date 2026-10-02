---
name: wait-sleep
description: Pause for a bounded duration or polling interval without treating elapsed time as proof of state.
metadata:
  source: skills/04-action-execution/wait-sleep.md
  category: 04-action-execution
---

# Wait Sleep

## Description

Pause for a bounded duration or polling interval without treating elapsed time as proof of state.

## When to Use

- Execute an explicitly approved action.
- Use when the target and scope can be verified.
- Verify the resulting state when the action is consequential.

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Target and action | Execution result | Invalid target |
| Scope/authorization | Allowed action | Unauthorized action |
| Timeout/bounds | Controlled execution | Resource exhaustion |
| Postcondition | Verified state | Silent failure |

## Runnable Example

```python
import time
def bounded_wait(seconds, maximum=30):
    if not 0 <= seconds <= maximum: raise ValueError("out of bounds")
    time.sleep(seconds)
    print("wait completed")
```

## Failure modes

Long fixed waits; unbounded polling; busy waiting; assuming time proves state.

## Related

- `assertion.md`
- `process-management.md`
- `automation-review.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
