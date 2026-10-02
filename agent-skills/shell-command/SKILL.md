---
name: shell-command
description: Execute a permitted local command with explicit working directory, environment, timeout, and output bounds.
metadata:
  source: skills/04-action-execution/shell-command.md
  category: 04-action-execution
---

# Shell Command

## Description

Execute a permitted local command with explicit working directory, environment, timeout, and output bounds.

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
def run_command(argv, cwd):
    if not argv: raise ValueError("empty command")
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=30)
```

## Failure modes

Untrusted command strings; shell injection; unnecessary secrets; no timeout or output bound.

## Related

- `process-management.md`
- `environment-variables.md`
- `approval-before-destructive-tools.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
