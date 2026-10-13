---
name: ssh-remote-command-execution
description: Execute commands on remote hosts over SSH with explicit host keys, non-interactive auth, timeout handling, and full stdout and stderr capture.
metadata:
  source: skills/04-action-execution/ssh-remote-command-execution.md
  category: 04-action-execution
  version: "v1"
---

# SSH Remote Command Execution

## Description
Execute commands on remote hosts over SSH with explicit host keys, non-interactive auth, timeout handling, and full stdout and stderr capture. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a command must run on a remote host without interactive prompts before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for ssh remote command execution work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the ssh remote command execution steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def build_command(allowed, requested):
    if requested not in allowed:
        raise ValueError("command not on allowlist %r" % requested)
    return ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", requested]

allowed = {"systemctl status app", "uptime"}
assert build_command(allowed, "uptime")[1] == "-o"
try:
    build_command(allowed, "rm -rf /")
    raise AssertionError("should have raised")
except ValueError:
    print("ssh allowlist held")
```

## Failure Modes
- Accepting unknown host keys on first connection.
- Hanging forever with no timeout.
- Dropping stderr and missing the real error.
- Using interactive password prompts inside automation.
- Running commands outside an explicit allowlist.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Remote execution for agent-operated infrastructure is a recurring 2026 operations request signal; this is a dated signal, not an adoption metric.

## Related
- shell-command.md
- process-management.md
- http-request.md
