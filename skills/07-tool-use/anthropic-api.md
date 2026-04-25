---
title: "Anthropic API"
category: 07-tool-use
level: intermediate
stability: stable
description: "Call Anthropic's Claude Messages API for chat, vision, tool use, and prompt-cached long context — with retry, streaming, and a typed tool dispatcher."
added: "2025-03"
version: v3
tags: [anthropic, claude, api, tool-use]
updated: "2026-04"
dependencies:
  - package: anthropic
    min_version: "0.39.0"
    tested_version: "0.39.0"
    confidence: verified
code_blocks:
  - id: "example-anthropic"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-anthropic-api.json)

# Anthropic API

## Description

Wraps the Anthropic Messages API for the four jobs an agent does most:

1. **Chat / completion** with system prompts and message history.
2. **Tool use** — the model returns `tool_use` blocks; you execute and return `tool_result`.
3. **Streaming** for token-by-token UX.
4. **Prompt caching** to amortize the cost of large stable system prompts (docs, code, glossaries).

## When to Use

- You want **strong multi-step tool use** with lower hallucinated-arg rates.
- You're feeding **long stable context** (full repo, manuals) and want prompt caching to drop cost ~85%.
- You need vision (Claude handles charts and diagrams strongly).

## Inputs / Outputs

| Helper | Input | Output |
|---|---|---|
| `chat()` | `messages`, `system`, `model` | assistant text |
| `tool_loop()` | tools registry + prompt | final text after tool round-trips |
| `stream_chat()` | `messages` | iterable of token chunks |
| `cached_chat()` | large system + messages | text, with cache reuse on repeat calls |

## Runnable Example

```python
# pip install "anthropic>=0.39"
# export ANTHROPIC_API_KEY=...
from __future__ import annotations
import json
import time, random
from typing import Callable, Iterable
import anthropic
from anthropic import APIConnectionError, APIStatusError, RateLimitError

client = anthropic.Anthropic()
MODEL = "claude-opus-4-5"

# 1. Chat with retry ----------------------------------------------------------
def chat(messages: list[dict], *, system: str = "", model: str = MODEL,
         max_attempts: int = 4) -> str:
    for attempt in range(max_attempts):
        try:
            r = client.messages.create(
                model=model, max_tokens=1024, system=system, messages=messages,
            )
            return r.content[0].text
        except (RateLimitError, APIConnectionError):
            if attempt == max_attempts - 1: raise
            time.sleep(min(2 ** attempt, 10) + random.random())
        except APIStatusError as e:
            if 500 <= e.status_code < 600 and attempt < max_attempts - 1:
                time.sleep(min(2 ** attempt, 10)); continue
            raise

# 2. Tool loop ----------------------------------------------------------------
def get_weather(city: str) -> str:
    return f"{city}: 24°C, clear."

REGISTRY: dict[str, Callable[..., str]] = {"get_weather": get_weather}

TOOLS = [{
    "name": "get_weather",
    "description": "Look up the current weather for a city.",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
    },
}]

def tool_loop(prompt: str, max_steps: int = 6) -> str:
    messages: list[dict] = [{"role": "user", "content": prompt}]
    for _ in range(max_steps):
        r = client.messages.create(
            model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages,
        )
        if r.stop_reason != "tool_use":
            return "".join(b.text for b in r.content if b.type == "text")
        messages.append({"role": "assistant", "content": r.content})
        results = []
        for block in r.content:
            if block.type == "tool_use":
                out = REGISTRY[block.name](**block.input)
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": out})
        messages.append({"role": "user", "content": results})
    return "tool loop budget exhausted"

# 3. Streaming ----------------------------------------------------------------
def stream_chat(messages: list[dict], system: str = "") -> Iterable[str]:
    with client.messages.stream(
        model=MODEL, max_tokens=1024, system=system, messages=messages,
    ) as s:
        for text in s.text_stream:
            yield text

# 4. Prompt caching -----------------------------------------------------------
def cached_chat(big_system_doc: str, user_msg: str) -> str:
    """Mark a large stable system block as cacheable. Subsequent calls
    that re-use the same block pay ~10% of its tokens."""
    r = client.messages.create(
        model=MODEL,
        max_tokens=512,
        system=[
            {"type": "text", "text": "You answer questions about the attached doc."},
            {"type": "text", "text": big_system_doc, "cache_control": {"type": "ephemeral"}},
        ],
        messages=[{"role": "user", "content": user_msg}],
    )
    return r.content[0].text

if __name__ == "__main__":
    print(chat([{"role": "user", "content": "One sentence on Skills Tree."}]))
    print(tool_loop("What is the weather in Cairo?"))
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Tool loop deadlock | Model keeps emitting `tool_use` forever | Hard `max_steps` cap (above) |
| `tool_result` mismatch | Forgot to attach the parent `assistant` message | Always append the entire `r.content` block before tool results |
| Cache cold-start cost | First call still pays full system tokens | Warm the cache once at deploy time |
| Streaming + retry duplicates tokens | Naive retry on the same stream | Cancel the stream before retry; resume from the last yielded chunk |
| 529 overloaded errors | Spike traffic | Exponential backoff + lower max_tokens; consider Bedrock fallback |
| Wrong content extraction | Model returned mixed text + tool_use | Filter `b.type == "text"` blocks before joining |

## Frameworks & Models

| Framework | Use case |
|---|---|
| `anthropic` SDK (above) | Direct, lowest abstraction |
| `anthropic` via Amazon Bedrock | Same model, different control plane / quotas |
| LangChain `ChatAnthropic` | Drop-in for LangChain pipelines |
| LiteLLM | Multi-provider abstraction with Anthropic support |

## Model Comparison

| Capability | claude-opus-4-5 | claude-sonnet-4-5 | claude-haiku-4-5 |
|---|---|---|---|
| Tool-use reliability | 5 | 5 | 4 |
| Long-context retrieval | 5 | 5 | 4 |
| Latency | 3 | 4 | 5 |
| Cost | 2 | 4 | 5 |

## Related Skills

- [OpenAI API](openai-api.md) — peer LLM provider
- [Function Calling](function-calling.md) — pattern this builds on
- [ReAct](../09-agentic-patterns/react.md) — uses tool-loop above
- [Image Understanding](../01-perception/image-understanding.md) — vision input

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial entry |
| 2026-04 | v3 | Tool loop, streaming, prompt caching, retry, model comparison |
