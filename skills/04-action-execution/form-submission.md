---
title: "Form Submission"
category: 04-action-execution
level: intermediate
stability: stable
description: "Submit validated form data to a verified target and confirm the resulting state."
added: "2026-09"
related: [keyboard-input, input-sanitization, assertion]
---

# Form Submission

## Description

Submit validated form data to a verified target and confirm the resulting state.

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
def submit(fields):
    required = [k for k in fields if fields[k] is None]
    if required: raise ValueError(required)
    return {"status": "submitted", "count": len(fields)}
```

## Failure modes

Unverified destination; missing validation; leaked secrets; unverified success.

## Related

- `keyboard-input.md`
- `input-sanitization.md`
- `assertion.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
