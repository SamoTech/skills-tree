---
title: "OpenAI API"
category: 07-tool-use
level: intermediate
stability: stable
description: "Call OpenAI Chat, Embeddings, Images, and Audio endpoints from Python — with structured outputs, function calling, retry, and streaming."
added: "2025-03"
version: v3
tags: [openai, api, llm, function-calling]
updated: "2026-04"
dependencies:
  - package: openai
    min_version: "1.50.0"
    tested_version: "2.31.0"
    confidence: verified
  - package: pydantic
    min_version: "2.0.0"
    tested_version: "2.13.0"
    confidence: verified
code_blocks:
  - id: "example-openai"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-openai-api.json)

# OpenAI API

## Description

Wraps the four OpenAI surfaces an agent typically needs:

1. **Chat Completions** — text generation.
2. **Structured Outputs** — typed JSON via Pydantic.
3. **Function Calling / Tools** — let the model invoke your code.
4. **Embeddings & multimodal** — vectors, vision, audio.

The example below covers all four with retries, streaming, and a single client. Pair with [`anthropic-api.md`](anthropic-api.md) when you need provider-fallback.

## When to Use

- Default for production agents on commodity tasks (Q&A, classification, summarization).
- When you specifically need OpenAI's structured-outputs guarantee (JSON schema enforced server-side).
- When the platform's vector store / file search / Realtime API are hard requirements.

## Inputs / Outputs

| Helper | Input | Output |
|---|---|---|
| `chat()` | `messages: list[dict]`, `model: str` | `str` (assistant text) |
| `parse_typed()` | Pydantic schema + prompt | Instance of that schema |
| `call_tools()` | tool registry + user prompt | Final text after the tool round-trip |
| `embed()` | `list[str]` | `list[list[float]]` |
| `stream_chat()` | `messages` | `Iterable[str]` token chunks |

## Runnable Example

```python
# pip install "openai>=1.50" "pydantic>=2"
# export OPENAI_API_KEY=...
from __future__ import annotations
import json
from typing import Callable, Iterable
from openai import OpenAI
from openai import APIConnectionError, APIStatusError, RateLimitError
from pydantic import BaseModel
import time, random

client = OpenAI()

# 1. Chat with bounded retry --------------------------------------------------
def chat(messages: list[dict], model: str = "gpt-4o", *,
         max_attempts: int = 4) -> str:
    for attempt in range(max_attempts):
        try:
            r = client.chat.completions.create(model=model, messages=messages)
            return r.choices[0].message.content or ""
        except (RateLimitError, APIConnectionError) as e:
            if attempt == max_attempts - 1:
                raise
            time.sleep(min(2 ** attempt, 10) + random.random())
        except APIStatusError as e:
            if 500 <= e.status_code < 600 and attempt < max_attempts - 1:
                time.sleep(min(2 ** attempt, 10))
                continue
            raise

# 2. Typed (structured) output ------------------------------------------------
class Sentiment(BaseModel):
    label: str  # "positive" | "neutral" | "negative"
    score: float
    reason: str

def parse_typed(text: str) -> Sentiment:
    r = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Classify sentiment."},
            {"role": "user", "content": text},
        ],
        response_format=Sentiment,
    )
    return r.choices[0].message.parsed

# 3. Function calling ---------------------------------------------------------
def add(a: int, b: int) -> int: return a + b

TOOLS = [{
    "type": "function",
    "function": {
        "name": "add",
        "description": "Add two integers.",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
            "required": ["a", "b"],
        },
    },
}]

REGISTRY: dict[str, Callable] = {"add": add}

def call_tools(prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]
    for _ in range(4):
        r = client.chat.completions.create(model="gpt-4o", messages=messages, tools=TOOLS)
        m = r.choices[0].message
        if not m.tool_calls:
            return m.content or ""
        messages.append(m)
        for tc in m.tool_calls:
            args = json.loads(tc.function.arguments)
            result = REGISTRY[tc.function.name](**args)
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": str(result)})
    return "tool loop budget exhausted"

# 4. Embeddings + streaming ---------------------------------------------------
def embed(texts: list[str]) -> list[list[float]]:
    r = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [d.embedding for d in r.data]

def stream_chat(messages: list[dict], model: str = "gpt-4o") -> Iterable[str]:
    with client.chat.completions.stream(model=model, messages=messages) as s:
        for event in s:
            if event.type == "content.delta":
                yield event.delta

if __name__ == "__main__":
    print(chat([{"role": "user", "content": "One sentence on Skills Tree."}]))
    print(parse_typed("This library saved me hours."))
    print(call_tools("What is 41 + 1?"))
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| `RateLimitError` storms | No backoff | Exponential backoff with jitter (above) |
| `APIConnectionError` after long idle | Stale TLS connection | Retry on connection errors; do NOT retry on 4xx other than 429 |
| Tool loop never terminates | Model keeps calling tools | Hard cap iterations (`for _ in range(N)`) |
| Structured output rejected | Schema includes union types | Use plain Pydantic; prefer literals over `Union[A,B,C]` |
| Cost spike | Streaming + retry duplicates output | Drop the in-flight request before retrying |
| Token leakage in logs | Logging full requests | Redact the `Authorization` header and message content |

## Frameworks & Models

| Framework | Use case |
|---|---|
| `openai` SDK (above) | Direct, lowest abstraction |
| LangChain `ChatOpenAI` | Drop-in for LangChain pipelines |
| LiteLLM | Multi-provider abstraction with OpenAI-compatible API |
| OpenRouter | Single key for OpenAI + 100+ models |

## Model Comparison

| Capability | gpt-4o | gpt-4.1-mini | o3-mini |
|---|---|---|---|
| Function calling reliability | 5 | 4 | 4 |
| Structured outputs | 5 | 5 | 5 |
| Reasoning depth | 4 | 3 | 5 |
| Cost / latency | 4 | 5 | 3 |

## Related Skills

- [Anthropic API](anthropic-api.md) — peer LLM provider
- [Function Calling](function-calling.md) — pattern this builds on
- [Embedding Generation](../12-data/embedding-generation.md)

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial entry |
| 2026-04 | v3 | Retry, structured outputs, tool loop, streaming, embeddings |
