---
title: "Keyboard Input"
category: 04-action-execution
level: intermediate
stability: stable
description: "Send bounded keyboard input to a verified target while controlling focus and sensitive text."
added: "2026-09"
related: [mouse-input, clipboard-ops, screenshot-capture]
---

# Keyboard Input

## Description

Send bounded keyboard input to a verified target while controlling focus and sensitive text.

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
def type_bounded(target, text):
    if len(text) > 2000: raise ValueError("input too long")
    target.click()
    target.fill(text)
    print("input complete")
```

## Failure modes

Wrong focus; destructive shortcuts; sensitive keystroke logging; unbounded input.

## Related

- `mouse-input.md`
- `clipboard-ops.md`
- `screenshot-capture.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
