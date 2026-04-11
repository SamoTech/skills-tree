# Anthropic API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

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
