---
title: Plan-and-Execute
category: 09-agentic-patterns
level: intermediate
stability: stable
description: Separate planning from execution — a planner LLM generates a task list upfront, then an executor agent works through each step.
added: "2025-03"
version: v1.2
prerequisites:
  - 09-agentic-patterns/react
  - 02-reasoning/planning-decomposition
---

# Plan-and-Execute

### Description

Separate planning from execution: a planner LLM generates a task list upfront, then an executor agent works through each step, optionally replanning when steps fail.

### Example

```python
# pip install langgraph langchain-openai pydantic
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import List, Optional

class AgentState(BaseModel):
    goal: str
    plan: List[str] = []
    current_step: int = 0
    results: List[str] = []
    final_answer: Optional[str] = None

planner_llm = ChatOpenAI(model="gpt-4o")
executor_llm = ChatOpenAI(model="gpt-4o-mini")

def planner(state: AgentState) -> AgentState:
    response = planner_llm.invoke(f"Create a step-by-step plan for: {state.goal}. Return only numbered steps.")
    steps = [line.strip() for line in response.content.split("\n") if line.strip() and line[0].isdigit()]
    state.plan = steps
    return state

def executor(state: AgentState) -> AgentState:
    if state.current_step >= len(state.plan):
        state.final_answer = "\n".join(state.results)
        return state
    step = state.plan[state.current_step]
    result = executor_llm.invoke(f"Execute this step: {step}")
    state.results.append(result.content)
    state.current_step += 1
    return state

def should_continue(state: AgentState) -> str:
    return END if state.final_answer else "executor"

graph = StateGraph(AgentState)
graph.add_node("planner", planner)
graph.add_node("executor", executor)
graph.set_entry_point("planner")
graph.add_edge("planner", "executor")
graph.add_conditional_edges("executor", should_continue, {END: END, "executor": "executor"})
app = graph.compile()

result = app.invoke(AgentState(goal="Research and summarize the benefits of RAG"))
print(result["final_answer"])
```

### Related Skills
- `react`, `planning`, `stateful-agent-graphs`, `agent-handoffs`

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial entry |
| 2026-06 | v1.1 | Added prerequisites field (INITIATIVE-005) |
| 2026-06-23 | v1.2 | Added prerequisite: 02-reasoning/planning-decomposition (INITIATIVE-009, C-003) |
