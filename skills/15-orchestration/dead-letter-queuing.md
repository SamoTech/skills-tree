---
title: "Dead-Letter Queuing"
category: 15-orchestration
level: intermediate
stability: experimental
description: "Route repeatedly failing messages to a dedicated dead-letter queue with full failure metadata so poison payloads are quarantined for inspection instead of blocking the pipeline or vanishing."
added: "2026-10"
version: v1
related: ["task-queue", "retry-backoff"]
---

# Dead-Letter Queuing

Category: Orchestration | Level: intermediate | Stability: experimental | Version: v1

## Description

Some messages cannot be processed, and retrying them forever converts one bad payload into a stuck pipeline. Dead-letter queuing draws the line: after a bounded number of attempts, the message moves to a dedicated dead-letter queue carrying its attempts, errors, and original payload. The main queue keeps flowing, the failure stays inspectable, and a replay path exists for after the cause is fixed.

## When to Use

Use with any task queue or event pipeline where a malformed or failing message must not block subsequent messages.

Do not use a dead-letter queue as a trash bin: entries are quarantined pending diagnosis, and unbounded growth without review hides an outage in plain sight.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `message` | `payload + id` | Yes | The message being processed |
| `max_attempts` | `number` | Yes | Processing attempts before dead-lettering |
| `attempt_log` | `list[(time, error)]` | Yes | Prior failures for this message id |
| `dlq` | `queue` | Yes | The dead-letter destination with its metadata schema |

## Procedure

1. Track attempts per message id; the count travels with the message, not with worker memory.
2. On each failure, record the error and timestamp; retry only while under the attempt bound.
3. At the bound, move the message to the dead-letter queue with its payload, attempts, and error history attached.
4. Surface dead-letter depth and entry age as operational alarms; a growing dead-letter queue is a failing pipeline.
5. Diagnose entries before replay: fix the consumer or correct the payload, then replay deliberately.
6. Re-run replayed messages through the same accounting so a still-failing replay dead-letters again, visibly.

## Outputs

| Output | Type | Description |
|---|---|---|
| `route` | `processed | retried | dead_lettered` | Disposition of the message |
| `dlq_entry` | `map | null` | The quarantined message with metadata when dead-lettered |
| `attempts` | `number` | Attempts made before the disposition |

## Runnable Example

```python
def route_message(msg, attempt_log, max_attempts=3):
    """Dead-letter a message after bounded attempts."""
    if msg["ok"]:
        return {"route": "processed"}
    attempts = len(attempt_log) + 1
    if attempts >= max_attempts:
        return {
            "route": "dead_lettered",
            "dlq_entry": {"id": msg["id"], "attempts": attempts,
                          "errors": [error for _, error in attempt_log] + [msg["error"]]},
        }
    return {"route": "retried", "attempts": attempts}

failures = [(1, "timeout"), (2, "timeout")]
print(route_message({"id": "job-9", "ok": False, "error": "timeout"}, failures))
print(route_message({"id": "job-1", "ok": False, "error": "timeout"}, failures[:1]))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Infinite retry | No attempt bound on failing messages | Count attempts per id and enforce the bound |
| Silent drop | Failures discarded without a dead-letter queue | Every non-processed message lands somewhere inspectable |
| Unreviewed backlog | The dead-letter queue grows with no alarm watching it | Alarm on depth and oldest entry age |
| Blind replay | Messages replayed before the cause is fixed | Fix first, replay deliberately, re-account on failure |
| Metadata loss | Entry stored without errors or attempt count | Attach payload, attempts, and error history to the entry |

## Security and Authority Boundary

The dead-letter queue quarantines and preserves; it does not diagnose. Root-cause analysis, payload correction, and the decision to replay remain operator work, with the quarantine treated as evidence, not as a fix.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of dead-letter queues (https://en.wikipedia.org/wiki/Dead_letter_queue).
2. The RabbitMQ documentation on dead-letter exchanges (https://www.rabbitmq.com/docs/dlx).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Task Queue](task-queue.md) — the primary queue whose flow the dead-letter path protects.
- [Retry Backoff](retry-backoff.md) — the bounded retry policy that precedes dead-lettering.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
