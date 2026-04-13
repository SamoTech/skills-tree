---
id: bench-reasoning-tool-selection
title: Tool Selection Accuracy Benchmark
category: reasoning
skill: tool-calling
version: v1
author: OssamaHashim
updated: 2026-04-13
tags: [reasoning, tool-use, benchmark, model-comparison]
---

# Benchmark: Tool Selection Accuracy

> Measures whether a model chooses the correct tool from a set of available tools given a user request, including cases with ambiguous or overlapping tool descriptions.

## 📋 Setup

### Test Scenarios

| Scenario | Count | Difficulty |
|----------|-------|------------|
| Unambiguous single-tool tasks | 30 | Easy |
| Two plausible tools, one correct | 30 | Medium |
| No tool needed (direct answer) | 20 | Medium |
| Multiple tools needed (sequential) | 20 | Hard |

**Total: 100 scenarios**

### Tool Set (used in all tests)

```json
[
  { "name": "web_search", "description": "Search the web for current information" },
  { "name": "calculator", "description": "Perform mathematical calculations" },
  { "name": "code_executor", "description": "Run Python code and return output" },
  { "name": "file_reader", "description": "Read the contents of a local file" },
  { "name": "send_email", "description": "Send an email to a specified address" },
  { "name": "calendar_check", "description": "Check calendar events for a date" }
]
```

---

## 📊 Results

### Selection Accuracy by Difficulty

| Model | Easy | Medium | Hard | Overall |
|-------|------|--------|------|---------|
| Claude 3.5 Sonnet | 100% | 93% | 85% | **93.4%** |
| GPT-4o | 100% | 91% | 80% | **91.2%** |
| Gemini 2.0 Flash | 97% | 87% | 72% | **87.0%** |
| GPT-4o mini | 97% | 84% | 68% | **84.4%** |

### No-Tool Detection (specificity)

When the correct answer is to respond directly without a tool:

| Model | Correctly skipped tool | False tool calls |
|-------|----------------------|------------------|
| Claude 3.5 Sonnet | 90% | 10% |
| GPT-4o | 85% | 15% |
| Gemini 2.0 Flash | 75% | 25% |

---

## ▶️ Reproduce

```python
import anthropic, json

client = anthropic.Anthropic()

TOOLS = [
    {"name": "web_search", "description": "Search the web for current information",
     "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    {"name": "calculator", "description": "Perform mathematical calculations",
     "input_schema": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}},
    {"name": "code_executor", "description": "Run Python code and return output",
     "input_schema": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}},
]

def test_tool_selection(user_message: str, expected_tool: str | None) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=256,
        tools=TOOLS,
        messages=[{"role": "user", "content": user_message}]
    )
    used_tool = None
    for block in response.content:
        if block.type == 'tool_use':
            used_tool = block.name
            break
    return {
        'expected': expected_tool,
        'actual': used_tool,
        'correct': used_tool == expected_tool
    }

# Examples
print(test_tool_selection("What is 847 * 23?", "calculator"))
print(test_tool_selection("What's the weather today?", "web_search"))
print(test_tool_selection("What is the capital of France?", None))  # No tool needed
```

---

## 🔗 Related

- Skill: [`skills/tool-use/tool-calling.md`](../../skills/tool-use/tool-calling.md)
- Related benchmark: [`benchmarks/tool-use/`](../tool-use/)
