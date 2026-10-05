---
title: "Context Compaction"
category: 03-memory
level: advanced
stability: experimental
description: "Compress long agent context while preserving active task state, user constraints, tool dependencies, and evidence required for correct continuation."
added: "2026-10"
version: v1
related: [short-term-memory, working-memory, state-machine]
tags: [memory, context, compression, compaction, long-running-agents]
---

# Context Compaction

## Description
Reduce an agent's active context when it approaches a configured budget while preserving the information required to continue correctly. Compaction must preserve active objectives, constraints, decisions, unresolved work, tool dependencies, authoritative evidence, and user-provided requirements while discarding redundant or safely recoverable history.

## When to Use
- Long-running agent sessions approach context limits.
- Tool-heavy workflows accumulate large outputs.
- Repeated context windows cause cost or latency pressure.
- An agent must continue work after a context boundary without restarting.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Conversation state, active task, completed actions, pending actions, evidence, dependencies, and context budget. |
| Outputs | Compact continuation state plus a deterministic record of what was retained, discarded, or made recoverable. |
| Invariant | The compacted state must not claim completion for unfinished work. |

## Procedure
1. Detect context pressure before the hard limit.
2. Identify active objective, constraints, current state, dependencies, evidence, and pending actions.
3. Preserve user requirements and facts needed to verify continuation.
4. Collapse redundant tool output and stale narration.
5. Prevent self-referential summaries from re-expanding the context.
6. Validate the compacted state against the active task before resuming.
7. If critical state cannot be preserved, stop and recover from an authoritative checkpoint instead of guessing.

## Runnable Example
```python
state = {"task": "deploy", "status": "in_progress", "evidence": ["tests-pass"]}
summary = {"active_task": state["task"], "status": state["status"], "evidence": state["evidence"]}
assert summary["status"] != "done"
print(summary)
```

## Failure Modes
- Repeated compaction with no net reduction.
- Loss of active task or user constraints.
- Dropped tool dependency causing incorrect continuation.
- Summary claims a step is complete when it is only planned.
- Full transcript repeatedly re-sent to the compression model, creating unnecessary cost.
- Compaction failure silently continues with an over-budget context.

## Recovery Boundary
Compaction is a state-preservation operation, not a license to infer missing facts. Missing critical state must produce BLOCKED or trigger an authoritative recovery mechanism.

## Evidence
Public 2026 agent issues document repeated compaction failures, context bloat, lost checkpoints, and substantial token/cost waste in long-running agent workflows. These are direct demand signals for reliable context-management behavior.

## Related
- short-term-memory.md
- working-memory.md
- long-term-memory.md
- state-machine.md
- retry-backoff.md
