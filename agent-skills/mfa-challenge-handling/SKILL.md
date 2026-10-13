---
name: mfa-challenge-handling
description: Handle multi-factor authentication challenges during automated web flows with a declared factor policy, secure factor storage rules, and fail-closed handling.
metadata:
  source: skills/11-web/mfa-challenge-handling.md
  category: 11-web
  version: "v1"
---

# MFA Challenge Handling

## Description
Handle multi-factor authentication challenges during automated web flows with a declared factor policy, secure factor storage rules, and fail-closed handling. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an automated login flow must pass MFA without weakening the factor policy.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for mfa challenge handling work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the mfa challenge handling steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def handle_challenge(factor_available, policy):
    if policy == 'strict' and len(factor_available) < 2:
        return 'fail-closed'
    return 'satisfied' if factor_available else 'fail-closed'

assert handle_challenge(['app'], 'strict') == 'fail-closed'
assert handle_challenge(['app', 'backup'], 'strict') == 'satisfied'
```

## Failure Modes
- Weakening or disabling MFA to make automation easier.
- Storing factor material in plaintext logs or code.
- Passing on a weaker factor than the declared policy.
- Not failing closed when the factor source is unavailable.
- Assuming a challenge passed without verifying the session state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
MFA handling for automation with fail-closed policies recurs in 2026 agent security discussions; this is a dated signal, not an adoption metric.

## Related
- web-oauth-flow-handling.md
- web-login.md
- captcha-solving.md
