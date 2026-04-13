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
