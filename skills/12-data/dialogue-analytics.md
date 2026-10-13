---
title: "Dialogue Analytics"
category: 12-data
level: advanced
stability: experimental
description: "Analyze conversation logs into structured metrics including resolution, turn counts, and escalation rates with provenance back to the source turns."
added: "2026-10"
version: v1
related: [data-summarization, funnel-analysis, statistical-analysis]
tags: [dialogue, analytics, metrics]
---

# Dialogue Analytics

## Description
Analyze conversation logs into structured metrics including resolution, turn counts, and escalation rates with provenance back to the source turns. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- conversation logs must be summarized into metrics that trace back to evidence.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for dialogue analytics work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the dialogue analytics steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def metrics(turns):
    return {
        'turns': len(turns),
        'resolved': turns[-1] == 'resolution',
        'escalations': sum(1 for t in turns if t == 'escalation'),
    }

m = metrics(['question', 'answer', 'resolution'])
assert m['resolved'] and m['escalations'] == 0
```

## Failure Modes
- Metrics with no link back to the source turns.
- Defining resolution so loosely most chats count as resolved.
- Ignoring censoring for conversations that never ended.
- Comparing periods with different traffic mixes.
- Reporting averages that hide a bimodal experience.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Conversation-log analytics requests recur in 2026 support-automation discussions; this is a dated signal, not an adoption metric.

## Related
- data-summarization.md
- funnel-analysis.md
- statistical-analysis.md
