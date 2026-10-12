---
name: agent-checkpointing
description: Persist an agent run as resumable checkpoints — state, memory, pending actions — so a failure or restart continues from a recorded point instead of from scratch.
metadata:
  source: skills/09-agentic-patterns/agent-checkpointing.md
  category: 09-agentic-patterns
  version: "v1"
---

# Agent Checkpointing

Category: Agentic Patterns | Level: intermediate | Stability: experimental | Version: v1

## Description

A long agent run that cannot resume is a long agent run that will eventually be repeated. This skill treats the run as a sequence of durable states: after each completed step, the run writes a checkpoint — conversation state, working memory, pending tool calls — and a restart restores the latest one before doing anything else. The design question is granularity: checkpoints cost writes, and restarts cost rework, so the checkpoint cadence is chosen by what re-execution is actually allowed to cost.

## When to Use

Use for long-running or stateful agent work — multi-step plans, sessions holding tool state, pipelines vulnerable to timeout or restart.

Do not checkpoint every intermediate token of fast, cheap runs; when re-execution costs less than persistence, the checkpoint is pure overhead.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `run_state` | `map` | Yes | Conversation, memory, and pending actions to persist |
| `cadence` | `enum` | Yes | Checkpoint after every step, on demand, or on a schedule |
| `restore_policy` | `enum` | Yes | Latest checkpoint, or a specific recorded point |

## Procedure

1. Choose the checkpoint unit — step, tool call, or plan stage — based on what re-execution of that unit is allowed to cost.
2. Serialize complete state, not deltas alone: a checkpoint that needs every prior checkpoint to restore is a chain, not a checkpoint.
3. Write the checkpoint atomically, so a crash mid-write leaves the previous checkpoint intact rather than a torn one.
4. On restart, restore the latest checkpoint first and reconcile with reality — replay tool side effects only where the tool contract allows it.
5. Version the checkpoint schema; a restored run must refuse to continue on a state format it cannot fully interpret.
6. Prune old checkpoints on a retention rule, and record the retention decision so the pruning is explainable later.

## Outputs

| Output | Type | Description |
|---|---|---|
| `checkpoints` | `list` | Durable run states with timestamps and step markers |
| `resume_point` | `map` | The checkpoint a restart continues from |

## Runnable Example

```python
import json

class RunStore:
    def __init__(self):
        self.checkpoints = []

    def save(self, state):
        record = {"step": state["step"], "state": state}
        self.checkpoints.append(json.dumps(record))

    def latest(self):
        if not self.checkpoints:
            return None
        return json.loads(self.checkpoints[-1])["state"]

store = RunStore()
store.save({"step": 1, "plan": "gather facts"})
store.save({"step": 2, "plan": "gather facts", "found": 3})
print("resuming from step:", store.latest()["step"])
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Torn writes | A crash during checkpoint serialization | Write atomically; keep the previous checkpoint valid |
| Delta-only state | Restoring requires the entire history | Serialize complete state per checkpoint |
| Stale resume | Restored state disagrees with the world it mutated | Reconcile with external state before continuing |
| Unversioned schema | A restored run misreads an old format | Version schemas and refuse unknown formats |
| Checkpoint storms | Persisting on every token, starving the work | Choose cadence by re-execution cost |

## Security and Authority Boundary

A checkpoint is a complete, portable copy of agent state — credentials in working memory get persisted with it, so checkpoints must inherit the encryption and access scope of the run itself, and the pruning policy must respect data-retention obligations, not just disk budgets.

## Evidence

This skill is grounded in dated public implementation references:

1. The arXiv paper on human-in-the-loop agent oversight (https://arxiv.org/abs/2503.13657).
2. The NIST AI Risk Management Framework overview (https://www.nist.gov/itl/ai-risk-management-framework).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Time-Travel Debugging](time-travel-debugging.md) — inspecting past run states recorded by checkpoints.
- [Interruptible Agent Flows](interruptible-agent-flows.md) — the pause mechanism checkpoints formalize.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
