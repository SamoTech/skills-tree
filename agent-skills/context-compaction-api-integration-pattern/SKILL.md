---
name: context-compaction-api-integration-pattern
description: Integrate provider context-compaction into an agent loop while preserving task-critical state and verification checkpoints.
metadata:
  source: skills/09-agentic-patterns/context-compaction-api-integration-pattern.md
  category: 09-agentic-patterns
  version: "v1"
---

# Context Compaction API Integration Pattern

## Description
Integrate provider context-compaction into an agent loop while preserving task-critical state and verification checkpoints. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent loop consumes provider context compaction to stay in budget.
- Task-critical state must survive compaction events.
- Compaction boundaries must be observable, not silent.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The conversation state, the provider compaction events, and the task state registry. |
| Outputs | A compaction ledger naming each compaction event and state recovery verdict. |
| Safety | Fail closed by pausing the loop when a compaction event drops registered task state. |

## Procedure
1. Register task-critical state keys before the loop starts.
2. Observe provider compaction events as explicit loop checkpoints.
3. After each compaction, verify registered state keys are still recoverable.
4. Rebuild recoverable state from durable records, not from compacted text.
5. Pause the loop when a registered key cannot be recovered.
6. Emit the compaction ledger naming each event and recovery verdict.

## Outputs
| Area | Contract |
|---|---|
| Primary | A compaction ledger naming each compaction event and state recovery verdict. |
| Verification | Registered keys and recovery runs that reproduce the ledger. |
| Failure | A fail-closed pause report naming the unrecoverable state key. |

## Runnable Example
```python
def after_compaction(context, registry):
    missing = [k for k in registry if k not in context]
    return {"pause": bool(missing), "missing": missing}
ctx = {"task_goal": "ship", "acceptance": "tests-green"}
reg = ["task_goal", "acceptance", "budget"]
r = after_compaction(ctx, reg)
assert r["pause"] and r["missing"] == ["budget"]
assert after_compaction({k: 1 for k in reg}, reg)["pause"] is False
```

## Failure Modes
- Compaction events are unobserved, so state loss is discovered late.
- Task state is rebuilt from compacted summaries instead of durable records.
- The loop continues after registered state keys disappear.
- Registration is optional, so critical state silently drops.
- The ledger records only compaction counts, not recovery verdicts.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI DevDay 2026 brought context compaction from Codex into the Agents API for application builders (OpenAI DevDay 2026 Recap, dated November 5, 2026) ([public signal](https://openai.com/index/devday-2026-recap/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Context Engineering](context-engineering.md)
- [Agent Memory Compaction Tiers](agent-memory-compaction-tiers.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
