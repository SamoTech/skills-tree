---
title: "Process Management"
category: 04-action-execution
level: advanced
stability: stable
description: "Manage a local process with explicit command scope, timeout, environment, output limits, and termination policy."
added: "2026-09"
related: [shell-command, assertion, approval-before-destructive-tools]
---

# Process Management

## Description

Manage a local process with explicit command scope, timeout, environment, output limits, and termination policy.

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
import subprocess
p = subprocess.Popen(["python", "-c", "print('ok')"], stdout=subprocess.PIPE, text=True)
out, _ = p.communicate(timeout=10)
print(p.returncode, out.strip())
```

## Failure modes

Out-of-scope termination; no timeout; unnecessary secret inheritance; incomplete success evidence.

## Related

- `shell-command.md`
- `assertion.md`
- `approval-before-destructive-tools.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
