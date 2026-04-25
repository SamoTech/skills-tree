---
title: "Planning"
category: 02-reasoning
level: intermediate
stability: stable
added: "2025-03"
description: "Generate a typed, ordered plan from a goal — each step has an action, expected outcome, and a contingency, ready for an executor agent to consume."
version: v3
tags: [planning, decomposition, agent]
updated: "2026-04"
dependencies:
  - package: openai
    min_version: "1.0.0"
    tested_version: "2.31.0"
    confidence: verified
  - package: pydantic
    min_version: "2.0.0"
    tested_version: "2.13.0"
    confidence: verified
code_blocks:
  - id: "example-planning"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-planning.json)

# Planning

## Description

Turns a fuzzy human goal into a structured, executable plan: a typed list of steps where each step has an action, an expected outcome the executor can verify, and a contingency for when the action fails. The plan is the contract between the planner and the executor — typed, validated, and replannable.

## When to Use

- Long-horizon agent tasks (deploy a service, write a research report, run a data pipeline).
- You want plans that are **inspectable and editable by humans** before execution.
- You need a clear seam between planning and acting (Plan-and-Execute, HTN, ReWOO).

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `goal` | `str` | High-level objective |
| `constraints` | `list[str]` | Hard rules (budget, time, allowed tools) |
| → `plan.goal` | `str` | Echo of the goal for traceability |
| → `plan.steps[i].action` | `str` | What to do |
| → `plan.steps[i].expected_outcome` | `str` | How to know the step succeeded |
| → `plan.steps[i].contingency` | `str` | What to do on failure |

## Runnable Example

```python
# pip install openai pydantic
from __future__ import annotations
from openai import OpenAI
from pydantic import BaseModel, Field

client = OpenAI()

class Step(BaseModel):
    step_number: int = Field(ge=1)
    action: str
    expected_outcome: str
    contingency: str
    requires: list[int] = Field(default_factory=list,
        description="step_numbers this step depends on")

class Plan(BaseModel):
    goal: str
    steps: list[Step]

SYSTEM = """You are a planner. Produce a plan that:
- Has 3 to 8 steps.
- Each step is concrete and verifiable.
- Lists prerequisites in `requires` so the executor can parallelize.
- Includes a one-line contingency for each step.
Never include explanation outside the JSON schema."""

def plan_for(goal: str, constraints: list[str] | None = None) -> Plan:
    user = f"Goal: {goal}"
    if constraints:
        user += "\nConstraints:\n- " + "\n- ".join(constraints)
    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": user}],
        response_format=Plan,
    )
    return completion.choices[0].message.parsed

def topological(plan: Plan) -> list[Step]:
    """Verify the plan is a DAG and return steps in dependency order."""
    by_num = {s.step_number: s for s in plan.steps}
    visited: set[int] = set()
    order: list[Step] = []
    def visit(n: int, stack: set[int]) -> None:
        if n in stack:
            raise ValueError(f"cycle through step {n}")
        if n in visited:
            return
        stack.add(n)
        for r in by_num[n].requires:
            if r not in by_num:
                raise ValueError(f"step {n} requires unknown step {r}")
            visit(r, stack)
        stack.remove(n)
        visited.add(n)
        order.append(by_num[n])
    for n in by_num: visit(n, set())
    return order

if __name__ == "__main__":
    plan = plan_for(
        "Deploy a FastAPI app to a Linux VM with HTTPS",
        constraints=["Budget < $10/month", "No managed services"],
    )
    for s in topological(plan):
        print(f"{s.step_number}. {s.action}")
        print(f"   ✓ {s.expected_outcome}")
        print(f"   ⚠ {s.contingency}")
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Vague steps ("set up the server") | Schema doesn't enforce concreteness | Add a validator: action must contain a verb + concrete object |
| Hallucinated dependencies | `requires` references nonexistent step | Run `topological()` validator and reject |
| Plan over-constrains executor | Planner specifies _how_ instead of _what_ | System prompt: "describe outcomes, not commands" |
| No re-planning on failure | One-shot plan, no feedback loop | Pair with [reflection.md](../09-agentic-patterns/reflection.md): on failure, replan from the failed step |
| Cost: planner runs every turn | Re-using stale plans | Cache plan keyed by `(goal, constraints)` hash; reuse until a step fails |

## Variants

| Variant | Description | Best for |
|---|---|---|
| **Plan-and-Execute** | Plan once, execute, replan only on failure | Linear tasks |
| **Hierarchical (HTN)** | Top plan + sub-plans per step | Long, multi-domain tasks |
| **ReWOO** | Plan emits `#tool(args)` placeholders; executor resolves all in one pass | Cost-bounded agents |
| **Adaptive replanning** | Replan after every step | Dynamic environments |

## Frameworks & Models

| Framework | Implementation |
|---|---|
| OpenAI Structured Outputs | `response_format=Plan` (above) |
| LangGraph | Planner node → executor node loop |
| LlamaIndex | `LLMCompiler` agent |
| DSPy | `Plan(BaseModule)` typed signature |

## Model Comparison

| Capability | claude-opus-4-5 | gpt-4o | gemini-2.0-flash |
|---|---|---|---|
| Concrete, verifiable steps | 5 | 4 | 3 |
| Honest contingencies | 4 | 4 | 3 |
| JSON schema adherence | 5 | 5 | 4 |

## Related Skills

- [Task Decomposition](task-decomposition.md)
- [ReAct](../09-agentic-patterns/react.md)
- [Reflection](../09-agentic-patterns/reflection.md)
- [Goal Setting](goal-setting.md)

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial entry |
| 2026-02 | v2 | Pydantic schema + executor |
| 2026-04 | v3 | DAG validator, failure modes, model comparison, variants |
