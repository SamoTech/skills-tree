---
name: event-sourced-projections
description: Build deterministic read models from event streams with replayable projection state and gap detection between source and projection.
metadata:
  source: skills/12-data/event-sourced-projections.md
  category: 12-data
  version: "v1"
---

# Event-Sourced Projections

## Description
Build deterministic read models from event streams with replayable projection state and gap detection between source and projection. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a read model must be rebuildable from the event stream and provably in sync.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for event-sourced projections work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the event-sourced projections steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def project(events, start=0):
    balance = start
    for kind, amount in events:
        if kind == 'credit':
            balance += amount
        elif kind == 'debit':
            balance -= amount
        else:
            raise ValueError('unknown event kind')
    return balance

assert project([('credit', 10), ('debit', 4)]) == 6
```

## Failure Modes
- A projection that cannot be rebuilt from the event log.
- No gap detection between stream position and projection state.
- Replaying events in arrival order instead of sequence order.
- Silently swallowing unknown event kinds during replay.
- Assuming eventual consistency without measuring the lag.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Replayable projections with gap detection appear in 2026 event-driven architecture discussions; this is a dated signal, not an adoption metric.

## Related
- change-data-capture.md
- stream-processing.md
- data-lineage.md
