---
name: mouse-input
description: Perform bounded pointer actions against verified interface targets and verify consequential results.
metadata:
  source: skills/04-action-execution/mouse-input.md
  category: 04-action-execution
---

# Mouse Input

## Description

Perform bounded pointer actions against verified interface targets and verify consequential results.

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
def click_verified(target):
    target.click()
    state = target.get_attribute("data-state")
    if state != "clicked": raise RuntimeError("not verified")
    print("click verified")
```

## Failure modes

Stale coordinates; wrong target; destructive click without authorization; silent failure.

## Related

- `keyboard-input.md`
- `screenshot-capture.md`
- `assertion.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
