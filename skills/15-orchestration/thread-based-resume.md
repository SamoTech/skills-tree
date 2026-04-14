---
title: "Thread-Based Resume"
category: 15-orchestration
level: intermediate
stability: stable
description: "Resume a paused or crashed LangGraph agent from its last checkpoint using thread IDs."
added: "2026-04"
version: v2
---

# Thread-Based Resume
Category: orchestration | Level: intermediate | Stability: stable | Version: v2

## Description
In LangGraph, every run is scoped to a `thread_id`. When a graph is interrupted (by `interrupt_before`, a human approval gate, or a crash), you can resume it by calling `graph.invoke(None, config)` with the same `thread_id`. The graph replays from the last saved checkpoint, skipping already-completed nodes. This makes long-running agent tasks resilient to transient failures.

## Inputs
- `thread_id`: string identifying the conversation or task run
- `config`: `{"configurable": {"thread_id": "..."}}` dict
- `resume_input`: `None` to continue, or new state delta to inject before resuming
- `checkpointer`: must be attached to the compiled graph

## Outputs
- Continued graph execution from last checkpoint
- Final `State` after completion

## Example
```python
# Initial run — graph interrupts before 'approval' node
app.invoke({"task": "deploy prod"}, config, interrupt_before=["approval"])

# Human reviews...
# Resume after approval
app.invoke(None, config)  # Continues from 'approval' node
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| `thread_id` not found in store | Graph starts fresh | Verify checkpointer store is persistent across restarts |
| State schema evolved since checkpoint | Deserialization error | Add migration logic for state schema changes |
| Resume input overwrites critical state | Wrong execution path | Validate resume input against state schema before invoking |

## Prompt Patterns
**Basic:** `"Always use a stable thread_id tied to the task or conversation ID."`

**Chain-of-Thought:** `"On resume, verify the last checkpoint state before injecting new input."`

**Constrained Output:** `"Pass None as input when resuming unless you need to inject corrected state."`

## Model Comparison
| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---|---|---|---|
| Resume pattern understanding | ✅ Strong | ✅ Strong | ⚠️ Moderate |
| State injection advice | ✅ Accurate | ✅ Accurate | ⚠️ Vague |
| Error diagnosis on resume | ✅ Good | ✅ Strong | ⚠️ Limited |
| LangGraph API knowledge | ✅ Current | ✅ Current | ⚠️ May lag |
| Cost | Moderate | Moderate | Low |

## Related
- `langgraph-checkpointing.md` · `human-approval-gates.md` · `interruptible-agent-flows.md` · `stateful-agent-graphs.md`

## Changelog
- v2 (2026-04): Full expansion
