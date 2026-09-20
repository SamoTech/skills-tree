---
title: Time-travel Debugging
category: 09-agentic-patterns
level: advanced
stability: stable
description: "Rewind an agent run to a prior checkpoint, inspect or modify state, and re-execute from that point while preserving checkpoint identity and separating diagnostic forks from production runs."
added: "2026-04"
version: v2
prerequisites:
  - 09-agentic-patterns/interruptible-agent-flows
related: [interruptible-agent-flows, stateful-agent-graphs, thread-based-resume]
---

# Time-travel Debugging

## Description
Time-travel debugging replays a stateful agent graph from a recorded checkpoint instead of repeating earlier work.
A checkpointer is required to inspect history. State edits create a diagnostic fork and should not silently mutate the original production run.
The exact checkpoint API depends on the graph runtime; the example below uses the LangGraph interface already described by this skill.

## Inputs / Outputs
| Input | Type | Contract |
|---|---|---|
| `app` | graph runtime | Compiled stateful graph with a configured checkpointer |
| `thread_id` | `str` | Identifier for the run history |
| `checkpoint_id` | `str` | Existing checkpoint identifier |
| `state_update` | `dict | None` | Optional controlled state patch |

| Output | Type | Contract |
|---|---|---|
| `history` | iterable | Ordered checkpoint snapshots |
| `replay_result` | runtime-defined | Result of execution from the selected checkpoint |
| `fork_config` | mapping | Configuration identifying the diagnostic replay context |

## Reference Workflow
```python
# Requires an already-compiled stateful graph named `app` with a checkpointer.
config = {"configurable": {"thread_id": "run-001"}}
history = list(app.get_state_history(config))
assert history, "checkpoint history is required"

target = history[2].config
print(target["configurable"]["checkpoint_id"])

# Replay without changing the stored checkpoint.
replay = app.invoke(None, target)

# If a correction is required, apply it only in a controlled diagnostic fork.
fork = dict(target)
fork["configurable"] = dict(target["configurable"])
fork["configurable"]["thread_id"] = "debug-run-001"
app.update_state(fork, {"result": "corrected value"})
replayed_fork = app.invoke(None, fork)
```

## Diagnostic Protocol
1. Capture the production `thread_id` and checkpoint identifier.
2. Verify that the checkpoint exists before replaying.
3. Replay the unmodified checkpoint first to establish a baseline.
4. Create a separate diagnostic thread before mutating state.
5. Record the state patch and reason for the fork.
6. Compare the forked result with the baseline.
7. Never overwrite production state merely to make a test pass.

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| No checkpointer | Empty history | Configure persistent or test checkpointer before execution |
| Checkpoint deleted | History unavailable | Retain checkpoints required by the operational debugging policy |
| Invalid state patch | Downstream node failure | Validate state schema before `update_state` |
| Fork shares production identity | Production history is mutated | Use a distinct diagnostic `thread_id` |
| Non-deterministic external tool | Replay diverges | Stub or record external effects when reproducibility matters |

## Reproducibility Limits
Checkpoint replay restores graph state, not the external world.
HTTP responses, clocks, random seeds, model outputs, databases, and tool side effects can differ unless captured or stubbed.
A replay should therefore report which external inputs were restored and which were live.

## Validation Rules
- The target checkpoint must exist before replay.
- Diagnostic state changes must use a distinct run identity.
- State patches must conform to the graph's state contract.
- Replay results must not be presented as identical to production unless external effects were controlled.
- Checkpoint identifiers and state changes should be recorded for auditability.

## Security Boundaries
Checkpoint state can contain prompts, tool arguments, secrets, or user data.
Do not expose checkpoint contents to unauthorized users, logs, or model prompts merely for debugging convenience.
State patches must not be allowed to bypass authorization or approval gates.

## Provenance
The workflow is runtime-specific at the API boundary and intentionally does not pin a LangGraph release here.
The conceptual guarantees are checkpoint lookup, controlled state replay, and diagnostic isolation; verify exact runtime APIs against the deployed version.

## Related
- `interruptible-agent-flows.md` — pause/resume control
- `stateful-agent-graphs.md` — persistent graph state
- `thread-based-resume.md` — resuming a prior run

## Changelog
- v2 (2026-04): Full expansion
- v2.1 (2026-06): Added prerequisites field
- v2 (2026-09-20): Added explicit I/O contract, diagnostic-fork protocol, reproducibility limits, security boundaries, and validation rules
