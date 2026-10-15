---
name: graph-state-machine-agent-design
description: Design agents as explicit state machines with typed nodes, edges, and checkpointable state for production control.
metadata:
  source: skills/09-agentic-patterns/graph-state-machine-agent-design.md
  category: 09-agentic-patterns
  version: "v1"
---

# Graph State Machine Agent Design

## Description
Design agents as explicit state machines with typed nodes, edges, and checkpointable state for production control. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires graph state machine agent design before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for graph state machine agent design. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the graph state machine agent design steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def next_node(graph, node, result):
    return graph[node][result]
g = {"start": {"ok": "end", "retry": "start"}}
assert next_node(g, "start", "ok") == "end"
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Graph-based stateful agent frameworks lead 2026 production framework comparisons. These are dated public signals, not adoption metrics.

## Related
- planning.md
- multi-step-planning.md
- agent-checkpointing.md
