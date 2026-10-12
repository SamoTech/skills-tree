---
title: "Idempotent Retries"
category: 04-action-execution
level: intermediate
stability: experimental
description: "Make retries safe by designing operations to be idempotent — client-generated keys, state checks before effect, and receiver-side dedupe — before any retry loop runs."
added: "2026-10"
version: v1
related: ["api-call", "webhook-handling"]
---

# Idempotent Retries

Category: Action Execution | Level: intermediate | Stability: experimental | Version: v1

## Description

A retry that re-applies a side effect is worse than the original failure: duplicate charges, double sends, repeated writes. This skill makes an operation idempotent before retrying it — the caller attaches a stable operation key, the receiver dedupes, and the effect happens once regardless of how many attempts the network takes.

## When to Use

Use for any operation with side effects that might be retried — payments, emails, writes, external state changes — especially across network boundaries where timeouts make outcomes ambiguous.

Do not retry a non-idempotent operation; make it idempotent first or refuse the retry.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `operation` | `callable` | Yes | The side-effecting operation to make retryable |
| `key` | `string` | Yes | Client-generated stable operation key |
| `receiver` | `map` | No | Receiver state for dedupe, when modeling the remote side |

## Procedure

1. Generate the operation key once per logical operation, before the first attempt, and reuse it on every retry.
2. Design the receiver to dedupe on the key: return the original result for a repeated key instead of re-applying the effect.
3. Check current state before applying the effect — the operation may already have succeeded on a previous attempt.
4. Retry only on retryable failures — timeouts and transient errors — with exponential backoff and a stated attempt cap.
5. Treat ambiguous outcomes, such as a timeout after send, as pending rather than failed: resolve by querying the receiver with the key before retrying.
6. Record the operation key in the audit trail so duplicates are explainable after the fact.

## Outputs

| Output | Type | Description |
|---|---|---|
| `effect` | `map` | The single applied effect with its operation key |
| `attempts` | `list` | Per-attempt outcome and timing |
| `audit` | `map` | Key, result, and dedupe decisions for the operation |

## Runnable Example

```python
def apply_once(receiver, key, effect):
    if key in receiver["applied"]:
        return {"status": "already-applied", "result": receiver["applied"][key]}
    receiver["applied"][key] = effect()
    return {"status": "applied", "result": receiver["applied"][key]}

receiver = {"applied": {}}
print(apply_once(receiver, "op-1", lambda: "receipt-42"))
print(apply_once(receiver, "op-1", lambda: "receipt-42"))
print(sorted(receiver["applied"]))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Re-applied effects | A retry re-runs a non-idempotent operation | Dedupe on a stable operation key |
| Key churn | A new key per attempt defeats dedupe | Generate the key once per logical operation |
| Retry on permanent errors | Deterministic failures are retried to the cap | Retry only transient failure classes |
| Ambiguous treated as failed | A timeout after send triggers a duplicate | Resolve pending state by query before retrying |
| Unlogged keys | Duplicates are unexplainable in audit | Record keys and dedupe decisions |

## Security and Authority Boundary

Operation keys are integrity anchors rather than secrets, but they must be unguessable enough that a third party cannot pre-claim a key and suppress someone else operation. Generate them from a cryptographically secure source.

## Evidence

This skill is grounded in dated public implementation references:

1. The Stripe API documentation on idempotent requests (https://docs.stripe.com/api/idempotent_requests).
2. Wikipedia's overview of idempotence (https://en.wikipedia.org/wiki/Idempotence).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [API Call](api-call.md) — the network layer whose timeouts make idempotency necessary.
- [Webhook Handling](webhook-handling.md) — the delivery path where at-least-once delivery requires dedupe.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
