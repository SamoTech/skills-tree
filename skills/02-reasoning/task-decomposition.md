---
title: "Task Decomposition"
category: 02-reasoning
level: intermediate
stability: stable
description: "Split a complex task into a structured, ordered list of subtasks small enough that a single LLM call (or tool call) reliably solves each one."
added: "2025-03"
version: v3
tags: [planning, decomposition, agent]
updated: "2026-04"
dependencies:
  - package: anthropic
    min_version: "0.39.0"
    tested_version: "0.39.0"
    confidence: verified
  - package: pydantic
    min_version: "2.5.0"
    confidence: verified
code_blocks:
  - id: "example-decomp"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-task-decomposition.json)

# Task Decomposition

## Description

Decomposition is the **first move** of any non-trivial agent task: break the user's goal into 3–10 atomic subtasks the executor can dispatch independently. Distinct from [Planning](planning.md) — decomposition produces *what* to do, planning adds *order, deps, constraints*.

Done well, decomposition shrinks the per-call solution space, lets you parallelise independent work, and gives you a clean unit to retry / verify / cache. Done badly, you get vague subtasks ("research the topic") that don't actually reduce difficulty.

## When to Use

- The user request is too large to answer in one model call.
- You want to run subtasks in parallel.
- You need an audit trail of "what the agent decided to do" before it does it.
- For trivial tasks (single API call, single lookup), skip — decomposition adds latency and tokens for no gain.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `goal` | `str` | The user's high-level objective |
| `context` | `str` | Optional facts the agent already knows |
| `min_subtasks` | `int` | Reject decompositions smaller than this |
| `max_subtasks` | `int` | Reject decompositions larger than this |
| → `subtasks` | `list[Subtask]` | Each: `id`, `title`, `expected_output`, `inputs_from` |

## Runnable Example

```python
# pip install anthropic pydantic
from __future__ import annotations
import json
from typing import Literal
from pydantic import BaseModel, Field, ValidationError
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-opus-4-5"

class Subtask(BaseModel):
    id: str = Field(description="Stable kebab-case identifier")
    title: str = Field(description="Imperative one-line action")
    expected_output: str = Field(description="What this subtask must produce")
    inputs_from: list[str] = Field(default_factory=list,
                                   description="ids of subtasks this depends on")
    kind: Literal["research", "transform", "synthesize", "act"] = "transform"

class Decomposition(BaseModel):
    goal: str
    subtasks: list[Subtask]

SYS = (
    "You decompose a user goal into 3–8 atomic subtasks. Each subtask must be "
    "small enough that a single skilled assistant can complete it in one shot. "
    "Output ONLY JSON matching this schema: "
    "{goal, subtasks: [{id, title, expected_output, inputs_from, kind}]}."
)

def decompose(goal: str, *, context: str = "",
              min_subtasks: int = 3, max_subtasks: int = 8) -> Decomposition:
    user = f"GOAL:\n{goal}\n\nCONTEXT:\n{context or '(none)'}"
    r = client.messages.create(
        model=MODEL, max_tokens=1024, system=SYS,
        messages=[{"role": "user", "content": user}],
    )
    raw = r.content[0].text.strip()
    # Strip ```json fences if model added them
    if raw.startswith("```"):
        raw = raw.strip("`").lstrip("json").strip()
    try:
        d = Decomposition.model_validate_json(raw)
    except ValidationError as e:
        raise ValueError(f"decomposition failed validation: {e}\n\nRAW:\n{raw}")
    if not (min_subtasks <= len(d.subtasks) <= max_subtasks):
        raise ValueError(f"got {len(d.subtasks)} subtasks; need {min_subtasks}–{max_subtasks}")
    # ID uniqueness
    ids = [s.id for s in d.subtasks]
    if len(set(ids)) != len(ids):
        raise ValueError(f"duplicate subtask ids: {ids}")
    return d

if __name__ == "__main__":
    out = decompose("Write a launch announcement blog post for our new SDK.")
    print(json.dumps(out.model_dump(), indent=2))
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Vague subtasks ("understand the problem") | System prompt didn't enforce concrete `expected_output` | Require & validate non-empty `expected_output`; reject if it's a verb only |
| Too few subtasks (single call wrapped in JSON) | Model thinks the goal is trivial | Enforce `min_subtasks` lower bound and re-ask |
| Too many micro-tasks ("write word 1, write word 2") | No upper bound | Enforce `max_subtasks`; nudge with "atomic, not granular" |
| Cyclic dependencies | `inputs_from` references later sibling | Validate as DAG (topological sort, see [Planning](planning.md)) |
| Hallucinated subtasks unrelated to goal | Cold-start, no context | Always include context block, even empty |

## Variants

| Variant | When to use |
|---|---|
| **Sequential** | Linear pipeline (research → draft → edit) |
| **Parallel** | Independent subtasks (analyze 4 documents in parallel) |
| **Hierarchical (HTN)** | Subtasks themselves get decomposed recursively |
| **Plan-and-Solve** ([Wang et al.](https://arxiv.org/abs/2305.04091)) | Decompose explicitly, then execute against the plan |

## Frameworks & Models

| Framework | Notes |
|---|---|
| LangGraph | Native subtask + dependency representation |
| AutoGen Group Chat | Decomposition emerges from agent dialogue |
| DSPy `ChainOfThought` w/ structured output | Lightweight programmatic version |

## Model Comparison

| Capability | claude-opus-4-5 | gpt-4o | claude-sonnet-4-5 |
|---|---|---|---|
| Atomic, well-scoped subtasks | 5 | 4 | 4 |
| Schema adherence | 5 | 5 | 4 |
| Avoids over-decomposition | 5 | 4 | 4 |
| Cost | 2 | 3 | 4 |

## Related Skills

- [Planning](planning.md) — adds order + deps + constraints to a decomposition
- [Reflection](../09-agentic-patterns/reflection.md) — revise a bad decomposition
- [Tree of Thought](../09-agentic-patterns/tot.md) — branch over alternative decompositions

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial stub |
| 2026-04 | v3 | Battle-tested: typed `Subtask` + `Decomposition`, validation, failure modes, model comparison |
