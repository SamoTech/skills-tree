# Path: Memory-First Agent

**Difficulty:** ⭐⭐ Intermediate  
**Skills:** 5  
**Est. Time:** ~3 hours  
**Goal:** Build an agent with persistent, queryable, multi-layer memory that remembers facts, user preferences, and past conversations.

---

## Overview

Most agents are stateless — every conversation starts from scratch. A Memory-First Agent maintains a structured memory store across sessions: short-term working memory, long-term semantic memory, and a user profile. This is the foundation of any personalised or long-running agent.

---

## Prerequisites

- Python 3.11+
- `pip install openai chromadb langchain`
- Basic understanding of vector embeddings

---

## The Path

### Step 1 — Working Memory
`skills/03-memory/working-memory.md`

**Why first:** The scratchpad. Working memory holds the current conversation turn, intermediate reasoning steps, and temporary variables. Every other memory layer builds on top of this.

**Key takeaways:**
- Keep working memory as a simple typed dict in the agent state
- Flush it at conversation end — it is not meant to persist
- Surface working memory explicitly to the LLM via a `<scratchpad>` section

---

### Step 2 — Memory Injection
`skills/03-memory/memory-injection.md`

**Why second:** You learn how to pull relevant memories from storage and inject them into the prompt at the right position. Bad injection order destroys context. This skill teaches the "memory window" pattern.

**Key takeaways:**
- Inject memories between system prompt and user message — not after
- Use recency + relevance scoring to select which memories to inject
- Cap injected memories at 800 tokens to preserve context budget

---

### Step 3 — Semantic Search
`skills/03-memory/semantic-search.md`

**Why third:** Long-term memory is only useful if the agent can retrieve the right memories at query time. Semantic search over an embedded memory store is the standard retrieval mechanism.

**Key takeaways:**
- Embed memories at write time, query at read time
- Use metadata filters (user_id, date, topic) to pre-filter before vector search
- Always return top-k=5 and let a re-ranker pick the final 2

---

### Step 4 — User Profile
`skills/03-memory/user-profile.md`

**Why fourth:** Facts about the user (name, preferences, goals, constraints) belong in a structured user profile, not scattered across semantic memory. This skill teaches profile construction, update triggers, and conflict resolution.

**Key takeaways:**
- Store profile as JSON with typed fields
- Update profile only when the user explicitly states a fact about themselves
- Surface profile fields as a `<user_context>` block in every system prompt

---

### Step 5 — Forgetting / Memory Decay
`skills/03-memory/forgetting.md`

**Why last:** Unlimited memory accumulation degrades retrieval quality over time. This skill teaches TTL-based expiry, relevance decay scoring, and controlled forgetting without losing important facts.

**Key takeaways:**
- Assign a TTL to every memory at write time based on its type
- Run a nightly decay job — reduce relevance score, delete below threshold
- Never delete user profile entries without explicit user request

---

## Code Scaffold

```python
# memory_agent.py — minimal multi-layer memory agent
import json
from datetime import datetime, timezone
from typing import TypedDict, List, Any
import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection("agent_memory")

class AgentState(TypedDict):
    session_id: str
    user_id: str
    working_memory: dict        # Step 1: transient
    user_profile: dict          # Step 4: structured user facts
    injected_memories: List[str] # Step 2: memories in current prompt

def write_memory(user_id: str, text: str, memory_type: str = "fact") -> None:
    """Embed and store a memory — skills/03-memory/semantic-search.md"""
    import openai
    resp = openai.embeddings.create(input=text, model="text-embedding-3-small")
    vec = resp.data[0].embedding
    collection.add(
        ids=[f"{user_id}-{datetime.now(timezone.utc).timestamp()}"],
        embeddings=[vec],
        documents=[text],
        metadatas=[{"user_id": user_id, "type": memory_type,
                    "created": datetime.now(timezone.utc).isoformat()}]
    )

def retrieve_memories(user_id: str, query: str, k: int = 5) -> List[str]:
    """Retrieve relevant memories — skills/03-memory/semantic-search.md"""
    import openai
    resp = openai.embeddings.create(input=query, model="text-embedding-3-small")
    vec = resp.data[0].embedding
    results = collection.query(
        query_embeddings=[vec],
        n_results=k,
        where={"user_id": user_id}
    )
    return results["documents"][0] if results["documents"] else []

def inject_memories(memories: List[str], system_prompt: str) -> str:
    """Inject memories into prompt — skills/03-memory/memory-injection.md"""
    if not memories:
        return system_prompt
    block = "\n".join(f"- {m}" for m in memories[:5])
    return f"{system_prompt}\n\n<memory>\n{block}\n</memory>"

def update_profile(profile: dict, user_message: str) -> dict:
    """Extract and update user profile — skills/03-memory/user-profile.md"""
    # In production: call LLM to extract profile facts from user_message
    # profile["name"] = extracted_name  etc.
    return profile

def decay_memories(user_id: str, threshold_days: int = 30) -> None:
    """Remove stale memories — skills/03-memory/forgetting.md"""
    results = collection.get(where={"user_id": user_id})
    now = datetime.now(timezone.utc)
    to_delete = []
    for id_, meta in zip(results["ids"], results["metadatas"]):
        created = datetime.fromisoformat(meta.get("created", now.isoformat()))
        age = (now - created).days
        if age > threshold_days and meta.get("type") != "profile":
            to_delete.append(id_)
    if to_delete:
        collection.delete(ids=to_delete)
        print(f"[memory] Decayed {len(to_delete)} memories for {user_id}")

def chat(state: AgentState, user_message: str) -> str:
    """One turn of the memory-first agent."""
    import openai
    # 1. Update working memory
    state["working_memory"]["last_message"] = user_message
    # 2. Retrieve + inject relevant memories
    memories = retrieve_memories(state["user_id"], user_message)
    system = inject_memories(memories, "You are a helpful assistant with persistent memory.")
    # 3. Update user profile
    state["user_profile"] = update_profile(state["user_profile"], user_message)
    # 4. Call LLM
    resp = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user_message},
        ]
    )
    reply = resp.choices[0].message.content
    # 5. Write this exchange to long-term memory
    write_memory(state["user_id"], f"User: {user_message}\nAgent: {reply}")
    return reply
```

---

## Completion Checklist

- [ ] Agent recalls a fact stated 3 turns ago without re-prompting
- [ ] User profile persists across two separate Python process runs
- [ ] Memory injection stays under 800 tokens
- [ ] `decay_memories()` removes entries older than the threshold
- [ ] Semantic search returns contextually relevant memories, not just keyword matches

---

## Next Steps

- Add **episodic memory** (`skills/03-memory/episodic-memory.md`) for multi-session narrative recall
- Add **fact verification** (`skills/03-memory/fact-verification.md`) before writing to long-term store
- See the full system: `systems/memory-agent-system.md`
