# Blueprint: Multi-Agent Workflow

**Type:** `blueprint`  
**Pattern:** Orchestrator + Specialists  
**Complexity:** High  
**Status:** Production-Ready  
**Version:** v1

---

## Overview

A multi-agent system where an **orchestrator** agent decomposes tasks and delegates to **specialist** sub-agents in parallel or sequence, then aggregates results. This pattern handles tasks too complex for a single agent context window, or tasks requiring specialised tool sets.

---

## When to Use This Pattern

- Task naturally decomposes into independent parallel subtasks
- Different subtasks require different tools / system prompts
- Single-agent context would overflow (> 50K tokens of working memory)
- You want isolated failure domains (one sub-agent failing ≠ whole pipeline failing)

---

## Architecture

```
                     ┌──────────────────┐
                     │   ORCHESTRATOR   │
                     │                  │
  User Task ────────▶│ 1. Decompose     │
                     │ 2. Route         │
                     │ 3. Aggregate     │
                     │ 4. Synthesise    │
                     └────────┬─────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
  │  SPECIALIST A │  │  SPECIALIST B │  │  SPECIALIST C │
  │  (Research)   │  │  (Code)       │  │  (Write)      │
  │               │  │               │  │               │
  │  web_search   │  │  code_exec    │  │  text_format  │
  │  fetch_url    │  │  file_write   │  │  translate    │
  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘
          │                  │                   │
          └──────────────────┴───────────────────┘
                             │
                     ┌───────▼───────┐
                     │ ORCHESTRATOR  │
                     │  (aggregate)  │
                     └───────────────┘
```

---

## Implementation (LangGraph)

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class WorkflowState(TypedDict):
    task: str
    subtasks: list[dict]
    results: Annotated[list, operator.add]  # Fan-in: results accumulated
    final_report: str

# Orchestrator: decompose task into subtasks
def orchestrate(state: WorkflowState) -> WorkflowState:
    subtasks = llm_decompose(state["task"])  # returns [{agent, prompt}, ...]
    return {**state, "subtasks": subtasks}

# Fan-out: create a node per subtask dynamically
def make_specialist(agent_type: str):
    def run(state: WorkflowState) -> WorkflowState:
        # Each specialist has its own tools + system prompt
        result = run_specialist_agent(agent_type, state)
        return {**state, "results": [result]}
    return run

# Aggregator: synthesise all results
def aggregate(state: WorkflowState) -> WorkflowState:
    report = llm_synthesise(state["task"], state["results"])
    return {**state, "final_report": report}

build = StateGraph(WorkflowState)
build.add_node("orchestrate", orchestrate)
build.add_node("research", make_specialist("research"))
build.add_node("code", make_specialist("code"))
build.add_node("write", make_specialist("write"))
build.add_node("aggregate", aggregate)

build.set_entry_point("orchestrate")
build.add_edge("orchestrate", "research")
build.add_edge("orchestrate", "code")
build.add_edge("orchestrate", "write")
build.add_edge("research", "aggregate")
build.add_edge("code", "aggregate")
build.add_edge("write", "aggregate")
build.add_edge("aggregate", END)

workflow = build.compile()
```

---

## Orchestration Strategies

| Strategy | Description | Use When |
|---|---|---|
| **Sequential** | A → B → C, each uses prior output | Strict dependencies between steps |
| **Parallel fan-out** | A, B, C run simultaneously | Independent subtasks |
| **Map-reduce** | Same agent runs on N chunks, results merged | Large document processing |
| **Debate** | Two agents produce competing answers, judge picks | High-stakes decisions |
| **Hierarchical** | Orchestrator orchestrates sub-orchestrators | Very complex multi-domain tasks |

---

## Failure Handling

```python
def safe_specialist(agent_type: str, state: WorkflowState,
                    timeout: float = 30.0) -> dict:
    import asyncio
    try:
        return asyncio.wait_for(
            run_specialist_agent(agent_type, state), timeout=timeout
        )
    except asyncio.TimeoutError:
        return {"agent": agent_type, "result": None,
                "error": "timeout", "status": "failed"}
    except Exception as e:
        return {"agent": agent_type, "result": None,
                "error": str(e), "status": "failed"}
```

---

## Cost Profile

| Config | Agents | Avg Tokens/Run | Est. Cost |
|---|---|---|---|
| Small (3 specialists) | 4 | 15K | ~$0.23 |
| Medium (5 specialists) | 6 | 30K | ~$0.45 |
| Large (10 specialists) | 11 | 80K | ~$1.20 |

---

## Related

- [Blueprint: RAG Stack](rag-stack.md)
- [System: Research Agent](../systems/research-agent.md)
- [Skill: Task Decomposition](../skills/02-reasoning/task-decomposition.md)
- [Skill: Planning](../skills/02-reasoning/planning.md)
