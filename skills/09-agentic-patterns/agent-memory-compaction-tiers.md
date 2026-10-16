---
title: "Agent Memory Compaction Tiers"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Compact agent memory in tiers by summarizing aged turns, promoting stable facts, and recording what was dropped so context stays bounded without silent loss."
added: "2026-10"
version: v1
related: [agent-checkpoint-restore-patterns, agent-idle-wakeup-scheduling]
tags: [memory, compaction, context]
---
# Agent Memory Compaction Tiers

## Description
Compact agent memory in tiers by summarizing aged turns, promoting stable facts, and recording what was dropped so context stays bounded without silent loss. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A running context is near its budget and must shrink without losing commitments.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | agent memory compaction tiers task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent memory compaction tiers steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A compaction record with kept turns, promoted facts, and a dropped manifest. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def compact(turns, keep_last=2):
    return {"kept": turns[-keep_last:], "dropped": len(turns) - keep_last}
c = compact(["a", "b", "c", "d"])
assert c["kept"] == ["c", "d"] and c["dropped"] == 2
```

## Failure Modes
- Summarizing away an open commitment that a later turn still relies on.
- Compacting without recording which turns were dropped and why.
- Promoting an unverified claim into stable memory during compaction.
- Retrying without preserving state or evidence.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Tiered agent-memory compaction is a 2026 agent memory practice theme. ([public signal](https://mem0.ai/blog/state-of-ai-agent-memory-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [agent checkpoint restore patterns](../09-agentic-patterns/agent-checkpoint-restore-patterns.md)
- [agent idle wakeup scheduling](../09-agentic-patterns/agent-idle-wakeup-scheduling.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
