---
title: "Webhook Handling"
category: 04-action-execution
level: intermediate
stability: experimental
description: "Verify webhook deliveries with an HMAC signature over raw request bytes, reject replays outside a bounded window, and dispatch events idempotently so duplicate deliveries cause no double effects."
added: "2026-10"
version: v1
related: ["http-request", "api-call", "retry-backoff"]
---

# Webhook Handling

Category: Action Execution | Level: intermediate | Stability: experimental | Version: v1

## Description

Webhooks are the entry point for external systems to trigger effects, which makes them a double risk: an unverified sender can forge events, and a redelivered event can double-charge or double-create. This skill defines the handling contract: verify a signature computed over the raw request bytes, bound the replay window, and dispatch idempotently by event identity. It covers verification and dispatch; handler business logic stays in its own skills.

## When to Use

Use when a service accepts event callbacks from an external platform and a forged or duplicated delivery would cause a wrong effect.

Do not use for outgoing API calls or polling; the request and API-call skills fit those boundaries.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `raw_body` | `bytes` | Yes | The exact request bytes the signature was computed over |
| `signature` | `string` | Yes | Received signature from the delivery headers |
| `signing_key` | `bytes` | Yes | Shared key used to compute the expected signature |
| `replay_window` | `integer` | Yes | Maximum tolerated age of a delivery in seconds |
| `seen_events` | `set` | Yes | Durable record of already-dispatched event identities |

## Procedure

1. Read the raw request bytes before any parsing; re-serialization changes the bytes the signature covers.
2. Compute the expected HMAC over the raw bytes and compare with a constant-time comparison; reject on mismatch.
3. Check the delivery timestamp against the replay window before any handler runs.
4. Derive a stable event identity and check it against the seen set; duplicates are acknowledged, not dispatched.
5. Dispatch to the handler registry only after verification and identity checks pass, in that order.
6. Record the event identity durably in the same step that applies the effect, so a crash cannot split them.
7. Acknowledge the delivery only after the handler reports success; failed handlers return a retryable error to the sender.
8. Alert on verification failures at a threshold; repeated failures are an attack signal, not noise.

## Outputs

| Output | Type | Description |
|---|---|---|
| `decision` | `string` | ACCEPTED, DUPLICATE, STALE, or REJECTED with the failing check |
| `dispatched` | `boolean` | Whether a handler ran for this delivery |
| `event_id` | `string` | The stable identity used for deduplication |
| `failure_reason` | `string` | The check that failed, when the delivery was rejected |

## Runnable Example

```python
import hashlib
import hmac

def verify_webhook(raw_body, received_signature, signing_key):
    """Verify an HMAC-SHA256 signature computed over the raw request bytes."""
    expected = hmac.new(signing_key, raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, received_signature)

def dispatch(event_id, handlers, seen, replay_window, age_seconds):
    """Dispatch a verified event at most once inside the replay window."""
    if age_seconds > replay_window:
        return "REJECTED - outside replay window"
    if event_id in seen:
        return "SKIPPED - duplicate delivery"
    seen.add(event_id)
    handler = handlers.get(event_id.split(":")[0])
    if handler is None:
        return "DISPATCHED - no handler registered"
    return handler(event_id)

body = b'{"event": "checkout.completed"}'
signature = hmac.new(b"whsec_demo", body, hashlib.sha256).hexdigest()
print(verify_webhook(body, signature, b"whsec_demo"))
print(dispatch("order:1", {"order": lambda event: "order processed"}, set(), 300, 5))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Verification bypass | The signature is compared after JSON parsing | Verify over the raw bytes with a constant-time compare |
| Replay attack | The delivery timestamp is unchecked | Bound the replay window and check it before dispatch |
| Double dispatch | The seen set is updated after the effect | Record the event identity atomically with the effect |
| Key leakage | The signing key sits in code or logs | Hold keys in declared secret storage and never log them |
| Silent drop | Verification failures are logged nowhere | Alert on verification failures at a threshold |

## Security and Authority Boundary

Verifying a webhook signature grants no authority beyond the sender’s declared events. The signing key is a credential: it lives in the runtime’s declared secret storage, is never embedded in code or logs, and rotates on the platform’s schedule. Verified events still pass through the handler’s own permission checks before any effect.

## Evidence

This skill is grounded in dated public implementation references:

1. GitHub’s guide to validating webhook deliveries (https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries).
2. Python’s hmac module documentation (https://docs.python.org/3/library/hmac.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [HTTP Request](http-request.md) — performs outbound requests; this skill guards the inbound delivery path.
- [API Call](api-call.md) — invokes external APIs; this skill receives their event callbacks.
- [Retry Backoff](../15-orchestration/retry-backoff.md) — bounds sender-side retries; this skill bounds receiver-side replays.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
