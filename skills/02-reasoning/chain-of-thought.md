---
title: "Chain of Thought"
category: 02-reasoning
level: intermediate
stability: stable
added: "2025-03"
description: "Apply chain of thought in AI agent workflows."
dependencies:
  - package: anthropic
    min_version: "0.25.0"
    tested_version: "0.94.1"
    confidence: verified
code_blocks:
  - id: "example-cot"
    type: executable
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
