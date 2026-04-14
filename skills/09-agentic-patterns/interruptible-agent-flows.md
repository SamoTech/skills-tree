---
title: "Interruptible Agent Flows"
category: 09-agentic-patterns
level: intermediate
stability: stable
description: "Design agent graphs that can pause, wait for external signals, and resume cleanly."
added: "2026-04"
version: v2
---

# Interruptible Agent Flows
Category: agentic-patterns | Level: intermediate | Stability: stable | Version: v2

## Description
Interruptible flows allow an agent graph to suspend mid-execution, persist state, and resume later — with or without human intervention. LangGraph implements this via `interrupt_before` / `interrupt_after` on specific nodes, combined with a checkpointer. The pattern is essential for long-running tasks, human-in-the-loop workflows, async pipelines, and any process where execution may span minutes or hours.

## Inputs
- `interrupt_before`: node names where the graph suspends before execution
- `interrupt_after`: node names where the graph suspends after execution
- `checkpointer`: persistent store (SQLite/Postgres)
- `thread_id`: run identity for resume
- `resume_value`: optional state update injected on resume

## Outputs
- `GraphInterrupt` exception surfaced to the caller when the graph pauses
- Persisted state snapshot at the interrupt point
- Resumed execution on next `invoke()` with same `thread_id`

## Example
```python
from langgraph.types import interrupt

def human_review_node(state):
    decision = interrupt("Review this action: " + state["pending_action"])
    return {"approved": decision}

app = graph.compile(checkpointer=MemorySaver())
config = {"configurable": {"thread_id": "task-99"}}
app.invoke({"pending_action": "delete user data"}, config)
# → GraphInterrupt raised

# Later, resume with decision
app.invoke(Command(resume=True), config)
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| No notification on interrupt | External system waits forever | Trigger webhook/event on `GraphInterrupt` catch |
| Resume with wrong thread_id | Graph restarts from scratch | Store thread_id durably tied to the originating request |
| Interrupt inside a nested subgraph | Resume skips subgraph state | Use `interrupt_before` on the parent node instead |

## Prompt Patterns
**Basic:** `"Use interrupt() inside nodes that need external decisions."`

**Chain-of-Thought:** `"Map all wait points → use interrupt_before for pre-node, interrupt() inside node for mid-execution."`

**Constrained Output:** `"Always catch GraphInterrupt at the application layer and persist the thread_id."`

## Model Comparison
| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---|---|---|---|
| Interrupt pattern design | ✅ Strong | ✅ Very Strong | ⚠️ Moderate |
| Resume logic accuracy | ✅ Reliable | ✅ Reliable | ⚠️ Confused by Command API |
| Error handling guidance | ✅ Good | ✅ Strong | ⚠️ Generic |
| LangGraph version awareness | ✅ Current | ✅ Current | ⚠️ May reference old API |
| Cost | Moderate | Moderate | Low |

## Related
- `human-approval-gates.md` · `langgraph-checkpointing.md` · `thread-based-resume.md` · `stateful-agent-graphs.md`

## Changelog
- v2 (2026-04): Full expansion
