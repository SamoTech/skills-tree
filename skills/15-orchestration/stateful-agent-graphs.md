---
title: "Stateful Agent Graphs"
category: 15-orchestration
level: intermediate
stability: stable
description: "Model multi-step agent workflows as directed graphs with typed shared state using LangGraph StateGraph."
added: "2026-04"
version: v2
---

# Stateful Agent Graphs
Category: orchestration | Level: intermediate | Stability: stable | Version: v2

## Description
LangGraph's `StateGraph` models agentic workflows as a directed graph where each node is a Python function that reads and writes to a shared typed state object. Edges can be fixed or conditional. The graph is compiled into a runnable that accepts an initial state and produces a final state, with each intermediate state persisted if a checkpointer is attached.

## Inputs
- `State`: `TypedDict` or Pydantic model defining graph state schema
- `nodes`: dict of node-name → function mapping
- `edges`: fixed (`add_edge`) or conditional (`add_conditional_edges`) connections
- `entry_point`: first node to execute
- `checkpointer`: optional, for persistence

## Outputs
- Final `State` dict after all nodes execute
- Per-node state deltas accessible via checkpointer

## Example
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    query: str
    result: str
    needs_search: bool

def classify(state):
    return {"needs_search": "weather" in state["query"].lower()}

def search(state):
    return {"result": f"Weather result for: {state['query']}"}

def respond(state):
    return {"result": state.get("result", "Answer from knowledge base.")}

graph = StateGraph(AgentState)
graph.add_node("classify", classify)
graph.add_node("search", search)
graph.add_node("respond", respond)
graph.set_entry_point("classify")
graph.add_conditional_edges("classify", lambda s: "search" if s["needs_search"] else "respond")
graph.add_edge("search", "respond")
graph.add_edge("respond", END)

app = graph.compile()
print(app.invoke({"query": "What is the weather today?", "result": "", "needs_search": False}))
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| Node mutates state directly | Unpredictable state | Always return a new dict from node functions; never mutate in-place |
| Missing edge for conditional branch | `GraphError` | Test all conditional branches with unit assertions |
| State key typo | `KeyError` at runtime | Use `TypedDict` with strict type checking |

## Prompt Patterns
**Basic:** `"Design a StateGraph with classify → route → respond nodes."`

**Chain-of-Thought:** `"Map each decision point to a conditional edge and each action to a node."`

**Constrained Output:** `"Each node function must return only the keys it modifies, not the full state."`

## Model Comparison
| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---|---|---|---|
| StateGraph design | ✅ Strong | ✅ Very Strong | ⚠️ Moderate |
| Conditional edge logic | ✅ Reliable | ✅ Reliable | ⚠️ Errors on complex conditions |
| TypedDict generation | ✅ Clean | ✅ Clean | ✅ Good |
| Error diagnosis | ✅ Strong | ✅ Strong | ⚠️ Shallow |
| Cost | Moderate | Moderate | Low |

## Related
- `langgraph-checkpointing.md` · `human-approval-gates.md` · `interruptible-agent-flows.md` · `time-travel-debugging.md`

## Changelog
- v2 (2026-04): Full expansion
