---
name: docker-container-lifecycle-actions
description: Start, stop, and inspect containers with declared resource limits and health checks, verify state transitions, and never force-kill without a grace path.
metadata:
  source: skills/04-action-execution/docker-container-lifecycle-actions.md
  category: 04-action-execution
  version: "v1"
---

# Docker Container Lifecycle Actions

## Description
Start, stop, and inspect containers with declared resource limits and health checks, verify state transitions, and never force-kill without a grace path. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- containerized services must be started and stopped as part of an automated workflow before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for docker container lifecycle actions work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the docker container lifecycle actions steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def plan_stop(state, force=False):
    if state != "running":
        return "no-op"
    return "kill" if force else "stop-graceful"

assert plan_stop("running") == "stop-graceful"
assert plan_stop("exited") == "no-op"

def limits_ok(cpu, mem):
    return 0 < cpu <= 4 and 256 <= mem <= 8192

assert limits_ok(2, 1024) is True and limits_ok(16, 1024) is False
```

## Failure Modes
- Force-killing without a graceful stop window.
- Starting containers without declared resource limits.
- Assuming health-check status from the state field alone.
- Losing logs when containers are removed too early.
- Leaving stopped containers to accumulate on the host.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Container lifecycle automation is a recurring 2026 infrastructure request for agent tooling; this is a dated signal, not an adoption metric.

## Related
- shell-command.md
- process-management.md
- action-result-verification.md
