---
title: "Memory Summarization"
category: 03-memory
level: intermediate
stability: stable
description: "Apply memory summarization in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-memory-summarization.json)

# Memory Summarization

**Category:** `memory`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Compress a large set of stored memories, conversation turns, or retrieved documents into a compact, information-dense summary. Reduces context window usage while preserving the most actionable facts. Supports rolling summaries (incremental) and batch summarization (full history at once). Essential for long-running agents and chatbots that accumulate context over many sessions.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `memories` | `list` | ✅ | List of memory strings or `{content, created_at}` dicts |
| `target_length` | `int` | ❌ | Max tokens in summary (default: 500) |
| `focus` | `string` | ❌ | Topic or question to summarize toward |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `summary` | `string` | Compressed memory summary |
| `retained_ids` | `list` | Memory IDs preserved verbatim (high-importance) |
| `dropped_count` | `int` | Number of memories fully absorbed into summary |

---

## Example

```python
import anthropic
import json

client = anthropic.Anthropic()

def summarize_memory_window(memories: list[str], focus: str = "") -> dict:
    """
    Compress a list of memory strings into a concise summary.
    """
    mem_block = "\n".join(f"- {m}" for m in memories)
    focus_hint = f"\nFocus the summary on: {focus}" if focus else ""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": (
                f"Memories to compress:{focus_hint}\n\n{mem_block}\n\n"
                "Return JSON with:\n"
                "- summary: compressed paragraph preserving all actionable facts\n"
                "- key_facts: list of the 5 most important facts extracted\n"
                "- dropped_topics: list of topics that were de-prioritized\n"
                "Return ONLY valid JSON."
            )
        }]
    )
    return json.loads(response.content[0].text)

memories = [
    "User is building a SaaS app with Next.js",
    "User deploys to Vercel",
    "User prefers TypeScript over JavaScript",
    "User asked about rate limiting in April 2026",
    "User mentioned budget is $200/month for infra",
    "User's team has 3 engineers",
    "User asked about Stripe integration last session",
]

result = summarize_memory_window(memories, focus="technical preferences and constraints")
print(json.dumps(result, indent=2))
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Claude claude-opus-4-5 | Direct prompt | 2024-06 |
| LangChain | `ConversationSummaryMemory` | v0.1 |
| mem0 | Built-in memory consolidation | v1.0 |

---

## Notes

- For rolling summaries, append the previous summary + new memories and re-summarize
- Preserve verbatim memories that contain unique identifiers, credentials, or exact values
- Run summarization when the memory store exceeds a token threshold (e.g., 80% of context limit)

---

## Related Skills

- [Memory Injection](memory-injection.md) — storing summaries back to memory
- [Forgetting](forgetting.md) — deleting low-value memories after summarization
- [User Profile](user-profile.md) — user-scoped memory

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: rolling summary pattern, compression example, notes |
| `2025-03` | Initial stub entry |
