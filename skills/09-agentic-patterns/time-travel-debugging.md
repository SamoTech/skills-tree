---
title: Time-Travel Debugging
category: 09-agentic-patterns
level: advanced
stability: stable
description: Rewind an agent run to a previous durable checkpoint, inspect the recorded state, optionally fork corrected state, and replay forward without re-executing the earlier prefix.
added: "2026-04"
version: v3
prerequisites:
  - 09-agentic-patterns/interruptible-agent-flows
---

# Time-Travel Debugging

## Description
Time-travel debugging is checkpoint-based replay for stateful agent graphs. It separates the original execution history from a deliberate fork, allowing an engineer to inspect a known checkpoint, change state, and replay downstream nodes.

This skill assumes the graph runtime exposes durable checkpoints and stable thread identifiers. It does not reconstruct state that was never persisted, and it does not guarantee that replay is identical when nodes depend on wall-clock time, random values, external services, mutable files, or non-deterministic model responses.

Use it to diagnose a failed branch, validate a corrected state transition, or reproduce a historical execution without paying the cost of recomputing the prefix.

## Inputs
- `app`: graph/application object with checkpoint history support.
- `thread_id`: identifier for the execution history.
- `checkpoint_id`: optional target checkpoint; otherwise inspect history first.
- `state_update`: optional patch to apply before replay.
- `fork_thread_id`: recommended separate identifier for experiments.

## Outputs
- Ordered checkpoint snapshots for the selected thread.
- Target checkpoint configuration.
- Replay result from the selected checkpoint.
- A separately identifiable fork when state is modified.

## Reference workflow
```python

def list_checkpoints(app, thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    return list(app.get_state_history(config))


def replay_checkpoint(app, snapshot):
    return app.invoke(None, snapshot.config)


history = list_checkpoints(app, "run-001")
if not history:
    raise RuntimeError("no durable checkpoints available")

target = history[0]
print("checkpoint", target.config["configurable"].get("checkpoint_id"))
result = replay_checkpoint(app, target)
print(result)
```

## Fork-and-correct pattern
```python
history = list(app.get_state_history({"configurable": {"thread_id": "run-001"}}))
target = history[2]

fork_config = {
    "configurable": {
        "thread_id": "debug-fork-001",
        "checkpoint_id": target.config["configurable"]["checkpoint_id"],
    }
}

app.update_state(fork_config, {"result": "corrected value"})
result = app.invoke(None, fork_config)
```

The exact checkpoint and update APIs vary by runtime version. Validate the installed API before execution and never assume that a checkpoint identifier is portable across stores.

## Contract
| Condition | Required behavior | Invariant |
|---|---|---|
| Durable history exists | Enumerate checkpoints | Target is traceable |
| Target checkpoint missing | Fail explicitly | No silent fallback |
| Debugging without mutation | Replay original checkpoint | Original history remains unchanged |
| State correction | Prefer a new thread/fork | Original execution remains auditable |
| External side effect during replay | Require idempotency or isolation | No accidental duplicate side effects |
| Non-deterministic dependency | Record the limitation | Replay is not claimed identical |

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| No checkpointer | Empty history | Attach a durable checkpointer before execution |
| Checkpoint store expired | Target unavailable | Retain required checkpoints in persistent storage |
| Invalid checkpoint ID | Lookup/replay failure | Enumerate history and select an existing ID |
| State patch violates schema | Downstream node failure | Validate state before replay |
| External side effect repeats | Duplicate write/request | Use idempotency keys, mocks, or a side-effect gate |
| Time/randomness changes | Divergent replay | Record clocks/seeds or classify replay as non-deterministic |
| Model output changes | Different branch behavior | Pin model/configuration where reproducibility matters |

## Safety boundaries
Do not replay production side effects merely to inspect state. Prefer a sandbox or forked thread for corrective experiments. Treat checkpoint contents as sensitive application state and enforce the same access controls as the live execution. A checkpoint is evidence of a prior state, not proof that its values are still correct.

## Observability requirements
Record thread ID, checkpoint ID, graph/version identifier, state patch, operator intent, and replay outcome. Keep the original checkpoint immutable. When a fork is promoted into production, record the reason and validation evidence separately from the historical run.

## Frameworks
| Framework | Method |
|---|---|
| LangGraph | `get_state_history`, checkpoint-aware `invoke`, `update_state` |
| Durable workflow runtimes | Equivalent checkpoint enumeration and replay APIs |

## Related
- `interruptible-agent-flows.md`
- `stateful-agent-graphs.md`
- `thread-based-resume.md`
- `human-approval-gates.md`

## Changelog
- v2 (2026-04): Full expansion
- v2.1 (2026-06): Added prerequisites field
- v3 (2026-09): Added fork isolation, side-effect safety, reproducibility limits, observability requirements, and deterministic contracts.
