---
title: "Cross-Session Persistence"
category: 03-memory
level: advanced
stability: stable
tags: [memory, persistence, state, storage, sessions]
description: "Persist agent memory, state, and context across separate conversation sessions using external storage backends."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-cross-session-persistence.json)

# Cross-Session Persistence

**Category:** `memory`  
**Skill Level:** `advanced`  
**Stability:** `stable`  
**Added:** 2025-03

---

## Description

Cross-session persistence gives an agent a continuous identity across time. Without it, every new conversation starts from zero — the agent has no knowledge of past users, decisions, or learned preferences. With it, the agent can recall prior context, build longitudinal user models, and avoid asking the same questions twice.

The core pattern is straightforward: before a session ends, serialize the relevant state to a durable store. At the start of the next session, hydrate that state back into the agent's working context. The challenging part is deciding **what to persist**, **how to expire stale entries**, and **how to merge conflicting state** when sessions overlap or the user's situation has changed.

---

## When to Use

- The agent needs to remember user preferences, names, or prior decisions beyond one conversation
- Multi-step workflows that may span days or weeks (e.g. research assistants, project trackers)
- Any agentic system where continuity of identity matters for trust and UX
- Avoiding redundant grounding questions: "As I mentioned last time..."

---

## Storage Backend Options

| Backend | Best for | Notes |
|---|---|---|  
| JSON file / SQLite | Local dev, single-user tools | Simple but not concurrent-safe |
| Redis / Upstash | Low-latency read/write, TTL support | Ideal for web agents |
| PostgreSQL / Supabase | Relational queries, audit trail | Use `jsonb` column for flexible schema |
| Vector store (Pinecone, Qdrant) | Semantic retrieval of past episodes | Use alongside a scalar store |
| Object storage (S3, R2) | Large serialized state blobs | Slow reads; good for checkpointing |

---

## Implementation Pattern

```python
import json
from pathlib import Path
from datetime import datetime, timezone


class SessionMemory:
    """Simple file-backed cross-session memory store."""

    def __init__(self, user_id: str, store_dir: str = ".sessions"):
        self._path = Path(store_dir) / f"{user_id}.json"
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._data: dict = self._load()

    def _load(self) -> dict:
        if self._path.exists():
            try:
                return json.loads(self._path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value) -> None:
        self._data[key] = value
        self._data["_updated_at"] = datetime.now(timezone.utc).isoformat()

    def save(self) -> None:
        """Flush in-memory state to disk. Call at session end."""
        self._path.write_text(
            json.dumps(self._data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def clear(self, key: str) -> None:
        self._data.pop(key, None)
```

### Redis-Backed Pattern (production)

```python
import json
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

SESSION_TTL = 60 * 60 * 24 * 30  # 30 days


def save_session(user_id: str, state: dict) -> None:
    r.setex(f"session:{user_id}", SESSION_TTL, json.dumps(state))


def load_session(user_id: str) -> dict:
    raw = r.get(f"session:{user_id}")
    return json.loads(raw) if raw else {}


def patch_session(user_id: str, updates: dict) -> None:
    """Merge *updates* into existing session without a full overwrite."""
    state = load_session(user_id)
    state.update(updates)
    save_session(user_id, state)
```

---

## What to Persist

Not everything belongs in long-term memory. Apply the following tiers:

1. **Core identity** — user name, language preference, timezone, role
2. **Accumulated preferences** — topics the user finds important, formats they prefer
3. **Active task state** — in-progress goals, last-known checkpoint
4. **Important decisions** — choices the agent made on behalf of the user and why
5. **Expirable context** — current project, recent files — expire after N days of inactivity

Never persist raw conversation transcripts verbatim unless legally required. Instead, summarize and extract key facts (see [Memory Summarization](memory-summarization.md)).

---

## Pitfalls

- **Stale state rot**: Old preferences conflict with new ones. Always include an `_updated_at` timestamp and define explicit TTLs.
- **Schema drift**: Your data model evolves but persisted JSON does not. Use versioned schemas and migration functions.
- **Concurrency races**: Two agent threads writing simultaneously can corrupt state. Use optimistic locking or atomic Redis operations (`WATCH`/`MULTI`).
- **PII without consent**: Persisting user data requires a privacy policy and, in many jurisdictions, explicit consent. Design a `forget_me()` API from day one.
- **Over-persistence**: Saving too much creates noise at retrieval time. Be selective; prune aggressively.

---

## Related Skills

- [User Profile Memory](user-profile-memory.md)
- [Episodic Memory](episodic-memory.md)
- [Memory Summarization](memory-summarization.md)
- [RAG](rag.md)
- [Working Memory](working-memory.md)
