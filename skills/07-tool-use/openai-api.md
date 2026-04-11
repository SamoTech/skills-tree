# OpenAI API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Call OpenAI's GPT, embedding, image, audio, and fine-tuning endpoints via the official Python SDK or REST API.

### Example

```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[
        {'role': 'system', 'content': 'You are a helpful AI assistant.'},
        {'role': 'user', 'content': 'What is the skills-tree repository?'}
    ]
)
print(response.choices[0].message.content)
```

### Related Skills

- [Anthropic API](anthropic-api.md)
- [Function Calling](function-calling.md)
- [Embedding Generation](../12-data/embedding-generation.md)
