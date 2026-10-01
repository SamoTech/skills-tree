---
title: "Sandboxed Execution"
category: 14-security
level: advanced
stability: stable
description: "Execute untrusted agent-generated code inside a separately enforced isolation boundary with resource, filesystem, network, and timeout controls."
added: "2025-03"
updated: "2026-10"
version: v2
---

# Sandboxed Execution

## Description

Sandboxed execution separates untrusted code from the agent host and limits what the code can read, write, execute, and connect to. A timeout alone is not a sandbox. Production isolation should be enforced by an operating-system, container, VM, or dedicated execution service boundary.

Treat the sandbox policy as part of the security contract: filesystem visibility, network egress, CPU/memory limits, process privileges, runtime image, and cleanup must all be explicit.

## Inputs / Outputs

| Input | Type | Required | Description |
|---|---|---:|---|
| `code` | string | yes | Untrusted program |
| `timeout_seconds` | int | yes | Maximum execution duration |
| `network` | string | yes | Explicit network policy such as `none` |
| `workspace` | path | no | Isolated working directory |

| Output | Type | Description |
|---|---|---:|
| `stdout` | string | Captured standard output |
| `stderr` | string | Captured standard error |
| `exit_code` | int | Process result |
| `timed_out` | bool | Whether the execution exceeded the limit |

## Runnable Example

```python
import subprocess

code = "print(2 ** 16)"
result = subprocess.run(
    ["python", "-c", code],
    capture_output=True,
    text=True,
    timeout=3,
    check=False,
)
print({"stdout": result.stdout.strip(), "exit_code": result.returncode})
```

This example demonstrates timeout-bounded subprocess execution only. It is **not** a security sandbox and must not be used as isolation for hostile code without an additional OS/container/VM boundary.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Host escape | Weak isolation boundary | Use a maintained container/VM runtime and least privilege |
| Network exfiltration | Unrestricted egress | Default to no network; allow only required destinations |
| Resource exhaustion | CPU/memory/process abuse | Enforce hard resource quotas outside the guest process |
| Filesystem exposure | Host paths mounted into the sandbox | Use an isolated workspace and read-only mounts where possible |
| Dependency attack | Untrusted packages installed at runtime | Use pinned images/packages and controlled registries |
| Cleanup failure | Processes survive after timeout | Kill the process tree and verify cleanup |

## Design Rules

- Do not call `eval` or `exec` on untrusted input in the agent process.
- Do not treat a Python timeout as a security boundary.
- Default network access to disabled.
- Use non-root execution and a minimal runtime image.
- Apply resource limits outside the untrusted process.
- Delete temporary state after execution and verify cleanup.
- Keep sandbox credentials separate from host credentials.

## References

- Python subprocess documentation: https://docs.python.org/3/library/subprocess.html
- OWASP Server-Side Request Forgery Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html

Evidence status: the cited Python documentation supports process execution semantics; isolation guarantees depend on the external sandbox technology and configuration.

## Related Skills

- [Input Sanitization](input-sanitization.md)
- [Permission Checking](permission-checking.md)
- [Secret Scanning](secret-scanning.md)
