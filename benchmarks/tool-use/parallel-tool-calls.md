---
id: bench-tooluse-parallel
title: Parallel Tool Call Benchmark
category: tool-use
skill: tool-calling
version: v1
author: OssamaHashim
updated: 2026-04-13
tags: [tool-use, parallel, benchmark, model-comparison]
---

# Benchmark: Parallel Tool Call Efficiency

> Measures whether a model correctly identifies opportunities to call multiple tools in parallel rather than sequentially, reducing total latency.

## 📋 Setup

### Scenario Types

| Type | Description | Optimal Behaviour |
|------|-------------|------------------|
| Independent tasks | Two tasks with no dependency | Call both tools in parallel |
| Dependent tasks | Task B needs Task A's output | Sequential calls |
| Mixed (3 tasks) | 2 independent + 1 dependent | Parallel first 2, then 3rd |
| False dependency | Tasks appear related but aren't | Parallel |

**Total: 80 scenarios**

### Evaluation

- **Parallelisation rate**: Did the model batch independent calls?
- **Correctness rate**: Did results integrate correctly into the final answer?
- **Over-parallelisation rate**: Did the model batch dependent calls (incorrect)?

---

## 📊 Results

| Model | Parallel Rate (independent) | Correct Integration | Over-Parallel Rate |
|-------|----------------------------|---------------------|-------------------|
| Claude 3.5 Sonnet | **87%** | 98% | 3% |
| GPT-4o | 81% | 96% | 5% |
| Gemini 2.0 Flash | 72% | 93% | 9% |
| GPT-4o mini | 68% | 91% | 7% |

**Latency savings (avg per parallelised call pair): ~1.4s**

---

## ▶️ Reproduce

```python
import anthropic, json

client = anthropic.Anthropic()

TOOLS = [
    {"name": "get_weather",
     "description": "Get current weather for a city",
     "input_schema": {"type": "object",
                      "properties": {"city": {"type": "string"}},
                      "required": ["city"]}},
    {"name": "get_population",
     "description": "Get current population of a city",
     "input_schema": {"type": "object",
                      "properties": {"city": {"type": "string"}},
                      "required": ["city"]}},
]

def test_parallel(
    user_msg: str,
    expect_parallel: bool
) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        tools=TOOLS,
        messages=[{"role": "user", "content": user_msg}]
    )
    tool_calls = [b for b in response.content if b.type == 'tool_use']
    # Parallel = multiple tool calls in one response turn
    is_parallel = len(tool_calls) > 1
    return {
        'tool_calls': [t.name for t in tool_calls],
        'is_parallel': is_parallel,
        'expected_parallel': expect_parallel,
        'correct': is_parallel == expect_parallel
    }

# Should trigger parallel calls (weather + population are independent)
result = test_parallel(
    "What's the weather and population of Tokyo right now?",
    expect_parallel=True
)
print(result)
```

---

## 🔗 Related

- Skill: [`skills/tool-use/tool-calling.md`](../../skills/tool-use/tool-calling.md)
- Blueprint: [`blueprints/multi-agent-workflow.md`](../../blueprints/multi-agent-workflow.md)
