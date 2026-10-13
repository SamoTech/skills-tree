---
name: signed-webhook-verification
description: Verify webhook signatures before processing, reject stale or replayed deliveries, and process events idempotently after verification passes.
metadata:
  source: skills/04-action-execution/signed-webhook-verification.md
  category: 04-action-execution
  version: "v1"
---

# Signed Webhook Verification

## Description
Verify webhook signatures before processing, reject stale or replayed deliveries, and process events idempotently after verification passes. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- incoming webhook events must be authenticated before any state change before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for signed webhook verification work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the signed webhook verification steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
import hmac, hashlib, time

def verify(sig, body, secret, now, max_age=300):
    expected = hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected):
        return False
    ts = int(body.split("ts=")[1])
    return now - ts <= max_age

secret = "k"
body = "event=done&ts=%d" % (1000,)
sig = hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()
assert verify(sig, body, secret, 1100) is True
assert verify("0" * 64, body, secret, 1100) is False
assert verify(sig, body, secret, 2000) is False  # stale
```

## Failure Modes
- Processing before verifying the signature.
- Using non-constant-time comparison.
- Ignoring timestamp windows so replays succeed.
- Reprocessing the same delivery id twice.
- Falling back to unsigned mode when verification fails.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Signed event delivery is a recurring 2026 integration security requirement in public coverage; this is a dated signal, not an adoption metric.

## Related
- webhook-handling.md
- idempotent-retries.md
- notification-parsing.md
