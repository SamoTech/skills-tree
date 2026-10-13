---
title: "File Permission Management"
category: 04-action-execution
level: advanced
stability: experimental
description: "Set and verify filesystem permissions to least-privilege values, check effective permissions after the change, and revert on partial failure."
added: "2026-10"
version: v1
related: [file-write, file-delete, env-vars]
tags: [permissions, filesystem, security]
---

# File Permission Management

## Description
Set and verify filesystem permissions to least-privilege values, check effective permissions after the change, and revert on partial failure. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- files must be locked down to least privilege before an agent uses them before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for file permission management work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the file permission management steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def apply_perm(current, desired):
    if int(desired, 8) > 0o777:
        raise ValueError("invalid mode")
    return desired

def is_least_privilege(mode):
    return not (int(mode, 8) & 0o022)

assert apply_perm("644", "600") == "600"
assert is_least_privilege("600") is True
assert is_least_privilege("644") is False
try:
    apply_perm("600", "999")
    raise AssertionError("should have raised")
except ValueError:
    print("mode guard held")
```

## Failure Modes
- Widening permissions to make a failure disappear.
- Not checking effective permissions after umask application.
- Forgetting directory execute bits.
- Ignoring ownership changes alongside modes.
- Leaving a partial change after a mid-path failure.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Least-privilege filesystem actions are a recurring 2026 agent-security hygiene topic in public coverage; this is a dated signal, not an adoption metric.

## Related
- file-write.md
- file-delete.md
- env-vars.md
