---
title: ReAct (Reasoning + Acting)
category: 02-reasoning
level: intermediate
stability: stable
added: "2025-03"
description: "Apply react in AI agent workflows."
version: v3
tags: [reasoning, planning, tool-use, agentic]
updated: 2026-04
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-react.json)

# ReAct — Reasoning + Acting

## What It Does

ReAct interleaves *reasoning traces* (Thought) with *grounded actions* (Act) and their *observations* (Obs) in a single loop. The model thinks step-by-step, calls a tool, reads the result, then thinks again — until the task is done.

It eliminates the gap between "thinking" and "doing" that plagues pure chain-of-thought approaches.

## When to Use

- Multi-step tasks that need external information (search, DB, APIs)
- Tasks where intermediate results change the next step
- Any agentic loop requiring tool calls + reasoning together

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `task` | `str` | The user's goal |
| `tools` | `list[Tool]` | Available tools (search, calculator, code, etc.) |
| `max_steps` | `int` | Termination limit (default: 10) |
| → `answer` | `str` | Final grounded answer |
| → `trace` | `list[dict]` | Full thought/action/observation history |

## Runnable Example

```python
import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "web_search",
        "description": "Search the web for current information",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    }
]

def react_loop(task: str, max_steps: int = 10):
    messages = [{"role": "user", "content": task}]
    trace = []

    system = """You are a ReAct agent. For every step:
1. Think: reason about what to do next
2. Act: call a tool if needed
3. Observe: read the result
4. Repeat until you can give a final answer.

When done, respond with: Final Answer: <answer>"""

    for step in range(max_steps):
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            system=system,
            tools=tools,
            messages=messages
        )

        # Check for final answer
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text") and "Final Answer:" in block.text:
                    answer = block.text.split("Final Answer:")[-1].strip()
                    return {"answer": answer, "trace": trace, "steps": step + 1}

        # Handle tool call
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    trace.append({"action": block.name, "input": block.input})
                    # Simulate tool execution
                    result = f"[Result for {block.name}({block.input})]"
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            messages.append({"role": "user", "content": tool_results})

    return {"answer": "Max steps reached", "trace": trace}

result = react_loop("What is the current population of Egypt and how has it changed since 2020?")
print(result["answer"])
```

## Framework Support

| Framework | Implementation | Notes |
|---|---|---|
| LangChain | `create_react_agent()` | Built-in, stable |
| LangGraph | Custom graph nodes | More control, recommended for production |
| CrewAI | Agent default loop | ReAct under the hood |
| AutoGen | `AssistantAgent` | Configurable |
| Raw API | See example above | Full control |

## Failure Modes

| Failure | Cause | Fix |
|---|---|---|
| Infinite loops | No termination condition | Set `max_steps`, check for "Final Answer" |
| Hallucinated tool results | Model fabricates observations | Always inject real tool results |
| Reasoning drift | Long traces confuse the model | Summarize trace every N steps |
| Over-thinking | Model calls tools unnecessarily | Add "only call tools when needed" to system prompt |

## Benchmarks

See → [`benchmarks/reasoning/react-vs-lats.md`](../../benchmarks/reasoning/react-vs-lats.md)

**Summary:** ReAct scores 68.4% on HotpotQA (multi-hop QA). LATS beats it by 8.3% but costs 4x more tokens. ReAct is the right default for most production use cases.

## Related Skills

- [`chain-of-thought.md`](chain-of-thought.md) — Reasoning without tool calls
- [`lats.md`](lats.md) — Tree search variant, higher accuracy
- [`tool-use.md`](../07-tool-use/tool-calling.md) — How tools are defined and called
- [`memory-injection.md`](../03-memory/memory-injection.md) — Add persistent context to the loop

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-03 | Initial entry, basic description |
| v2 | 2025-08 | Added framework table + failure modes |
| v3 | 2026-04 | Full runnable example, benchmark link, typed I/O |
