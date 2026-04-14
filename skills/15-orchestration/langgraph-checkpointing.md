---
title: "LangGraph Checkpointing"
category: 15-orchestration
level: intermediate
stability: stable
description: "Persist agent graph state at every step using LangGraph checkpointers for fault tolerance and resumability."
added: "2026-04"
version: v2
---

# LangGraph Checkpointing
Category: orchestration | Level: intermediate | Stability: stable | Version: v2

## Description
LangGraph checkpointers save a snapshot of the graph state after every node execution into a persistent store (in-memory, SQLite, PostgreSQL, or Redis). Each snapshot is associated with a `thread_id`, enabling the graph to resume from any prior checkpoint. This powers fault tolerance, human-in-the-loop interruption, and time-travel debugging. Without a checkpointer, graph state is ephemeral and lost on crash.

## Inputs
- `checkpointer`: instance of `MemorySaver`, `SqliteSaver`, or `AsyncPostgresSaver`
- `thread_id`: string identifier that scopes the checkpoint history
- `graph`: compiled `StateGraph` with `checkpointer` set at compile time
- `config`: `{"configurable": {"thread_id": "..."}}` passed to `graph.invoke()`

## Outputs
- State persisted after every node to the backing store
- `graph.get_state(config)` returns latest `StateSnapshot`
- `graph.get_state_history(config)` returns full checkpoint history

## Example
```python
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict

class State(TypedDict):
    messages: list[str]

def node_a(state): return {"messages": state["messages"] + ["step A"]}
def node_b(state): return {"messages": state["messages"] + ["step B"]}

graph = StateGraph(State)
graph.add_node("a", node_a)
graph.add_node("b", node_b)
graph.add_edge("a", "b")
graph.set_entry_point("a")

app = graph.compile(checkpointer=MemorySaver())
config = {"configurable": {"thread_id": "run-001"}}
result = app.invoke({"messages": []}, config)
print(result)
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| No `thread_id` in config | `ValueError` on invoke | Always pass `thread_id` in `configurable` dict |
| SQLite file locked (concurrent runs) | Write failures | Use PostgreSQL checkpointer for concurrent workloads |
| State schema mismatch after code update | Deserialization error | Version your state schema and migrate checkpoints |

## Prompt Patterns
**Basic:** `"Use MemorySaver for development, SqliteSaver for single-instance production."`

**Chain-of-Thought:** `"Choose checkpointer based on: (1) concurrency needs, (2) persistence requirements, (3) team infra."`

**Constrained Output:** `"Always pass thread_id; never call graph.invoke() without a config dict."`

## Model Comparison
| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---|---|---|---|
| Graph code generation | ✅ Strong | ✅ Very Strong | ⚠️ Moderate |
| LangGraph API accuracy | ✅ High | ✅ High | ⚠️ Hallucinations on new API |
| Checkpoint strategy advice | ✅ Good | ✅ Good | ⚠️ Generic answers |
| Debug suggestion quality | ✅ Strong | ✅ Strong | ⚠️ Shallow |
| Cost | Moderate | Moderate | Low |

## Related
- `stateful-agent-graphs.md` · `thread-based-resume.md` · `human-approval-gates.md` · `time-travel-debugging.md` · `agent-sessions.md`

## Changelog
- v2 (2026-04): Full expansion
