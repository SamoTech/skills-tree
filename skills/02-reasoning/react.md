---
title: "ReAct (Reason + Act)"
category: 02-reasoning
level: intermediate
stability: stable
added: "2025-03"
description: "Apply ReAct reasoning in AI agent workflows."
dependencies:
  - package: anthropic
    min_version: "0.25.0"
    tested_version: "0.94.1"
    confidence: verified
code_blocks:
  - id: "example-react"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-react.json)

# ReAct (Reason + Act)

**Category:** `reasoning`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Interleave reasoning traces with tool actions: Thought → Action → Observation loops that ground reasoning in real-world feedback.

### Example

```python
# pip install anthropic
from anthropic import Anthropic

client = Anthropic()
tools = [
    {
        "name": "search",
        "description": "Search the web for current information.",
        "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
    }
]

response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What is the current price of Bitcoin?"}]
)
for block in response.content:
    if block.type == "tool_use":
        print(f"Tool: {block.name}, Input: {block.input}")
    else:
        print(f"Text: {block.text}")
```

### Advanced Techniques
- **Multi-turn ReAct**: feed tool results back as `tool_result` blocks for true Observation steps
- **Scratchpad pattern**: use `<thinking>` XML tags to separate reasoning from final output
- **Parallel tool calls**: pass multiple tools and let the model decide which to invoke simultaneously

### Related Skills
- `chain-of-thought`, `planning`, `tool-selection`, `self-correction`
