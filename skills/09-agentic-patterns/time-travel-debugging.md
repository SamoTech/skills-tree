---
title: "Time-Travel Debugging"
category: 09-agentic-patterns
level: advanced
stability: stable
description: "Replay and fork a LangGraph agent run from any prior checkpoint to diagnose and fix failures."
added: "2026-04"
version: v2
---

# Time-Travel Debugging
Category: agentic-patterns | Level: advanced | Stability: stable | Version: v2

## Description
Time-travel debugging lets you rewind an agent run to any previous checkpoint, inspect the state, modify it, and re-execute forward from that point. LangGraph exposes this via `graph.get_state_history(config)` to list all checkpoints, and `graph.invoke(None, config_with_checkpoint_id)` to replay from a specific one. This is invaluable for debugging complex multi-step failures without re-running expensive earlier steps.

## Inputs
- `config`: `{"configurable": {"thread_id": "...", "checkpoint_id": "..."}}` for a specific checkpoint
- `checkpointer`: must be attached for history to exist
- `state_update`: optional dict to inject corrected values before re-execution

## Outputs
- Full list of `StateSnapshot` objects from `get_state_history()`
- Re-executed graph result from the target checkpoint forward

## Example
```python
# List all checkpoints for a run
history = list(app.get_state_history({"configurable": {"thread_id": "run-001"}}))
for snapshot in history:
    print(snapshot.config["configurable"]["checkpoint_id"], snapshot.values)

# Replay from a specific checkpoint
target = history[2].config
app.invoke(None, target)

# Fork: update state then replay
app.update_state(target, {"result": "corrected value"})
app.invoke(None, target)
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| No checkpointer attached | Empty history | Always attach a checkpointer before debugging |
| Checkpoint store cleared | History unavailable | Use persistent store (SQLite/Postgres) not MemorySaver |
| State update breaks downstream nodes | New error path after fork | Run fork in a shadow thread_id first to validate |

## Prompt Patterns
**Basic:** `"List checkpoints, find the failure point, then replay from the checkpoint before it."`

**Chain-of-Thought:** `"Walk backwards through history, identify the last known-good state, update incorrect values, replay."`

**Constrained Output:** `"Fork into a new thread_id (append -debug) to avoid polluting the production run history."`

## Model Comparison
| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---|---|---|---|
| Debugging strategy quality | ✅ Strong | ✅ Very Strong | ⚠️ Generic |
| LangGraph history API knowledge | ✅ Accurate | ✅ Accurate | ⚠️ May hallucinate method names |
| Fork/branch advice | ✅ Good | ✅ Good | ⚠️ Shallow |
| State mutation safety guidance | ✅ Careful | ✅ Very Careful | ⚠️ Misses edge cases |
| Cost | Moderate | Moderate | Low |

## Related
- `langgraph-checkpointing.md` · `stateful-agent-graphs.md` · `thread-based-resume.md` · `interruptible-agent-flows.md`

## Changelog
- v2 (2026-04): Full expansion
