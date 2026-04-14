---
title: "Cross-Thread Memory"
category: 03-memory
level: advanced
stability: stable
description: "Share and recall information across separate LangGraph threads using an external memory store."
added: "2026-04"
version: v2
---

# Cross-Thread Memory
Category: memory | Level: advanced | Stability: stable | Version: v2

## Description
LangGraph threads are isolated by default — state from thread A is not visible in thread B. Cross-thread memory breaks this isolation by storing facts in an external store (e.g. LangGraph Store, Redis, Postgres) keyed by user or entity ID rather than thread ID. On each new thread, the agent queries the store to retrieve relevant memories before processing the user request, enabling personalisation across conversations.

## Inputs
- `store`: `InMemoryStore`, `RedisStore`, or custom store implementing LangGraph's `BaseStore`
- `namespace`: tuple identifying the memory scope (e.g. `("user", user_id)`)
- `key`: string key for a specific memory item
- `value`: dict to store

## Outputs
- Retrieved memory items injected into node state before LLM call
- Updated store after new facts are written by the graph

## Example
```python
from langgraph.store.memory import InMemoryStore
from langgraph.graph import StateGraph

store = InMemoryStore()

def remember(state, config, *, store):
    user_id = config["configurable"]["user_id"]
    store.put(("user", user_id), "name", {"value": state["name"]})
    return {}

def recall(state, config, *, store):
    user_id = config["configurable"]["user_id"]
    mem = store.get(("user", user_id), "name")
    return {"recalled_name": mem.value["value"] if mem else "unknown"}
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| Namespace collision | User A sees User B memories | Always include unique user ID in namespace tuple |
| Memory store grows unbounded | High memory / storage costs | Implement TTL or LRU eviction policy |
| Stale memory retrieved | Agent acts on outdated info | Add `updated_at` field and ignore memories older than threshold |

## Prompt Patterns
**Basic:** `"Retrieve the user's stored preferences before answering."`

**Chain-of-Thought:** `"Check memory store → merge with current input → formulate personalised response."`

**Constrained Output:** `"Only write to memory if the user explicitly shares new personal information."`

## Model Comparison
| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---|---|---|---|
| Memory-aware response quality | ✅ Strong | ✅ Very Strong | ✅ Good |
| Store API usage accuracy | ✅ High | ✅ High | ⚠️ May lag on new APIs |
| Personalisation depth | ✅ Strong | ✅ Strong | ⚠️ Moderate |
| Long-context recall | ✅ 128k | ✅ 200k | ✅ 1M |
| Cost | Moderate | Moderate | Low |

## Related
- `agent-sessions.md` · `episodic-memory-replay.md` · `langgraph-checkpointing.md` · `thread-based-resume.md`

## Changelog
- v2 (2026-04): Full expansion
