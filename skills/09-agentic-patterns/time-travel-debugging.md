---
title: Time-Travel Debugging
category: 09-agentic-patterns
level: advanced
stability: stable
description: Rewind an agent run to any previous checkpoint, inspect state, modify it, and re-execute forward. Requires a checkpointer.
added: "2026-04"
version: v2
prerequisites:
  - 09-agentic-patterns/interruptible-agent-flows
---

# Time-Travel Debugging

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
history = list(app.get_state_history({"configurable": {"thread_id": "run-001"}}))
for snapshot in history:
    print(snapshot.config["configurable"]["checkpoint_id"], snapshot.values)

target = history[2].config
app.invoke(None, target)

app.update_state(target, {"result": "corrected value"})
app.invoke(None, target)
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| No checkpointer attached | Empty history | Always attach a checkpointer before debugging |
| Checkpoint store cleared | History unavailable | Use persistent store (SQLite/Postgres) not MemorySaver |
| State update breaks downstream nodes | New error path after fork | Run fork in a shadow thread_id first to validate |

## Related
- `interruptible-agent-flows.md` · `stateful-agent-graphs.md` · `thread-based-resume.md`

## Changelog
- v2 (2026-04): Full expansion
- v2.1 (2026-06): Added prerequisites field (INITIATIVE-005)
