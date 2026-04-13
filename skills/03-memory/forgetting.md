![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-forgetting.json)

# Forgetting

**Category:** `memory`  
**Skill Level:** `advanced`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Selectively remove, suppress, or down-weight stored memories to maintain context relevance, comply with privacy regulations (GDPR right to erasure), prevent confidential data leakage, and reduce context window bloat. Implements both hard deletion (removing memory records) and soft suppression (marking memories as excluded from retrieval).

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `memory_store` | `object` | ✅ | The memory store to operate on |
| `criteria` | `dict` | ✅ | Deletion criteria: `{older_than_days, user_id, topic_tags, content_match}` |
| `mode` | `string` | ❌ | `hard_delete` or `soft_suppress` (default: `soft_suppress`) |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `deleted_count` | `int` | Number of memories removed or suppressed |
| `retained_count` | `int` | Memories kept |
| `summary` | `string` | Human-readable report of what was removed |

---

## Example

```python
import anthropic
import json
from datetime import datetime, timedelta

client = anthropic.Anthropic()

def classify_memories_for_deletion(
    memories: list[dict],
    criteria: dict
) -> dict:
    """
    Use LLM to classify memories into keep/delete based on natural-language criteria.
    memories: [{id, content, created_at, tags}]
    criteria: {reason, instructions}
    """
    mem_text = json.dumps(memories, indent=2, default=str)
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": (
                f"Deletion criteria: {criteria['instructions']}\n\n"
                f"Memories:\n{mem_text}\n\n"
                "For each memory, return JSON with:\n"
                "- decisions: [{id, action (keep|delete), reason}]\n"
                "- summary: how many and why\n"
                "Return ONLY valid JSON."
            )
        }]
    )
    return json.loads(response.content[0].text)

memories = [
    {"id": "m1", "content": "User's home address: 123 Main St", "created_at": "2025-01-01", "tags": ["pii"]},
    {"id": "m2", "content": "User prefers dark mode", "created_at": "2025-06-01", "tags": ["preference"]},
    {"id": "m3", "content": "User's credit card last 4: 4242", "created_at": "2025-01-15", "tags": ["pii", "financial"]},
]

result = classify_memories_for_deletion(
    memories,
    criteria={"instructions": "Delete all PII and financial data per GDPR erasure request"}
)
print(json.dumps(result, indent=2))
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| LangChain | `VectorStore.delete()` by id | v0.2 |
| LangGraph | Memory management node | v0.1 |
| mem0 | `client.memory.delete()` | v1.0 |

---

## Notes

- Always log deleted memory IDs for audit purposes before hard deletion
- GDPR erasure requests must propagate to all downstream storage (vector store, relational DB, backups)
- Combine with [Memory Summarization](memory-summarization.md) to compact before deleting redundant details

---

## Related Skills

- [Memory Injection](memory-injection.md) — adding memories
- [Memory Summarization](memory-summarization.md) — compaction before deletion
- [User Profile](user-profile.md) — managing user-level memory

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: GDPR use-case, LLM classification example, hard vs soft delete |
| `2025-03` | Initial stub entry |
