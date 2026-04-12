# Memory-First Agent Blueprint

**Category:** blueprints | **Stability:** stable | **Version:** v1

## What This Solves

Most agents are stateless — every conversation starts from zero. This blueprint wires three complementary memory layers (user profile, episodic past interactions, semantic vector store) into a unified memory system that is loaded before every turn and updated after every resolved interaction.

**Use when:**
- Users return across multiple sessions
- Personalization improves task quality
- You want the agent to "remember" facts without user repetition

---

## Three Memory Layers

| Layer | What It Stores | Storage | Retrieval |
|---|---|---|---|
| **Profile** | Stable user facts (name, prefs, plan) | Key-value DB | Always loaded |
| **Episodic** | Past conversation summaries | Document store | Last 5 sessions |
| **Semantic** | Long-term knowledge, user docs | Vector DB | Top-K similarity |

---

## Architecture

```
  User Message
       │
       ▼
  Memory Retrieval (parallel)
  ┌────────┬────────┬────────┐
  │ Profile  │ Episodic │ Semantic │
  └────────┴────────┴────────┘
            │
       Memory Injector
       (builds system prompt)
            │
       LLM Agent Turn
            │
       Memory Updater
  ┌────────┬────────┬────────┐
  │ Update   │ Append   │  Embed   │
  │ Profile  │ Episode  │  + Store │
  └────────┴────────┴────────┘
```

---

## Full Implementation

```python
import anthropic
import json
from dataclasses import dataclass, field
from typing import Optional

client = anthropic.Anthropic()

# --- Storage (replace with real DB in production) ---
PROFILE_STORE: dict[str, dict] = {}
EPISODIC_STORE: dict[str, list[str]] = {}
VECTOR_STORE: list[dict] = []  # [{text, embedding, user_id}]

@dataclass
class MemoryContext:
    profile: dict
    recent_episodes: list[str]
    semantic_memories: list[str]

    def to_prompt(self) -> str:
        profile_text = json.dumps(self.profile, indent=2)
        episodes_text = "\n".join([f"- {e}" for e in self.recent_episodes])
        semantic_text = "\n".join([f"- {m}" for m in self.semantic_memories])
        return f"""## User Profile\n{profile_text}\n\n## Recent Sessions\n{episodes_text}\n\n## Relevant Knowledge\n{semantic_text}"""

def get_embedding(text: str) -> list[float]:
    """Get text embedding via OpenAI (swap for any embedding API)."""
    import httpx, os
    r = httpx.post(
        "https://api.openai.com/v1/embeddings",
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
        json={"model": "text-embedding-3-small", "input": text}
    )
    return r.json()["data"][0]["embedding"]

def cosine_similarity(a: list[float], b: list[float]) -> float:
    import math
    dot = sum(x*y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x**2 for x in a))
    norm_b = math.sqrt(sum(x**2 for x in b))
    return dot / (norm_a * norm_b + 1e-8)

def retrieve_memory(user_id: str, query: str, top_k: int = 3) -> MemoryContext:
    """Load all three memory layers for a user."""
    profile = PROFILE_STORE.get(user_id, {"user_id": user_id})
    episodes = EPISODIC_STORE.get(user_id, [])[-5:]  # last 5

    # Semantic retrieval
    semantic = []
    if VECTOR_STORE:
        query_emb = get_embedding(query)
        scored = [
            (cosine_similarity(query_emb, m["embedding"]), m["text"])
            for m in VECTOR_STORE if m.get("user_id") == user_id
        ]
        scored.sort(reverse=True)
        semantic = [text for _, text in scored[:top_k]]

    return MemoryContext(profile=profile, recent_episodes=episodes, semantic_memories=semantic)

UPDATE_SYSTEM = """
Based on this conversation, extract memory updates. Output JSON:
{
  "profile_updates": {"key": "value"},  // only new/changed facts
  "episode_summary": "one sentence summary of this interaction",
  "new_knowledge": ["fact to remember", ...]  // long-term facts to embed
}
Only include facts that would genuinely help future interactions.
"""

def update_memory(user_id: str, conversation: list[dict], memory: MemoryContext):
    """Extract and store memory updates after each turn."""
    conv_text = json.dumps(conversation[-4:])  # last 4 messages
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        system=UPDATE_SYSTEM,
        messages=[{"role": "user", "content": conv_text}]
    )
    updates = json.loads(response.content[0].text)

    # Update profile
    PROFILE_STORE.setdefault(user_id, {}).update(updates.get("profile_updates", {}))

    # Append episode
    EPISODIC_STORE.setdefault(user_id, []).append(updates["episode_summary"])

    # Embed and store new knowledge
    for fact in updates.get("new_knowledge", []):
        VECTOR_STORE.append({"text": fact, "embedding": get_embedding(fact), "user_id": user_id})

BASE_SYSTEM = "You are a helpful personal assistant with access to the user's memory."

def agent_turn(user_id: str, user_message: str, conversation: list[dict]) -> str:
    """Run one turn of the memory-first agent."""
    memory = retrieve_memory(user_id, query=user_message)
    system_prompt = f"{BASE_SYSTEM}\n\n{memory.to_prompt()}"

    conversation.append({"role": "user", "content": user_message})
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=system_prompt,
        messages=conversation
    )
    reply = response.content[0].text
    conversation.append({"role": "assistant", "content": reply})

    update_memory(user_id, conversation, memory)
    return reply

# Usage
if __name__ == "__main__":
    conversation = []
    print(agent_turn("user_ossama", "I prefer dark mode and I'm building a Next.js app.", conversation))
    print(agent_turn("user_ossama", "What do you know about me?", conversation))
```

---

## Failure Modes

| Failure | Mitigation |
|---|---|
| Memory injection too large | Summarize episodes if > 500 tokens total |
| Stale profile data | Add `last_updated` to profile, expire after 30 days |
| Irrelevant semantic retrieval | Set minimum similarity threshold (0.7) |
| Memory update invents facts | Instruct updater to only extract explicitly stated facts |

---

## Related

- `blueprints/rag-stack.md` — The semantic layer in detail
- `skills/03-memory/memory-injection.md` · `skills/03-memory/episodic.md`
- `benchmarks/memory/injection-strategies.md`

## Changelog

- **v1** (2026-04) — Initial blueprint: three-layer memory, injection, extraction, vector store
