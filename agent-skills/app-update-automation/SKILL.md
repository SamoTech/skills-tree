---
name: app-update-automation
description: Automate application update installation with pre-update state capture, checksum verification, and post-update readiness checks with rollback on failure.
metadata:
  source: skills/10-computer-use/app-update-automation.md
  category: 10-computer-use
  version: "v1"
---

# App Update Automation

## Description
Automate application update installation with pre-update state capture, checksum verification, and post-update readiness checks with rollback on failure. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- applications must be updated across machines with verifiable recovery on failure.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for app update automation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the app update automation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def update_plan(current, target, checksum_ok, readiness_ok):
    if not (checksum_ok and readiness_ok):
        return 'rollback'
    return 'updated' if current != target else 'noop'

assert update_plan('1.2', '1.3', True, True) == 'updated'
assert update_plan('1.2', '1.3', False, True) == 'rollback'
```

## Failure Modes
- Installing an update whose checksum was never verified.
- Skipping the pre-update state capture that rollback needs.
- Declaring success without a post-update readiness probe.
- Rolling forward on failure because no rollback exists.
- Updating an app mid-use without a drain or maintenance window.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Update installation with rollback verification appears in 2026 fleet-automation requests; this is a dated signal, not an adoption metric.

## Related
- software-installation-automation.md
- app-readiness-probing.md
- computer-use-error-recovery.md
