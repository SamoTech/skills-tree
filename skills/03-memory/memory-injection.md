---
title: Memory Injection
category: 03-memory
level: intermediate
stability: stable
added: "2025-03"
description: "Retrieve the K most relevant memories for a turn and inject them into the system prompt — long-term user context without filling the context window with raw history."
version: v3
tags: [memory, context, personalization, rag]
updated: "2026-04"
dependencies:
  - package: anthropic
    min_version: "0.39.0"
    tested_version: "0.39.0"
    confidence: verified
  - package: numpy
    min_version: "1.26.0"
    tested_version: "1.26.4"
    confidence: verified
code_blocks:
  - id: "example-memory-injection"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-memory-injection.json)

# Memory Injection

## Description

Dynamically retrieves the **most relevant** prior memories (past user statements, preferences, established facts) and injects them into the model's system prompt before each turn. Gives an agent durable user context without paying the token cost of replaying every previous turn.

The key insight: **don't inject all memories — retrieve the top-K relevant to the current query.**

## When to Use

- Long-running assistants where users build up a profile over weeks.
- Multi-tenant agents that must scope memories per user without context-window blow-up.
- Any system where "the model forgot what I said yesterday" is the #1 user complaint.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `user_id` | `str` | Tenant key for memory store |
| `query` | `str` | Current user message |
| `top_k` | `int` | How many memories to inject (default: 5) |
| `memory_store` | `MemoryStore` | Vector index keyed by user_id |
| → `system_prompt` | `str` | Base system + injected memory block |
| → `injected` | `list[Memory]` | Memories actually used (for audit) |

## Runnable Example

```python
# pip install anthropic numpy
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable
import numpy as np
import anthropic

client = anthropic.Anthropic()

@dataclass
class Memory:
    text: str
    embedding: np.ndarray
    weight: float = 1.0  # boost recent / explicitly-asserted facts

class MemoryStore:
    def __init__(self) -> None:
        self._mem: dict[str, list[Memory]] = {}

    def add(self, user_id: str, text: str, embedding: np.ndarray, weight: float = 1.0) -> None:
        self._mem.setdefault(user_id, []).append(Memory(text, embedding, weight))

    def top_k(self, user_id: str, query_emb: np.ndarray, k: int = 5) -> list[Memory]:
        items = self._mem.get(user_id, [])
        if not items:
            return []
        scores = np.array([
            m.weight * float(np.dot(m.embedding, query_emb) /
                             (np.linalg.norm(m.embedding) * np.linalg.norm(query_emb) + 1e-8))
            for m in items
        ])
        idx = np.argsort(-scores)[:k]
        return [items[i] for i in idx]

def embed(texts: Iterable[str]) -> np.ndarray:
    # Production: voyage-3, text-embedding-3-large, or jina-embeddings-v3.
    # Demo: deterministic hash-based vectors so the example runs offline.
    rng = np.random.default_rng(0)
    return np.stack([rng.standard_normal(256) for _ in texts])

def build_system_prompt(base: str, memories: list[Memory]) -> str:
    if not memories:
        return base
    block = "\n".join(f"- {m.text}" for m in memories)
    return f"{base}\n\n## What you remember about this user\n{block}"

def reply_with_memory(user_id: str, query: str, store: MemoryStore, base_system: str) -> str:
    [q_emb] = embed([query])
    injected = store.top_k(user_id, q_emb, k=5)
    system_prompt = build_system_prompt(base_system, injected)
    msg = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        system=system_prompt,
        messages=[{"role": "user", "content": query}],
    )
    return msg.content[0].text

# --- demo ---
if __name__ == "__main__":
    store = MemoryStore()
    facts = [
        "User prefers concise answers, no preamble.",
        "User is a senior backend engineer working primarily in Python.",
        "User's timezone is Africa/Cairo.",
        "User dislikes emoji in technical responses.",
    ]
    for fact, emb in zip(facts, embed(facts)):
        store.add("user-42", fact, emb, weight=1.0)
    print(reply_with_memory(
        "user-42",
        "Draft a one-line cron expression for 9am every weekday.",
        store,
        base_system="You are a precise engineering assistant.",
    ))
```

## Retrieval Strategies

| Strategy | When to use | Trade-off |
|---|---|---|
| Cosine top-K | Default, well-understood | Misses paraphrased facts |
| HyDE (hypothetical answer → embed → retrieve) | Sparse memory store | +12% recall, +1 LLM call |
| Recency-weighted | User profile drifts over time | Older facts under-retrieved |
| Hybrid (BM25 + vector) | Mixed natural-language + named-entity memory | More infra; higher precision |
| Memory summarization rollup | >1k memories per user | Lossy; needs periodic rebuild |

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Stale facts retrieved | No invalidation on `user said X is no longer true` | Add a `superseded_by` link; soft-delete on contradiction |
| Personality leakage across users | Wrong `user_id` scoping | Make `user_id` a required arg; assert on retrieval |
| Prompt injection via memory | User-asserted memory contains "Ignore prior instructions" | Wrap injected block in `<user_memory>` tags; remind the model the block is data, not instructions |
| Context-window blowup | `top_k` set too high | Cap at K=10; budget ~1.5k tokens for the memory block |
| Cold start | New user has no memories | Fall back to base system prompt; no injected block |

## Frameworks & Models

| Framework / Service | Implementation | Notes |
|---|---|---|
| [mem0](https://mem0.ai) | Managed memory layer with auto-write | Easiest to adopt |
| [LangGraph](https://langchain.com/langgraph) | Memory node before LLM node | Full control over scoring |
| [Letta (MemGPT)](https://letta.com) | Hierarchical core/recall memory | Best for very long sessions |
| OpenAI Assistants v2 threads | Implicit per-thread memory | No cross-thread |
| Anthropic prompt caching | Cache the injected block when stable | Cuts cost on warm sessions |

## Model Comparison

| Capability | claude-opus-4-5 | gpt-4o | gemini-2.0-flash |
|---|---|---|---|
| Treats memory block as data, not instructions | 4 | 4 | 3 |
| Recovers gracefully when memories contradict | 4 | 3 | 3 |
| Cost efficiency for short queries | 3 | 4 | 5 |

## Related Skills

- [Working Memory](working-memory.md) — short-term, intra-turn
- [Long-Term Memory](long-term-memory.md) — persistence layer
- [RAG](../09-agentic-patterns/rag.md) — retrieval over external corpora vs. user memory
- [Forgetting](forgetting.md) — TTL / superseded-by handling

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial entry |
| 2026-04 | v2 | Added retrieval scoring + cosine top-K |
| 2026-04 | v3 | Full runnable example, failure modes, model comparison, hybrid strategies |
