---
name: chain-of-thought
description: Use structured intermediate reasoning techniques for multi-step tasks without requiring exposure of private chain-of-thought; return concise conclusions, assumptions, and verification steps.
metadata:
  source: skills/02-reasoning/chain-of-thought.md
  category: 02-reasoning
  version: "v3"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-chain-of-thought.json)

# Chain of Thought

**Category:** `reasoning`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Prompt a model to reason step-by-step before producing a final answer, improving accuracy on multi-step and arithmetic tasks, and return concise conclusions, assumptions, and verification steps.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `question` | string | The multi-step task or question to reason about |
| Input | `constraints` | optional list of string | Stated constraints the reasoning must respect |
| Input | `budget` | optional integer | Maximum reasoning steps or tokens before stopping |
| Output | `answer` | string | The final conclusion, stated concisely |
| Output | `assumptions` | list of string | Assumptions the reasoning relied on |
| Output | `verification` | list of string | Checks that were run against the conclusion |

### Procedure
1. State the question, its constraints, and the stop condition before reasoning begins.
2. Decompose the task into ordered steps small enough to verify individually.
3. Reason step by step, keeping intermediate results explicit and checkable.
4. Verify material steps by recomputation, tool call, or a second reasoning pass.
5. Compress the reasoning into the answer plus assumptions and verification evidence.
6. Stop when the requested result is established or the budget is exhausted, and say which happened.

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
- [Tree of Thought](tree-of-thought.md)
- [ReAct](react.md)
- [Self Reflection](self-reflection.md)
- [Planning](planning.md)

## Failure Modes

- Private reasoning exposure: return concise conclusions and verification evidence rather than hidden chain-of-thought.
- Unsupported assumptions: state assumptions explicitly and separate them from observed inputs.
- Ambiguous or incomplete premises: return uncertainty or request the missing constraint rather than fabricating one.
- Resource or reasoning-budget explosion: bound candidate counts, iterations, and external tool calls.
- Confident wrong answers: verify material steps before presenting the conclusion as established.

## Changelog
- v3 (2026-11): Structural modernization; merged the duplicated failure-mode and evidence sections into one authoritative set, added the input/output contract table and procedure.
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification
- https://github.com/openai/openai-python

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
