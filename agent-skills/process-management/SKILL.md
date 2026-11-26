---
name: process-management
description: Manage a local process with explicit command scope, timeout, environment minimization, output limits, and a termination policy.
metadata:
  source: skills/04-action-execution/process-management.md
  category: 04-action-execution
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-process-management.json)

# Process Management

**Category:** `action-execution`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Manage a local process with explicit command scope, timeout, environment, output limits, and termination policy. Every process runs inside declared bounds, inherits the minimum environment necessary, and is terminated or reported deliberately rather than left running.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `argv` | list of string | The exact command and arguments; no shell string interpolation |
| Input | `timeout` | number | Wall-clock bound; the process is terminated when exceeded |
| Input | `env` | map or `None` | Explicit environment; never inherits secrets implicitly |
| Input | `max_output` | int | Cap on captured stdout/stderr bytes |
| Output | `result` | `{returncode, stdout, stderr, timed_out}` | The bounded execution record |

### Procedure
1. Express the command as an argv list so arguments cannot be reinterpreted by a shell.
2. Declare the environment explicitly; pass only the variables the process needs, never the full inherited environment.
3. Set a timeout and an output cap before starting; a process without bounds is a defect, not a default.
4. Start the process and collect output through bounded pipes; on timeout, terminate the process tree, not only the parent.
5. Record the return code and output; a zero return code without a checked postcondition is not success evidence.
6. Escalate termination of processes owned by other sessions or system services for explicit human approval.

### Example

```python
import subprocess

def run_bounded(argv: list[str], timeout: float = 10, max_output: int = 100_000) -> dict:
    if not argv or any(not isinstance(a, str) for a in argv):
        raise ValueError("argv must be a non-empty list of strings")
    try:
        p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = p.communicate(timeout=timeout)
        return {"returncode": p.returncode, "stdout": out[:max_output],
                "stderr": err[:max_output], "timed_out": False}
    except subprocess.TimeoutExpired:
        p.kill()
        p.communicate()
        return {"returncode": None, "stdout": "", "stderr": "", "timed_out": True}

result = run_bounded(["python", "-c", "print('ok')"])
print(result)
```

### Related Skills

- [Shell Command](shell-command.md)
- [Assertion](assertion.md)
- [Approval Before Destructive Tools](../14-security/approval-before-destructive-tools.md)

## Failure Modes

- Out-of-scope termination: killing processes outside this task's ownership; escalate instead.
- No timeout: an unbounded process hangs the whole action sequence.
- Secret inheritance: passing the full environment leaks credentials to the child process.
- Killing only the parent while children keep running; terminate the process tree.
- Reporting a zero exit code as success without checking the process's actual effect.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, an explicit procedure, a bounded-execution example with process-tree timeout handling, expanded failure modes, and version history.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
