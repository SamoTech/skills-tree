---
title: "Plan-and-Execute"
category: 09-agentic-patterns
level: intermediate
stability: stable
added: "2025-03"
description: "Apply plan-and-execute pattern in AI agent workflows."
dependencies:
  - package: langgraph
    min_version: "0.2.0"
    tested_version: "1.1.6"
    confidence: verified
  - package: langchain-openai
    min_version: "0.1.0"
    tested_version: "1.1.12"
    confidence: verified
  - package: pydantic
    min_version: "2.0.0"
    tested_version: "2.13.0"
    confidence: verified
code_blocks:
  - id: "example-plan-execute"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-plan-and-execute.json)

# Plan-and-Execute

**Category:** `agentic-patterns`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

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
