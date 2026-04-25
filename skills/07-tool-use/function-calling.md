---
title: "Function / Tool Calling"
category: 07-tool-use
level: basic
stability: stable
description: "Let the model emit a structured request to call one of your functions, with type-checked arguments — the foundation of every tool-using agent."
added: "2025-03"
version: v3
tags: [tool-use, function-calling, structured-output, agent]
updated: "2026-04"
dependencies:
  - package: openai
    min_version: "1.40.0"
    tested_version: "1.50.0"
    confidence: verified
code_blocks:
  - id: "example-fc"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-function-calling.json)

# Function / Tool Calling

## Description

The model is told *what your functions do* via a JSON-Schema spec. When the user's request matches a function, the model emits `{name, arguments}` instead of free text. Your code parses the arguments, runs the function, and feeds the result back so the model can keep going.

This is the primitive that turns an LLM into an *agent*. Every higher-level pattern — [ReAct](../09-agentic-patterns/react.md), tool-use loops, multi-step plans — is built on it.

## When to Use

- Anywhere the model must *act on the world* — query a DB, hit an API, run a calculation.
- When you need **typed arguments** the model can't fudge.
- When you want a clean audit trail (every action is a parsed call).
- **Don't use** when the answer is purely text generation — you'll spend tokens on a schema for nothing.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `tools` | `list[ToolSpec]` | Each: name, description, JSON schema for args |
| `messages` | `list[dict]` | Chat history |
| `tool_choice` | `Literal["auto","required","none"] \| ToolName` | Force/disable tool use |
| → `tool_calls` | `list[Call]` | Each: `name`, `arguments: dict`, `id` |
| → `tool_results` | `list[dict]` | Your function output, sent back next round |

## Runnable Example

```python
# pip install "openai>=1.40"
# export OPENAI_API_KEY=...
from __future__ import annotations
import json
from typing import Callable
from openai import OpenAI

client = OpenAI()
MODEL = "gpt-4o"

# 1. Implement the actual functions ------------------------------------------
def get_weather(city: str, units: str = "celsius") -> str:
    return f"{city}: 24°{units[0].upper()}, clear."

def add_to_calendar(title: str, iso_time: str, duration_minutes: int = 30) -> str:
    return f"Booked '{title}' at {iso_time} for {duration_minutes}m."

REGISTRY: dict[str, Callable[..., str]] = {
    "get_weather": get_weather,
    "add_to_calendar": add_to_calendar,
}

# 2. Describe them so the model knows when to call them ----------------------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Look up the current weather in a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city":  {"type": "string"},
                    "units": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["city"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_to_calendar",
            "description": "Book an event on the user's calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title":           {"type": "string"},
                    "iso_time":        {"type": "string", "description": "ISO 8601"},
                    "duration_minutes":{"type": "integer", "minimum": 5},
                },
                "required": ["title", "iso_time"],
                "additionalProperties": False,
            },
        },
    },
]

# 3. Run a loop until the model stops emitting tool_calls --------------------
def run(prompt: str, max_steps: int = 6) -> str:
    messages: list[dict] = [{"role": "user", "content": prompt}]
    for _ in range(max_steps):
        r = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS, tool_choice="auto",
        )
        msg = r.choices[0].message
        if not msg.tool_calls:
            return msg.content or ""
        messages.append(msg.model_dump())  # the assistant turn carrying tool_calls
        for c in msg.tool_calls:
            args = json.loads(c.function.arguments)
            try:
                output = REGISTRY[c.function.name](**args)
            except Exception as e:
                output = f"ERROR: {type(e).__name__}: {e}"
            messages.append({
                "role": "tool",
                "tool_call_id": c.id,
                "content": output,
            })
    return "(tool budget exhausted)"

if __name__ == "__main__":
    print(run("What's the weather in Cairo, and book me a 15-min review tomorrow at 10am UTC?"))
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Model invents an unknown function name | Underspecified system prompt; missing tool | Validate `c.function.name in REGISTRY`, surface a `tool_result` error so the model can recover |
| Bad argument types (`"5"` instead of `5`) | Loose `parameters` schema | Use `additionalProperties: false`, strict types, providers' `strict: true` mode where supported |
| `arguments` is invalid JSON | Model truncated mid-emit | Increase `max_tokens`; on `JSONDecodeError`, re-ask with the same context |
| Infinite tool loop | No `max_steps` cap | Hard cap; on exhaustion return partial result + reason |
| Side-effects on retries | Idempotency missing in your function | Generate a per-call idempotency key from `c.id` |
| Sensitive data leaked into args | No redaction layer | Filter `args` before logging; never log raw chat content |

## Frameworks & Models

| Provider / Framework | Notes |
|---|---|
| OpenAI `tools` (above) | Strict mode + parallel tool calls supported |
| Anthropic `tools` | See [Anthropic API skill](anthropic-api.md) |
| OpenAI Assistants | Persistent threads; tools live on the assistant |
| LangGraph `ToolNode` | Graph-native dispatch |
| Pydantic AI | Functions defined as typed Python; schema auto-generated |

## Model Comparison

| Capability | gpt-4o | claude-opus-4-5 | gpt-4o-mini |
|---|---|---|---|
| Strict-schema arg fidelity | 5 | 5 | 4 |
| Multi-tool / parallel calls | 5 | 4 | 4 |
| Cost-efficiency | 3 | 2 | 5 |
| Tool-name hallucination rate (lower better) | 5 | 5 | 4 |

## Related Skills

- [OpenAI API](openai-api.md), [Anthropic API](anthropic-api.md) — full provider wrappers
- [ReAct](../09-agentic-patterns/react.md) — function calling inside a reasoning loop
- [Structured Output](../06-communication/structured-output.md) — same primitive without execution

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial stub |
| 2026-04 | v3 | Battle-tested: registry pattern, strict schema, error-as-tool-result, model comparison |
