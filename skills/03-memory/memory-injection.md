---
title: Memory Injection
category: 03-memory
level: intermediate
stability: stable
description: "Apply memory injection in AI agent workflows."
version: v2
tags: [memory, context, personalization, rag]
updated: 2026-04
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-memory-injection.json)

# Memory Injection

## What It Does

Dynamically retrieves and injects relevant memories (past conversations, user facts, preferences) into the model's system prompt before each turn. Gives the agent long-term user context without filling the context window with raw history.

The key insight: **you don't inject all memories — you retrieve the most relevant ones for the current query.**

## When to Use

- Personalized assistants that remember user preferences
- Multi-session agents that maintain continuity
- Any agent where past context improves current response quality

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `user_message` | `str` | Current user input |
| `memory_store` | `VectorStore` | Indexed past memories |
| `top_k` | `int` | Number of memories to inject (default: 5) |
| `base_system` | `str` | Core system prompt |
| → `response` | `str` | Model response with memory context |

## Runnable Example

```python
import anthropic
from typing import List

client = anthropic.Anthropic()

# Simple in-memory store (replace with vector DB in production)
class SimpleMemoryStore:
    def __init__(self):
        self.memories: List[str] = []

    def add(self, memory: str):
        self.memories.append(memory)

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        # Production: use cosine similarity with embeddings
        # Here: return most recent k memories
        return self.memories[-top_k:]

    def save_from_conversation(self, user_msg: str, assistant_msg: str):
        """Extract and save memorable facts (use LLM extraction in prod)"""
        # Simple heuristic: save if it contains personal info
        keywords = ["my name", "i am", "i work", "i prefer", "i like", "i hate"]
        if any(k in user_msg.lower() for k in keywords):
            self.add(f"User said: {user_msg}")


def chat_with_memory(
    user_message: str,
    store: SimpleMemoryStore,
    base_system: str = "You are a helpful personal assistant."
) -> str:
    # 1. Retrieve relevant memories
    memories = store.retrieve(user_message, top_k=5)

    # 2. Build system prompt with injected memories
    if memories:
        memory_block = "\n".join(f"- {m}" for m in memories)
        system = f"{base_system}\n\n## What you remember about this user:\n{memory_block}"
    else:
        system = base_system

    # 3. Call the model
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": user_message}]
    )

    answer = response.content[0].text

    # 4. Save memorable content from this turn
    store.save_from_conversation(user_message, answer)

    return answer


# Usage
store = SimpleMemoryStore()
store.add("User's name is Ossama")
store.add("User is a full-stack developer in Cairo")
store.add("User prefers Python and TypeScript")

print(chat_with_memory("What stack should I use for my new project?", store))
print(chat_with_memory("Do you remember what I do for work?", store))
```

## Production Upgrade Path

```
Simple list  →  SQLite + keyword search  →  pgvector  →  Pinecone/Qdrant
```

For production: use `text-embedding-3-small` or `voyage-3` to embed memories, store in a vector DB, and retrieve by cosine similarity against the current query embedding.

## Framework Support

| Framework | Tool | Notes |
|---|---|---|
| mem0 | `Memory.add()` / `Memory.search()` | Purpose-built, recommended |
| LangChain | `VectorStoreRetrieverMemory` | Solid, verbose config |
| LangGraph | Custom node in graph | Maximum flexibility |
| Zep | Hosted memory layer | Good for SaaS products |

## Failure Modes

| Failure | Cause | Fix |
|---|---|---|
| Stale memories | Old facts not updated | Add memory update + deduplication step |
| Too many memories | Injecting all K memories bloats prompt | Cap at 5, score by recency + relevance |
| Privacy leakage | Wrong user's memories injected | Always namespace by `user_id` |
| No memory extraction | Saving nothing | Use LLM to extract facts after each turn |

## Benchmarks

See → [`benchmarks/memory/injection-strategies.md`](../../benchmarks/memory/injection-strategies.md)

## Related Skills

- [`working-memory.md`](working-memory.md) — In-context message window management
- [`rag.md`](../09-agentic-patterns/rag.md) — Retrieval-augmented generation
- [`vector-store-retrieval.md`](vector-store-retrieval.md) — Building and querying vector stores

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-03 | Initial entry |
| v2 | 2026-04 | Full runnable example, production path, mem0 integration, failure modes |
