---
title: "Goal Decomposition"
category: 02-reasoning
level: intermediate
stability: stable
description: "Break a high-level user intent or agent objective into a hierarchy of sub-goals, clarifying ambiguities and establishing measurable success criteria at each level before execution begins."
added: "2025-06"
version: v2
tags: [reasoning, planning, goals, decomposition]
updated: "2026-06"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-goal-decomposition.json)

# Goal Decomposition

## Description

Goal Decomposition operates at the **intent level**: before any tool is called or plan is generated, the agent clarifies and breaks down the user's objective into a hierarchy of sub-goals. This is distinct from Planning Decomposition (which produces executable tasks) and from Task Decomposition (which operates on already-specified tasks).

Used in:
- **BabyAGI:** The task-creation agent generates sub-goals from a primary objective
- **LangGraph SubGraph:** Nested graphs representing decomposed goal trees
- **AutoGen:** Nested chat patterns where a UserProxyAgent sends sub-goals to specialised agents
- **GPT-Researcher:** Research question decomposition before search

## When to Use

- The user's request is ambiguous or multi-dimensional.
- Achieving the main goal requires achieving prerequisite sub-goals first.
- You want explicit success criteria at each level (not just the final answer).
- **Don't use** for simple, well-specified requests where goal is already clear.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `user_intent` | `str` | Raw user objective |
| `context` | `str` | Available context about the domain |
| → `goal_tree` | `dict` | Hierarchical goal decomposition |
| → `success_criteria` | `list[str]` | Measurable criteria per sub-goal |

## Runnable Example

```python
import json
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-opus-4-5"

GOAL_DECOMP_PROMPT = """Decompose the user intent into a goal tree.
Output JSON: {"main_goal": str, "sub_goals": [{"id": str, "goal": str, "success_criteria": str, "depends_on": []}]}
Max 5 sub-goals. Be concrete and measurable.

User intent: {intent}
Context: {context}"""

def goal_decomposition(user_intent: str, context: str = "") -> dict:
    resp = client.messages.create(
        model=MODEL, max_tokens=1024,
        messages=[{"role": "user", "content": GOAL_DECOMP_PROMPT.format(
            intent=user_intent, context=context or "No additional context"
        )}]
    )
    text = resp.content[0].text.strip()
    start = text.find("{")
    end = text.rfind("}") + 1
    return json.loads(text[start:end])

if __name__ == "__main__":
    result = goal_decomposition(
        user_intent="Help me learn machine learning and get a job in AI",
        context="User has Python experience, no ML background, 6 months available"
    )
    print("Main goal:", result["main_goal"])
    for sg in result["sub_goals"]:
        print(f"  [{sg['id']}] {sg['goal']} | Done when: {sg['success_criteria']}")
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Goals too abstract | Model doesn't add measurability | Require `success_criteria` in schema |
| Infinite goal recursion | Model decomposes sub-goals again | Limit decomposition to 2 levels |
| Missing dependency edges | Model skips prerequisite relationships | Post-validate: all non-leaf goals have at least one dependency |

## Production Applications

- **G01 Coding Agent:** Decompose "build a REST API" into: design, implement endpoints, add auth, add tests
- **G02 Research Agent:** Decompose research question into information needs before retrieval
- **G08 Multi-Agent Systems:** Root goal tree drives agent specialisation decisions

## Related Skills

- [Planning Decomposition](planning-decomposition.md) — converts sub-goals into executable tasks
- [Least-to-Most Prompting](least-to-most.md) — reasoning technique for decomposition
- [Plan-and-Execute](../09-agentic-patterns/plan-and-execute.md) — executes the resulting plan
- [Memory-Augmented Agent](../09-agentic-patterns/memory-augmented-agent.md) — tracks progress against goal tree

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-06 | v1 | Initial skill file |
| 2026-06 | v2 | Full runnable example, structured output, failure modes |
