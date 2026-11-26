---
title: "Shell Command"
category: 04-action-execution
level: advanced
stability: stable
version: v2
description: "Execute a permitted local command with explicit working directory, allowlisted environment, timeout, and output bounds, without shell injection."
added: "2026-09"
related: [process-management, env-vars, approval-before-destructive-tools]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-shell-command.json)

# Shell Command

**Category:** `action-execution`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Execute a permitted local command with explicit working directory, environment, timeout, and output bounds. Commands run as argv lists rather than interpolated shell strings, the environment is allowlisted rather than inherited, and destructive commands require prior authorization.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `argv` | list of string | Command plus arguments; never an interpolated shell string |
| Input | `cwd` | verified directory | Working directory the command runs in |
| Input | `env_allowlist` | list of string | Environment variables the command may receive |
| Input | `timeout` | number | Wall-clock bound applied to the command |
| Output | `result` | `{returncode, stdout, stderr}` | The bounded execution record |

### Procedure
1. Run the command through an argv list with shell interpretation disabled; reject any request that requires `shell=True` string interpolation.
2. Verify the working directory exists and is inside the approved scope for this task.
3. Build the child environment from an explicit allowlist (for example `PATH`, `HOME`, task variables); secrets pass only when the command demonstrably needs them.
4. Apply a timeout and capture output with bounds before starting.
5. Treat destructive commands (deletion, permission changes, remote execution) as requiring prior explicit authorization.
6. Record the return code and bounded output; a completed command is evidence only when its effect has been checked.

### Example

```python
import subprocess, os

def run_command(argv: list[str], cwd: str, timeout: float = 30,
                env_allowlist: list[str] = ["PATH", "HOME"]) -> dict:
    if not argv:
        raise ValueError("empty command")
    if not os.path.isdir(cwd):
        raise ValueError(f"cwd does not exist: {cwd}")
    env = {k: os.environ[k] for k in env_allowlist if k in os.environ}
    p = subprocess.run(argv, cwd=cwd, env=env, capture_output=True,
                       text=True, timeout=timeout, shell=False)
    return {"returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr}

result = run_command(["git", "status", "--porcelain"], cwd="/tmp/example-repo")
print(result)
```

### Related Skills

- [Process Management](process-management.md)
- [Environment Variables](env-vars.md)
- [Approval Before Destructive Tools](../14-security/approval-before-destructive-tools.md)

## Failure Modes

- Untrusted command strings passed to a shell: injection through interpolated input; always use argv lists.
- Unnecessary secrets in the child environment; allowlist instead of inheriting.
- No timeout or output bound: a hung or chatty command stalls the sequence.
- Working directory outside the approved scope.
- Destructive commands executed without prior authorization.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, an explicit procedure, an argv-list example with an environment allowlist, expanded failure modes, and version history; repaired the Related pointer to the existing `env-vars` skill (the previously referenced `environment-variables.md` does not exist in the corpus).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
