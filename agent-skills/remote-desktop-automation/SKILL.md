---
name: remote-desktop-automation
description: Automate tasks over remote desktop protocols with explicit latency and resolution constraints, verifying state on the remote host rather than the local screen.
metadata:
  source: skills/10-computer-use/remote-desktop-automation.md
  category: 10-computer-use
  version: "v1"
---

# Remote Desktop Automation

## Description
Automate tasks over remote desktop protocols with explicit latency and resolution constraints, verifying state on the remote host rather than the local screen. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a task must drive a machine that is only reachable through a remote desktop session.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for remote desktop automation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the remote desktop automation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def frame_ok(width, height, latency_ms, max_latency):
    return 0 < width * height and latency_ms <= max_latency

assert frame_ok(1920, 1080, 40, 80)
assert not frame_ok(1920, 1080, 200, 80)
```

## Failure Modes
- Trusting the local screen as proof of remote state.
- Ignoring latency spikes that make clicks land on stale frames.
- Hard-coding coordinates for one remote resolution.
- Proceeding after a session drop without reconnect verification.
- Recording success without checking the remote host directly.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Remote-desktop and cross-machine UI automation requests recur in 2026 computer-use agent discussions; this is a dated signal, not an adoption metric.

## Related
- vm-interaction.md
- screen-region-mapping.md
- keyboard-type.md
