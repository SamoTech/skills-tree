---
name: short-lived-credential-acquisition
description: Acquire short-lived credentials through the provider flow, verify scopes and expiry before use, and fail closed rather than falling back to static keys.
metadata:
  source: skills/04-action-execution/short-lived-credential-acquisition.md
  category: 04-action-execution
  version: "v1"
---

# Short-Lived Credential Acquisition

## Description
Acquire short-lived credentials through the provider flow, verify scopes and expiry before use, and fail closed rather than falling back to static keys. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an action needs a scoped, expiring credential instead of a stored key before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for short lived credential acquisition work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the short lived credential acquisition steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def usable(credential, now):
    if credential["expiry"] <= now:
        return False, "expired"
    if "write" not in credential["scopes"]:
        return False, "missing write scope"
    return True, "ok"

now = 100
assert usable({"expiry": 200, "scopes": ["read", "write"]}, now) == (True, "ok")
assert usable({"expiry": 50, "scopes": ["write"]}, now)[0] is False
assert usable({"expiry": 200, "scopes": ["read"]}, now)[0] is False
```

## Failure Modes
- Falling back to a long-lived key when the flow fails.
- Using credentials past their expiry window.
- Requesting broader scopes than the task needs.
- Caching tokens without a refresh plan.
- Logging the credential while debugging the flow.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Short-lived, scoped agent credentials are a recurring 2026 agent-identity signal in public coverage; this is a dated signal, not an adoption metric.

## Related
- env-vars.md
- api-call.md
- action-precondition-checking.md
