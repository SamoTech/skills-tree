---
title: "Short-Term Memory"
category: 03-memory
level: intermediate
stability: stable
added: "2025-03"
description: "The bounded conversational scratchpad — recent turns + tool outputs the model can see this turn. Trims under a token budget so the agent never crashes on context overflow."
version: v3
tags: [memory, context, token-budget]
updated: "2026-04"
dependencies:
  - package: tiktoken
    min_version: "0.7.0"
    confidence: verified
code_blocks:
  - id: "example-stm"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-short-term-memory.json)

# Short-Term Memory

## Description

Short-term memory (STM) is the **rolling context window** the agent shows the model on every turn: the last *N* user/assistant messages, plus any tool outputs and a small set of pinned system facts. It's the simplest, most-deployed memory pattern — and the one that breaks first when it isn't bounded by a real token budget.

A correct STM does three things every turn: (1) compute current token count, (2) drop oldest non-pinned messages until under budget, (3) optionally summarise the dropped chunk so the model still has a thread of the past. This skill is what the rest of [Long-Term Memory](long-term-memory.md), [Episodic Memory](episodic-memory.md), and [Memory Injection](memory-injection.md) build on top of.

## When to Use

- **Always** in any chat or agent loop — even one-turn agents need a bounded STM for tool outputs.
- When sessions are long enough that the raw history will exceed your model's context (~128k for current frontier).
- Pair with [Memory Injection](memory-injection.md) when you also want long-term, cross-session recall.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `history` | `list[Message]` | All messages in the session |
| `pinned` | `list[Message]` | Always-included messages (system, key facts) |
| `budget_tokens` | `int` | Max tokens for the rendered window |
| `model` | `str` | For tokenizer selection |
| → `window` | `list[Message]` | The trimmed list passed to the LLM |
| → `dropped` | `list[Message]` | What was removed (for optional summarisation) |

## Runnable Example

```python
# pip install tiktoken
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal
import tiktoken

@dataclass
class Message:
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    pinned: bool = False

def _encoder(model: str):
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        return tiktoken.get_encoding("cl100k_base")

def count_tokens(messages: list[Message], model: str) -> int:
    enc = _encoder(model)
    # Approx: 4 tokens of overhead per message + role token + content
    return sum(4 + len(enc.encode(m.role)) + len(enc.encode(m.content)) for m in messages)

def trim_window(
    history: list[Message],
    pinned: list[Message],
    budget_tokens: int,
    model: str = "gpt-4o",
) -> tuple[list[Message], list[Message]]:
    """Return (window, dropped). pinned messages always kept."""
    # Reserve budget for pinned messages
    pin_tokens = count_tokens(pinned, model)
    if pin_tokens > budget_tokens:
        raise ValueError(f"pinned messages ({pin_tokens}) exceed budget ({budget_tokens})")
    remaining = budget_tokens - pin_tokens

    # Walk history newest-first, keep until budget exhausted
    keep_rev: list[Message] = []
    used = 0
    for m in reversed(history):
        cost = count_tokens([m], model)
        if used + cost > remaining:
            break
        keep_rev.append(m)
        used += cost
    keep = list(reversed(keep_rev))
    dropped = [m for m in history if m not in keep]
    return pinned + keep, dropped

if __name__ == "__main__":
    history = [Message("user", f"turn {i}: " + "lorem " * 200) for i in range(50)]
    pinned = [Message("system", "You are a concise assistant.", pinned=True)]
    win, dropped = trim_window(history, pinned, budget_tokens=4_000, model="gpt-4o")
    print(f"window={len(win)} msgs ({count_tokens(win,'gpt-4o')} tok), dropped={len(dropped)}")
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Context overflow at runtime | Naive append-only history | Always `trim_window` before sending; reject any single message larger than the budget |
| Lost critical facts | Important info was at turn 1, dropped | Pin those facts; or summarise dropped chunk and re-inject |
| Tokenizer mismatch | Counted with wrong tokenizer | Use the model's actual tokenizer (or its closest fallback) |
| Identity drift mid-session | System prompt dropped | Pin the system prompt; never let it be trimmed |
| Tool spam blowing budget | Verbose tool outputs over many turns | Cap tool outputs (truncate to N tokens) before storage |
| Off-by-one with assistant turns | Trimmed an `assistant`/`tool` pair separately | Trim by message *pairs* if your provider requires interleaving |

## Variants

| Variant | Description |
|---|---|
| **Sliding window** | Drop oldest until under budget (above) |
| **Summarised window** | Replace dropped span with a 1-paragraph summary |
| **Hierarchical** | Recent turns verbatim + older turns as compressed summaries |
| **Token-budget per role** | Reserve N tokens for system, M for tool outputs, etc. |

## Frameworks & Models

| Framework | Notes |
|---|---|
| LangChain `ConversationTokenBufferMemory` | Sliding-window, token-aware |
| LangChain `ConversationSummaryBufferMemory` | Summarised variant |
| LlamaIndex `ChatMemoryBuffer` | Same primitive, different ergonomics |
| Anthropic prompt caching | Lets you keep a *long* STM cheap on repeat |

## Related Skills

- [Memory Injection](memory-injection.md) — pulls long-term memories *into* the STM each turn
- [Long-Term Memory](long-term-memory.md) — what dropped messages get archived to
- [Episodic Memory](episodic-memory.md) — session-scoped event store

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial stub |
| 2026-04 | v3 | Battle-tested: token-budgeted trim, tokenizer fallback, pinned messages, failure modes |
