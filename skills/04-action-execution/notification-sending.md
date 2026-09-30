---
title: "Notification Sending"
category: 04-action-execution
level: intermediate
stability: stable
description: "Deliver an approved notification through a configured channel with validated destination and content."
added: "2026-09"
related: [email-sending, assertion, tool-guardrails]
---

# Notification Sending

## Description

Deliver an approved notification through a configured channel with validated destination and content.

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
def build_notification(destination, message):
    if not destination or not message: raise ValueError("missing input")
    return {"destination": destination, "message": message}
```

## Failure modes

Ambiguous destination; sensitive content leakage; duplicate delivery; uncontrolled urgency.

## Related

- `email-sending.md`
- `assertion.md`
- `tool-guardrails.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
