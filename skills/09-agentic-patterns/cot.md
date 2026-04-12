# Chain of Thought (CoT)

**Category:** `agentic-patterns`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Prompt the model to produce explicit step-by-step reasoning before giving a final answer. Significantly improves accuracy on multi-step problems.

### Example

```
Q: A store sells apples for $0.50 each. Alice buys 14. How much does she pay?

Let me think step by step.
1. Each apple costs $0.50.
2. Alice buys 14 apples.
3. Total = 14 × $0.50 = $7.00

Answer: $7.00
```

### Variants

| Variant | Description |
|---|---|
| Zero-shot CoT | Append "Let's think step by step" to the prompt |
| Few-shot CoT | Provide worked examples before the question |
| Self-consistency | Sample multiple CoT paths and majority-vote |
| Least-to-most | Decompose problem into simpler sub-problems first |

### Related Skills

- [ReAct](react.md)
- [Tree of Thought](tot.md)
- [Self-Consistency](../02-reasoning/self-consistency.md)
