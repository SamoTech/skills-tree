![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-anthropic-api.json)

# Anthropic API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Call Anthropic's Claude models via the Messages API for text generation, tool use, vision, and long-context tasks.

### Example

```python
import anthropic
client = anthropic.Anthropic()
msg = client.messages.create(
    model='claude-opus-4-5',
    max_tokens=1024,
    messages=[{'role': 'user', 'content': 'List 5 advanced AI agent skills.'}]
)
print(msg.content[0].text)
```

### Related Skills

- [OpenAI API](openai-api.md)
- [Function Calling](function-calling.md)
