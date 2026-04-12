# Plan and Execute

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Separate planning from execution: a Planner LLM creates a step-by-step task list, then an Executor agent carries out each step, potentially replanning when steps fail.

### Example

```
[Planner]
Goal: Research AI trends and write a report
Plan:
  1. Search for "AI trends 2025"
  2. Summarize top 5 results
  3. Outline a 500-word report
  4. Write the report
  5. Proofread and finalize

[Executor]
Step 1 → web_search(...) ✓
Step 2 → summarize(...) ✓
...
```

### Frameworks

- LangChain `Plan-and-Execute` agent
- LangGraph with planner + executor nodes

### Related Skills

- [ReAct](react.md)
- [Subagent Delegation](subagent-delegation.md)
- [Tool-Use Loop](tool-use-loop.md)
