![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-function-calling.json)

# Function / Tool Calling

**Category:** `tool-use`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Invoke structured external functions defined in the model's tool schema. The model decides when and how to call each tool based on context.

### Example

```python
tools = [{
    'type': 'function',
    'function': {
        'name': 'get_weather',
        'description': 'Get current weather for a city',
        'parameters': {
            'type': 'object',
            'properties': {'city': {'type': 'string'}},
            'required': ['city']
        }
    }
}]
response = client.chat.completions.create(
    model='gpt-4o', messages=messages, tools=tools
)
```

### Frameworks

- OpenAI function calling
- Anthropic tool use
- Gemini function declarations
- LangChain tools

### Related Skills

- [MCP Tool](mcp-tool.md)
- [ReAct](../02-reasoning/react.md)
