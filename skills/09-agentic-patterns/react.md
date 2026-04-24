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

# --- 1. Real tools ----------------------------------------------------------

def web_search(query: str) -> str:
    # Plug in Tavily / Brave / Exa here. Demo returns a fixed snippet.
    if "cairo" in query.lower():
        return "Cairo metropolitan population (2024 UN est.): ~22.6 million."
    return "No high-confidence result found."

def calc(expression: str) -> str:
    # Eval-free arithmetic to keep the demo safe.
    import ast, operator as op
    ops = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv}
    def ev(node):
        if isinstance(node, ast.Constant): return node.value
        if isinstance(node, ast.BinOp):    return ops[type(node.op)](ev(node.left), ev(node.right))
        raise ValueError("unsupported expression")
    return str(ev(ast.parse(expression, mode="eval").body))

TOOLS: dict[str, Callable[[str], str]] = {"web_search": web_search, "calc": calc}

TOOL_SCHEMA = [
    {
        "name": "web_search",
        "description": "Search the web. Argument: a natural-language query string.",
        "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
    },
    {
        "name": "calc",
        "description": "Evaluate a basic arithmetic expression like '2 + 3 * 4'.",
        "input_schema": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]},
    },
]

# --- 2. ReAct loop ----------------------------------------------------------

SYSTEM = """You are a ReAct agent. For each turn either:
  1. Call exactly one tool to gather more information, OR
  2. Reply in plain text starting with 'Final Answer:' once you can answer.
Keep reasoning short and concrete. Never invent observations."""

def react(goal: str, max_steps: int = 8) -> dict:
    messages = [{"role": "user", "content": goal}]
    trace: list[dict] = []
    for step in range(max_steps):
        resp = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=512,
            system=SYSTEM,
            tools=TOOL_SCHEMA,
            messages=messages,
        )
        if resp.stop_reason == "tool_use":
            tool_block = next(b for b in resp.content if b.type == "tool_use")
            args = tool_block.input
            obs = TOOLS[tool_block.name](**args)
            trace.append({"thought": _text(resp), "action": tool_block.name, "args": args, "observation": obs})
            messages.append({"role": "assistant", "content": resp.content})
            messages.append({"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": tool_block.id, "content": obs}
            ]})
            continue
        # End_turn: model produced a final answer.
        answer = _text(resp)
        return {"answer": answer.removeprefix("Final Answer:").strip(), "trace": trace}
    return {"answer": "step budget exhausted", "trace": trace}

def _text(resp) -> str:
    return "".join(b.text for b in resp.content if b.type == "text")

if __name__ == "__main__":
    out = react("What is Cairo's population in millions, multiplied by 3?")
    print(out["answer"])
    print(json.dumps(out["trace"], indent=2))
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Tool-call ping-pong | Model re-asks the same tool with the same args | Detect duplicate (name, args) within trace; force "Final Answer or quit" prompt |
| Hallucinated observations | Model writes Observation in its own reasoning | Use a real tool-call API (function calling), not free-form text parsing |
| Infinite loop on impossible task | No success criterion + no step cap | Always set `max_steps`; have the agent self-summarize on cap |
| Wrong tool selected | Tool descriptions ambiguous | Make descriptions imperative + include "use when …" / "do NOT use when …" |
| Cost blow-up | Long traces fed back every turn | Truncate or summarize old observations; cache static tool results |

## Variants

| Variant | Difference |
|---|---|
| **Plan-and-Execute** | First produce a full plan, then execute steps without re-planning |
| **Tool-Use Loop** | Same as ReAct but tools may run in parallel each step |
| **LATS** | ReAct + tree search + value function — better on multi-hop search |
| **Reflection** | After failure, an evaluator critiques the trace and the next attempt re-plans |

## Frameworks & Models

| Framework | Implementation |
|---|---|
| LangGraph | `create_react_agent(llm, tools)` |
| LangChain (legacy) | `AgentExecutor(agent=ReActAgent(...), tools=...)` |
| OpenAI Assistants v2 | Function calling + thread loop |
| Anthropic Tool Use | Native `tool_use` / `tool_result` blocks (shown above) |
| Pydantic AI | `Agent(tools=[...])` with typed deps |

## Model Comparison

| Capability | claude-opus-4-5 | gpt-4o | gemini-2.0-flash |
|---|---|---|---|
| Stops looping when goal met | 5 | 4 | 3 |
| Recovers from a bad observation | 4 | 4 | 3 |
| Tool argument validity | 4 | 5 | 3 |
| Cost per task | 3 | 4 | 5 |

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
| 2026-04 | v3 | Full runnable Anthropic tool-use example, failure modes, model comparison |
