# Memory Injection

**Category:** `memory`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Store new information into a persistent memory store — vector database, key-value store, or structured database — so future agent turns can retrieve it. Handles deduplication, relevance scoring, and context-aware tagging at write time. Supports episodic memory ("what happened"), semantic memory ("what is true"), and procedural memory ("how to do it").

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `content` | `string` | ✅ | The information to store |
| `memory_type` | `string` | ❌ | `episodic`, `semantic`, `procedural` (default: `semantic`) |
| `tags` | `list` | ❌ | Optional category tags for retrieval filtering |
| `user_id` | `string` | ❌ | Owner user/session identifier |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `memory_id` | `string` | Unique ID of the stored memory |
| `deduplicated` | `bool` | Whether a near-duplicate was found and merged |
| `summary` | `string` | Condensed form stored (if original was compressed) |

---

## Example

```python
import anthropic
from mem0 import MemoryClient
import json

llm_client = anthropic.Anthropic()
mem_client = MemoryClient()  # requires MEM0_API_KEY

def smart_memory_inject(content: str, user_id: str, memory_type: str = "semantic") -> dict:
    """
    Extract key facts from content and store as structured memories.
    """
    # Extract facts worth storing
    extract_response = llm_client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": (
                f"From this content, extract key facts worth remembering as {memory_type} memory.\n"
                "Return JSON: {\"facts\": [\"fact 1\", \"fact 2\", ...]}\n"
                "Exclude ephemeral or low-value details. Return ONLY valid JSON.\n\n"
                f"Content:\n{content}"
            )
        }]
    )
    facts = json.loads(extract_response.content[0].text)["facts"]

    # Store each fact
    stored = []
    for fact in facts:
        result = mem_client.add(
            messages=[{"role": "user", "content": fact}],
            user_id=user_id,
            metadata={"type": memory_type}
        )
        stored.append(result)

    return {"stored_count": len(stored), "facts": facts}

result = smart_memory_inject(
    content="The user mentioned they are building a SaaS product in Next.js, prefers TypeScript, and deploys to Vercel.",
    user_id="ossama",
    memory_type="semantic"
)
print(json.dumps(result, indent=2))
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| mem0 | `MemoryClient.add()` | v1.0 |
| LangChain | `VectorStore.add_texts()` | v0.1 |
| LangGraph | Memory write node | v0.1 |

---

## Notes

- Extract facts before storing — storing raw conversation turns wastes vector space
- Tag memories at write time; retroactive tagging is expensive
- Implement deduplication by checking cosine similarity > 0.95 before inserting

---

## Related Skills

- [Memory Summarization](memory-summarization.md) — compressing before storing
- [Forgetting](forgetting.md) — removing stored memories
- [User Profile](user-profile.md) — user-scoped memory management

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: fact extraction + mem0 injection example, dedup note |
| `2025-03` | Initial stub entry |
