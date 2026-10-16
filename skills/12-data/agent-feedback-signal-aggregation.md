---
title: "Agent Feedback Signal Aggregation"
category: 12-data
level: advanced
stability: experimental
description: "Aggregate user ratings, thumbs, retries, and escalations into one per-skill feedback record with counts and provenance, so improvement work follows recorded signals rather than anecdotes."
added: "2026-10"
version: v1
related: [session-replay-sampling, observability-span-taxonomies]
tags: [feedback, aggregation, signals]
---
# Agent Feedback Signal Aggregation

## Description
Aggregate user ratings, thumbs, retries, and escalations into one per-skill feedback record with counts and provenance, so improvement work follows recorded signals rather than anecdotes. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Improvement priorities must be ranked from recorded feedback instead of anecdotes.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | agent feedback signal aggregation task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent feedback signal aggregation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A per-skill feedback record with signal-type counts, time window, and provenance links. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def aggregate(signals):
    counts = {}
    for s in signals:
        key = (s["skill"], s["kind"])
        counts[key] = counts.get(key, 0) + 1
    return counts
out = aggregate([{"skill": "a", "kind": "thumb_up"}, {"skill": "a", "kind": "thumb_up"}])
assert out == {("a", "thumb_up"): 2}
```

## Failure Modes
- Mixing signals with different scales into one composite score.
- Counting retries as engagement instead of failure.
- Dropping signal provenance so counts cannot be audited.
- Retrying without preserving state or evidence.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Aggregated feedback signals are a recurring 2026 agent observability platform feature. ([public signal](https://laminar.sh/article/langfuse-alternatives-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [session replay sampling](../12-data/session-replay-sampling.md)
- [observability span taxonomies](../12-data/observability-span-taxonomies.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
