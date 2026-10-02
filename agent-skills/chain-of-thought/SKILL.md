---
name: chain-of-thought
description: Use structured intermediate reasoning techniques for multi-step tasks without requiring exposure of private chain-of-thought; return concise conclusions, assumptions, and verification steps.
metadata:
  source: skills/02-reasoning/chain-of-thought.md
  category: 02-reasoning
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-chain-of-thought.json)

# Chain of Thought

**Category:** `reasoning`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Prompt a model to reason step-by-step before producing a final answer, improving accuracy on multi-step and arithmetic tasks.

### Example

```python
# pip install anthropic
from anthropic import Anthropic

client = Anthropic()

def chain_of_thought(question: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Think step by step, then answer.\n\nQuestion: {question}\n\nReasoning:"
        }]
    )
    return response.content[0].text

print(chain_of_thought("If a train travels 60 mph for 2.5 hours, how far does it go?"))
```

### Advanced Techniques
- **Zero-shot CoT**: append "Let's think step by step" to any prompt
- **Self-consistency**: sample multiple CoT paths and majority-vote the final answer
- **Least-to-most prompting**: decompose into sub-problems, solve sequentially

### Related Skills
- `tree-of-thought`, `react`, `self-reflection`, `planning`

## Failure Modes

- Unsupported assumptions: state assumptions explicitly and separate them from observed inputs.
- Ambiguous or incomplete premises: return uncertainty or request the missing constraint rather than fabricating one.
- Resource or search explosion: bound candidate counts, iterations, recursion, and external tool calls.

## Evidence

- https://agentskills.io/specification
- https://github.com/openai/openai-python

Evidence status: references support implementation guidance; no performance benchmark is claimed without reproducible benchmark evidence.

## Failure Modes

- Private reasoning exposure: return concise conclusions and verification evidence rather than hidden chain-of-thought.
- Unsupported intermediate claims: identify assumptions and verify material steps.
- Excessive reasoning budget: bound iterations and stop when the requested result is established.

## Evidence

- https://agentskills.io/specification
- https://github.com/openai/openai-python

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
