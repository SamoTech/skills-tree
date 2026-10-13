---
name: session-keepalive-automation
description: Keep authenticated sessions alive during long automation runs with honest activity signals and expiry detection that fails closed.
metadata:
  source: skills/10-computer-use/session-keepalive-automation.md
  category: 10-computer-use
  version: "v1"
---

# Session Keepalive Automation

## Description
Keep authenticated sessions alive during long automation runs with honest activity signals and expiry detection that fails closed. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a long automation run must not die mid-way from session expiry.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for session keepalive automation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the session keepalive automation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def keepalive(last_activity, expiry_s, now_s, margin_s):
    if expiry_s - (now_s - last_activity) <= margin_s:
        return 'refresh'
    return 'hold'

assert keepalive(0, 3600, 3400, 120) == 'refresh'
assert keepalive(0, 3600, 600, 120) == 'hold'
```

## Failure Modes
- Sending keepalives after the session already expired.
- Refreshing with fake activity that violates the site policy.
- Ignoring absolute session caps that no keepalive extends.
- Treating a keepalive response as proof of full re-auth.
- Not failing closed when refresh is unavailable.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Long-run session expiry breaking automation recurs repeatedly in 2026 discussions; this is a dated signal, not an adoption metric.

## Related
- meeting-app-automation.md
- desktop-notification-triage.md
- idle-detection.md
