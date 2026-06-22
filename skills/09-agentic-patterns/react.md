---
title: "ReAct (Reasoning + Acting)"
category: 09-agentic-patterns
level: intermediate
stability: stable
description: "Interleave Thought → Action → Observation steps in a tool-calling loop until the agent declares Final Answer. The most-used reasoning-with-tools pattern."
added: "2025-03"
version: v3
tags: [react, agent, tool-use, reasoning]
updated: "2026-04"
dependencies:
  - package: anthropic
    min_version: "0.39.0"
    tested_version: "0.39.0"
    confidence: verified
code_blocks:
  - id: "example-react-loop"
    type: executable
prerequisites:
  - 09-agentic-patterns/cot
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-react.json)

# ReAct (Reasoning + Acting)

## Description

ReAct interleaves **Thought** (model reasoning), **Action** (a tool call), and **Observation** (the tool's return value) inside a single loop. The model picks the next tool based on what it has learned so far and stops when it can answer. It is the simplest working architecture for tool-using agents and the foundation that more elaborate patterns (Plan-and-Execute, LATS, Tool-Use Loop) build on.

## When to Use

- The task needs **external information or actions** (search, DB query, API call) — pure CoT is not enough.
- You want a single tool-using loop that's easy to debug and inexpensive.
- You can tolerate **5–15 model calls** per task; for sub-second latency, prefer direct tool calls without the loop.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `goal` | `str` | The user's task |
| `tools` | `dict[str, Callable]` | Name → callable returning a string observation |
| `max_steps` | `int` | Hard cap, default 10 |
| → `answer` | `str` | Final Answer string |
| → `trace` | `list[dict]` | Per-step `{thought, action, args, observation}` |

## Runnable Example

```python
# pip install anthropic
from __future__ import annotations
import json
from typing import Callable
import anthropic

client = anthropic.Anthropic()

def web_search(query: str) -> str:
    if "cairo" in query.lower():
        return "Cairo metropolitan population (2024 UN est.): ~22.6 million."
    return "No high-confidence result found."

def calc(expression: str) -> str:
    import ast, operator as op
    ops = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv}
    def ev(node):
        if isinstance(node, ast.Constant): return node.value
        if isinstance(node, ast.BinOp):    return ops[type(node.op)](ev(node.left), ev(node.right))
        raise ValueError("unsupported expression")
    return str(ev(ast.parse(expression, mode="eval").body))

TOOLS: dict[str, Callable[[str], str]] = {"web_search": web_search, "calc": calc}

TOOL_SCHEMA = [
    {"name": "web_search", "description": "Search the web.", "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    {"name": "calc", "description": "Evaluate arithmetic.", "input_schema": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}},
]

SYSTEM = """You are a ReAct agent. For each turn either:
  1. Call exactly one tool to gather more information, OR
  2. Reply in plain text starting with 'Final Answer:' once you can answer."""

def react(goal: str, max_steps: int = 8) -> dict:
    messages = [{"role": "user", "content": goal}]
    trace: list[dict] = []
    for step in range(max_steps):
        resp = client.messages.create(model="claude-opus-4-5", max_tokens=512, system=SYSTEM, tools=TOOL_SCHEMA, messages=messages)
        if resp.stop_reason == "tool_use":
            tool_block = next(b for b in resp.content if b.type == "tool_use")
            obs = TOOLS[tool_block.name](**tool_block.input)
            trace.append({"action": tool_block.name, "args": tool_block.input, "observation": obs})
            messages.append({"role": "assistant", "content": resp.content})
            messages.append({"role": "user", "content": [{"type": "tool_result", "tool_use_id": tool_block.id, "content": obs}]})
            continue
        answer = "".join(b.text for b in resp.content if b.type == "text")
        return {"answer": answer.removeprefix("Final Answer:").strip(), "trace": trace}
    return {"answer": "step budget exhausted", "trace": trace}

if __name__ == "__main__":
    out = react("What is Cairo's population in millions, multiplied by 3?")
    print(out["answer"])
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Tool-call ping-pong | Model re-asks the same tool | Detect duplicate (name, args) in trace |
| Hallucinated observations | Model writes Observation itself | Use real tool-call API |
| Infinite loop | No step cap | Always set `max_steps` |
| Cost blow-up | Long traces fed back every turn | Truncate old observations |

## Variants

| Variant | Difference |
|---|---|
| **Plan-and-Execute** | Full plan first, then execute |
| **Tool-Use Loop** | Tools may run in parallel |
| **LATS** | ReAct + tree search + value function |
| **Reflection** | Evaluator critiques trace after failure |

## Related Skills

- [Chain of Thought](cot.md) — pure reasoning, no tools
- [Tool-Use Loop](tool-use-loop.md) — parallel-tool variant
- [Reflection](reflection.md) — critic + retry on failure
- [Planning](../02-reasoning/planning.md) — structured plan first, then execute

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial entry |
| 2026-02 | v2 | Added variants table |
| 2026-04 | v3 | Full runnable Anthropic tool-use example |
| 2026-06 | v3.1 | Added prerequisites field (INITIATIVE-005) |
