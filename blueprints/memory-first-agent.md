---
title: Memory-First Agent
category: blueprints
version: v1
stability: stable
---

# Memory-First Agent

> Agent architecture where every interaction is immediately stored, indexed, and retrieved — combining working memory, episodic memory, and semantic vector search into a unified context layer.

## When to Use

- Long-running personal assistants that must remember user preferences
- Agents handling recurring tasks where past context changes future strategy
- Any agent where context window length is a bottleneck

## Memory Layers

| Layer | What It Stores | Retrieval |
|---|---|---|
| **Working** | Current turn state, scratch-pad | In-context (no retrieval needed) |
| **Episodic** | Past interactions, timestamped | Recency + relevance hybrid |
| **Semantic** | User profile, preferences, facts | Vector similarity (top-K) |
| **Procedural** | Successful plans / strategies | Tag-based lookup |

## Architecture

```
  User message
       │
       ▼
┌─────────────────────┐
│   Memory Retriever   │
│  (episodic + semantic)│
└────────┬────────────┘
         │ top-K memories
         ▼
┌─────────────────────┐
│  Context Assembler   │
│  system + memories   │
│  + user message      │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│    Agent (LLM)       │
└────────┬────────────┘
         │ response
         ▼
┌─────────────────────┐
│   Memory Writer      │
│ extract + embed      │
│ + store all layers   │
└─────────────────────┘
         │
      Final reply to user
```

## Implementation

```python
import anthropic
from datetime import datetime

client = anthropic.Anthropic()

EXTRACT_SYSTEM = """
From this conversation turn, extract memorable facts about the user.
Output JSON: {"facts": ["..."], "preference_updates": {"key": "value"}, "episode_summary": "..."}
Only include things worth remembering long-term.
"""

class MemoryFirstAgent:
    def __init__(self, user_id: str, vector_store, episodic_store):
        self.user_id = user_id
        self.vector_store = vector_store   # e.g., Supabase pgvector
        self.episodic_store = episodic_store  # e.g., simple list/DB
        self.working_memory = {}  # cleared each session

    def retrieve(self, query: str, top_k: int = 5) -> str:
        semantic_hits = self.vector_store.search(self.user_id, query, top_k=top_k)
        recent_episodes = self.episodic_store.get_recent(self.user_id, n=3)
        return (
            "### Recent Episodes\n" + "\n".join(f"- {e['ts']}: {e['summary']}" for e in recent_episodes) +
            "\n\n### Relevant Memories\n" + "\n".join(f"- {h['fact']}" for h in semantic_hits)
        )

    def respond(self, user_message: str) -> str:
        memory_ctx = self.retrieve(user_message)
        system = f"You are a personal assistant with memory.\n\n## Memory\n{memory_ctx}"

        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.content[0].text

        # Extract and store new memories
        import json
        extract_resp = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=512,
            system=EXTRACT_SYSTEM,
            messages=[{"role": "user", "content": f"User: {user_message}\nAgent: {reply}"}]
        )
        extracted = json.loads(extract_resp.content[0].text)

        for fact in extracted.get("facts", []):
            self.vector_store.upsert(self.user_id, fact)
        self.episodic_store.add(self.user_id, {
            "ts": datetime.utcnow().isoformat(),
            "summary": extracted.get("episode_summary", user_message[:100])
        })
        return reply
```

## Failure Modes

| Failure | Fix |
|---|---|
| Memory grows unbounded | Add TTL or importance-weighted forgetting |
| Wrong memories retrieved | Use hybrid retrieval: recency × cosine similarity |
| Extract step hallucinates facts | Add confidence threshold; only store high-confidence facts |
| Slow retrieval at scale | Pre-filter by user_id, use HNSW index |

## Related

- `skills/03-memory/memory-injection.md`
- `skills/03-memory/vector-store-retrieval.md`
- `systems/customer-support-bot.md`
- `blueprints/rag-stack.md`

## Changelog

- `v1` (2026-04) — Initial three-layer memory (episodic + semantic + working) with extract-on-write
