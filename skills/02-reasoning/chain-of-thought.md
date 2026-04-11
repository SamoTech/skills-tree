# Chain of Thought (CoT)

**Category:** `reasoning`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Instructs the model to reason step-by-step before producing a final answer, dramatically improving accuracy on complex tasks. Activated via prompting or natively in reasoning models.

### Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `problem` | `string` | ✅ | The question or task to reason about |
| `cot_trigger` | `string` | ❌ | Prompt trigger e.g. "Think step by step" |

### Outputs

| Output | Type | Description |
|---|---|---|
| `reasoning_trace` | `string` | The step-by-step reasoning chain |
| `answer` | `string` | The final answer after reasoning |

### Example

```python
prompt = """Q: Roger has 5 tennis balls. He buys 2 more cans of 3 balls each. How many does he have?
Let's think step by step."""
# Model: Roger starts with 5. 2 cans x 3 = 6 more. 5 + 6 = 11.
# Answer: 11
```

### Frameworks / Models

- All LLMs — via prompt engineering
- OpenAI o3, o4-mini — native extended thinking
- Claude 3.7 Sonnet — extended thinking mode
- Gemini 2.5 Pro — thinking mode

### Related Skills

- [ReAct](react.md)
- [Tree of Thought](tree-of-thought.md)
- [Self-Reflection](self-reflection.md)
