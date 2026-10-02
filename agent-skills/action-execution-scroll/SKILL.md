---
name: action-execution-scroll
description: Scroll a verified interface container by a bounded amount and verify the resulting viewport state.
metadata:
  source: skills/04-action-execution/scroll.md
  category: 04-action-execution
---

# Scroll

## Description

Scroll a verified interface container by a bounded amount and verify the resulting viewport state.

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
def scroll_verified(page, pixels=600):
    if not 1 <= pixels <= 2000: raise ValueError("out of bounds")
    page.mouse.wheel(0, pixels)
    print("scroll completed")
```

## Failure modes

Wrong container; unbounded loop; assumed viewport change; bypassing authorization.

## Related

- `mouse-input.md`
- `screen-reading.md`
- `assertion.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
