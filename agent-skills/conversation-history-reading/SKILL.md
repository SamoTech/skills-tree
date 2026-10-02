---
name: conversation-history-reading
description: Normalize multi-turn conversation exports into a consistent message representation while preserving roles, timestamps, ordering, and provider-specific metadata. Use it before context selection, summarization, or memory injection.
metadata:
  source: skills/01-perception/conversation-history-reading.md
  category: 01-perception
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-conversation-history-reading.json)

# Conversation History Reading
Category: perception | Level: basic | Stability: stable | Version: v1

## Description
Load and structure multi-turn conversation histories from various formats (JSON, plain text, CSV exports) for context injection or analysis.

## Inputs
- `source`: file path or list of message dicts
- `format`: `openai` | `anthropic` | `plain` | `auto`

## Outputs
- Normalized message list: `[{role, content, timestamp}]`

## Example
```python
import json
with open("chat_export.json") as f:
    raw = json.load(f)
messages = [{"role": m["role"], "content": m["content"], "ts": m.get("created_at")} for m in raw["messages"]]
```

## Frameworks
| Framework | Method |
|---|---|
| LangChain | `ChatMessageHistory`, `FileChatMessageHistory` |
| LlamaIndex | `ChatMemoryBuffer` |
| mem0 | `memory.get_all()` |

## Failure Modes
- Role names differ across providers (`human` vs `user`)
- Token limit exceeded when injecting full history

## Related
- `text-reading.md` · `memory-injection.md` (03-memory)

## Changelog
- v1 (2026-04): Initial entry


## Evidence

The skill's implementation guidance is grounded in the following primary references:
- OpenAI conversation/message concepts: https://platform.openai.com/docs/guides/text
- Anthropic Messages API concepts: https://docs.anthropic.com/en/api/messages
- Agent Skills progressive-disclosure guidance: https://agentskills.io/specification

Evidence status: implementation guidance verified against the cited documentation; no benchmark claim is made unless a reproducible benchmark is included in this file.
