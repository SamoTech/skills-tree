---
title: "Planning Decomposition"
category: 02-reasoning
level: advanced
stability: stable
description: "Break a complex agent goal into an ordered sequence of actionable sub-tasks, each with clear inputs, outputs, and success criteria. The cognitive foundation for plan-and-execute, LangGraph pipelines, and CrewAI task breakdown."
added: "2025-06"
version: v2
tags: [reasoning, planning, decomposition, agent-design]
updated: "2026-06"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-planning-decomposition.json)

# Planning Decomposition

## Description

Planning Decomposition is the cognitive skill of converting a high-level objective into an explicit, ordered plan of sub-tasks that an agent (or multi-agent system) can execute sequentially or in parallel. It is the reasoning backbone behind:

- **LangGraph** state graphs where each node is a decomposed task
- **CrewAI** task sequences with explicit agent assignments
- **AutoGen** conversation-driven planning where a Planner agent decomposes before Executors act
- **BabyAGI** task-creation loops

Planning Decomposition differs from Goal Decomposition (which operates at the intent/objective level) by producing **actionable, executable steps** with tool bindings, not just sub-goals.

## When to Use

- The agent goal requires more than 3 sequential tool calls.
- Sub-tasks can be independently validated (each has a clear done condition).
- Different sub-tasks may be parallelisable across sub-agents.
- **Don't use** for single-shot tasks; the planning overhead is not justified.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `goal` | `str` | High-level objective |
| `available_tools` | `list[str]` | Tool names the agent can use |
| → `plan` | `list[Task]` | Ordered sub-tasks with tool bindings |
| → `dependencies` | `dict` | Task dependency graph |

## Runnable Example

```python
import json
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-opus-4-5"

PLAN_PROMPT = """You are a planning agent. Decompose the goal into actionable sub-tasks.
For each task output JSON with: id, description, tool, inputs, depends_on.
Output a JSON array. No prose.

Goal: {goal}
Available tools: {tools}"""

def planning_decomposition(goal: str, tools: list[str]) -> list[dict]:
    resp = client.messages.create(
        model=MODEL, max_tokens=1024,
        messages=[{"role": "user", "content": PLAN_PROMPT.format(
            goal=goal, tools=", ".join(tools)
        )}]
    )
    text = resp.content[0].text.strip()
    # Extract JSON array
    start = text.find("[")
    end = text.rfind("]") + 1
    return json.loads(text[start:end])

if __name__ == "__main__":
    plan = planning_decomposition(
        goal="Research the top 3 Python web frameworks and write a comparison report",
        tools=["web_search", "url_reader", "document_writer"]
    )
    for task in plan:
        print(f"{task['id']}: {task['description']} [{task.get('tool', 'none')}]")
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Over-decomposition (20+ tasks) | Model is too granular | Set max tasks constraint in prompt |
| Tasks have circular dependencies | Weak dependency reasoning | Post-process with cycle detection |
| Tool hallucination (uses unavailable tools) | Model invents tools | Strictly enumerate available tools |
| Missing success criteria | Vague task descriptions | Require `done_condition` field in JSON schema |

## Production Applications

- **G01 Coding Agent:** Decompose feature requests into: research, design, implement, test steps
- **G08 Multi-Agent Systems:** Assign decomposed tasks to specialised sub-agents via CrewAI/AutoGen
- **G02 Research Agent:** Structure multi-source research into search, read, synthesise, report tasks

## Related Skills

- [Plan-and-Execute](../09-agentic-patterns/plan-and-execute.md) — the agentic pattern that executes decomposed plans
- [Goal Decomposition](goal-decomposition.md) — operates at intent level; precedes planning decomposition
- [Least-to-Most Prompting](least-to-most.md) — reasoning-level analogue
- [ReAct Pattern](../09-agentic-patterns/react-pattern.md) — executes individual plan steps
- [Subagent Delegation](../09-agentic-patterns/subagent-delegation.md) — assigns plan tasks to sub-agents

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-06 | v1 | Initial skill file |
| 2026-06 | v2 | Full runnable example, failure modes, production applications |
