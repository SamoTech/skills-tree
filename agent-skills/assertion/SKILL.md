---
name: assertion
description: Check an explicit execution invariant and stop safely when the expected state is not true.
metadata:
  source: skills/04-action-execution/assertion.md
  category: 04-action-execution
---

# Assertion

## Description

Verify a condition that must hold before an agent continues an action sequence. Assertions turn assumptions into explicit gates and should fail closed when the expected state cannot be established.

## When to Use

- Checking a precondition before a destructive action.
- Verifying an API response or file state.
- Enforcing invariants in automation.

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Condition | Boolean or exception | False condition |
| Context/message | Actionable failure | Missing context |
| Severity | Stop or escalation decision | Wrong escalation |

## Runnable example

```python
def assert_state(condition, message):
    if not condition:
        raise RuntimeError("Assertion failed: " + message)
    return True

record = {"status": "ready"}
assert_state(record.get("status") == "ready", "record is not ready")
print("precondition satisfied")
```

## Failure modes

- Logging a failed assertion while continuing.
- Checking stale state.
- Hiding the evidence needed to diagnose failure.
- Using an assertion as a substitute for authorization.

## Related

- ../02-reasoning/self-correction.md
- ../14-security/approval-before-destructive-tools.md
- ../14-security/output-guardrails.md

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
