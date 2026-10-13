---
name: message-queue-consuming
description: Consume messages from queues with acknowledgment semantics, poison-message handling, and at-least-once idempotency so replays cannot corrupt state.
metadata:
  source: skills/04-action-execution/message-queue-consuming.md
  category: 04-action-execution
  version: "v1"
---

# Message Queue Consuming

## Description
Consume messages from queues with acknowledgment semantics, poison-message handling, and at-least-once idempotency so replays cannot corrupt state. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- work arrives through a queue and duplicates or poison messages must be handled before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for message queue consuming work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the message queue consuming steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def process_with_dedupe(msg, seen):
    if msg["id"] in seen:
        return "duplicate"
    seen.add(msg["id"])
    if msg["body"] is None:
        return "poison"
    return "processed"

seen = set()
assert process_with_dedupe({"id": 1, "body": "x"}, seen) == "processed"
assert process_with_dedupe({"id": 1, "body": "x"}, seen) == "duplicate"
assert process_with_dedupe({"id": 2, "body": None}, seen) == "poison"
```

## Failure Modes
- Acknowledging before processing completes.
- Retrying poison messages forever without a dead-letter path.
- Assuming exactly-once delivery from the broker.
- Losing the dedupe store across restarts.
- Blocking the consumer on one bad message.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Reliable event-driven agent actions are a recurring 2026 production request signal in public coverage; this is a dated signal, not an adoption metric.

## Related
- message-queue-publishing.md
- idempotent-retries.md
- background-job-submission.md
