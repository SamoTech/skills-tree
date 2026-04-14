---
title: "User Profile"
category: 03-memory
level: intermediate
stability: stable
description: "Apply user profile in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-user-profile.json)

# User Profile

**Category:** `memory`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Build, maintain, and query a structured user profile derived from conversations and explicit inputs. Captures preferences, constraints, expertise level, communication style, goals, and behavioral patterns. Injected into agent prompts to personalize responses, recommendations, and workflows without requiring the user to re-explain context each session.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `user_id` | `string` | ✅ | Unique identifier for the user or session |
| `conversation` | `list` | ❌ | Recent messages to extract new profile signals from |
| `explicit_update` | `dict` | ❌ | Direct profile update from user (`{field: value}`) |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `profile` | `dict` | Full structured user profile |
| `new_signals` | `list` | Newly detected preferences or facts from this session |
| `updated_fields` | `list` | Fields that changed from last session |

---

## Example

```python type:illustrative
# pip install mem0ai anthropic
# Note: `mem0` is the import name for PyPI package `mem0ai`
import anthropic
from mem0 import MemoryClient
import json

llm_client = anthropic.Anthropic()
mem_client = MemoryClient()

def extract_and_update_profile(messages: list[dict], user_id: str) -> dict:
    """
    Extract new user signals from conversation and update the profile.
    messages: [{role, content}]
    """
    conv_text = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)

    response = llm_client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": (
                "Extract profile signals from this conversation.\n"
                "Return JSON: {\"signals\": [{\"field\": str, \"value\": str, \"confidence\": 0-1}]}\n"
                "Fields: name, expertise_level, preferred_language, preferred_stack, "
                "communication_style, timezone, goals, constraints, tools_used.\n"
                "Only include fields with high confidence (>0.7). Return ONLY valid JSON.\n\n"
                f"Conversation:\n{conv_text}"
            )
        }]
    )
    signals = json.loads(response.content[0].text)["signals"]

    for signal in signals:
        if signal["confidence"] >= 0.7:
            mem_client.add(
                messages=[{"role": "user", "content": f"{signal['field']}: {signal['value']}"}],
                user_id=user_id,
                metadata={"type": "user_profile", "field": signal["field"]}
            )

    return {"stored_signals": len(signals), "signals": signals}

def get_profile_context(user_id: str, task: str) -> str:
    """Retrieve relevant profile context for a given task."""
    memories = mem_client.search(task, user_id=user_id, limit=10)
    profile_memories = [m for m in memories if m.get("metadata", {}).get("type") == "user_profile"]
    return "\n".join(m["memory"] for m in profile_memories)

# Usage
extract_and_update_profile(
    messages=[
        {"role": "user", "content": "I'm working on a Next.js SaaS app deployed on Vercel"},
        {"role": "assistant", "content": "Got it! What features are you building?"},
        {"role": "user", "content": "Rate limiting and Stripe billing. I prefer TypeScript."},
    ],
    user_id="ossama"
)
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| mem0ai | `add()` with `user_profile` metadata | v1.0 |
| LangChain | `ConversationEntityMemory` | v0.1 |
| LangGraph | Profile extraction node | v0.1 |

---

## Notes

- Only store signals with confidence ≥ 0.7 to avoid polluting the profile with guesses
- Re-run extraction every N turns and merge with existing profile
- Inject the profile as a system prompt prefix, not in the user turn
- Respect user requests to delete profile data ([Forgetting](forgetting.md))

---

## Related Skills

- [Memory Injection](memory-injection.md) — storing profile data
- [Forgetting](forgetting.md) — GDPR erasure of user profiles
- [Memory Summarization](memory-summarization.md) — condensing profile history

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Annotated code block as type:illustrative to clarify mem0 import name |
| `2026-04` | Fixed PyPI package name: mem0 → mem0ai |
| `2026-04` | Expanded from stub: signal extraction + mem0 storage example, confidence threshold |
| `2025-03` | Initial stub entry |
