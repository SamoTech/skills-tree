---
title: "Plan-and-Execute Pattern"
category: 09-agentic-patterns
level: intermediate
stability: stable
description: "Apply plan and execute in AI agent workflows."
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-plan-and-execute.json)

# Plan-and-Execute Pattern

### Description
Separates planning from execution using two distinct LLM roles: a **Planner** that generates a complete multi-step plan upfront, and an **Executor** that carries out each step sequentially, feeding results back for optional replanning. This separation allows the planner to reason globally while the executor focuses on single-step tool use, reducing context bloat and improving reliability on long-horizon tasks.

### When to Use
- Tasks requiring more than 5 sequential steps with dependencies
- Workflows where upfront resource allocation or conflict detection is needed
- Multi-agent systems where different specialists execute different plan steps
- Tasks that frequently require replanning due to uncertain environments

### Example
```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import List, Optional

class PlanExecuteState(BaseModel):
    goal: str
    plan: List[str] = []
    current_step: int = 0
    results: List[str] = []
    final_answer: Optional[str] = None

planner_llm = ChatOpenAI(model="gpt-4o", temperature=0)
executor_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def planner(state: PlanExecuteState) -> PlanExecuteState:
    prompt = f"Create a numbered step-by-step plan to: {state.goal}\nPrevious results: {state.results}"
    r = planner_llm.invoke(prompt)
    steps = [l.strip() for l in r.content.split("\n") if l.strip() and l[0].isdigit()]
    state.plan = steps
    state.current_step = 0
    return state

def executor(state: PlanExecuteState) -> PlanExecuteState:
    if state.current_step >= len(state.plan):
        state.final_answer = "\n".join(state.results)
        return state
    step = state.plan[state.current_step]
    r = executor_llm.invoke(f"Execute this step and return the result: {step}\nContext: {state.results[-3:]}")
    state.results.append(r.content)
    state.current_step += 1
    return state

graph = StateGraph(PlanExecuteState)
graph.add_node("planner", planner)
graph.add_node("executor", executor)
graph.set_entry_point("planner")
graph.add_edge("planner", "executor")
graph.add_conditional_edges("executor", lambda s: END if s.final_answer else "executor")
app = graph.compile()
```

### Advanced Techniques
- **Adaptive replanning**: after each step, score whether the result deviates significantly from the expected output; trigger the planner if score < threshold
- **Parallel execution**: identify independent plan steps and execute them concurrently with `asyncio.gather`
- **Planner specialization**: use a larger reasoning model (o3) for planning, a smaller fast model (4o-mini) for execution
- **Plan validation**: after generating the plan, pass it to a critic agent to check for logical errors before execution begins

### Related Skills
- `planning`, `task-decomposition`, `react`, `subagent-delegation`, `lats`, `critic-agent`
