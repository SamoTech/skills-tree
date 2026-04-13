---
title: Chain of Thought (CoT)
category: 02-reasoning
level: basic
stability: stable
description: "Apply chain of thought in AI agent workflows."
version: v2
tags: [reasoning, prompting, decomposition]
updated: 2026-04
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-chain-of-thought.json)

# Chain of Thought (CoT)

## What It Does

Chain of Thought prompting instructs the model to write out its reasoning step-by-step before giving a final answer. Adding "think step by step" or providing a few worked examples with reasoning traces dramatically improves accuracy on math, logic, and multi-step problems.

## When to Use

- Math and arithmetic problems
- Multi-step logical deductions
- Tasks where showing work improves answer quality
- Any case where the model is making errors on seemingly easy tasks

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `problem` | `str` | The question or task |
| `cot_style` | `str` | `zero-shot` ("think step by step") or `few-shot` (examples) |
| → `reasoning` | `str` | The step-by-step trace |
| → `answer` | `str` | Final answer extracted from trace |

## Runnable Example

```python
import anthropic

client = anthropic.Anthropic()

def chain_of_thought(problem: str, few_shot: bool = False) -> dict:
    if few_shot:
        system = """Solve problems step by step, showing your reasoning.

Example:
Q: A store has 48 apples. They sell 1/3 in the morning and 1/4 of the rest in the afternoon. How many remain?
A: Step 1: Morning sales = 48 × 1/3 = 16 apples
   Step 2: Remaining after morning = 48 - 16 = 32 apples  
   Step 3: Afternoon sales = 32 × 1/4 = 8 apples
   Step 4: Final remaining = 32 - 8 = 24 apples
   Answer: 24 apples"""
    else:
        system = "Think step by step before giving your final answer. End with 'Answer: <answer>'"

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": problem}]
    )

    text = response.content[0].text
    answer = text.split("Answer:")[-1].strip() if "Answer:" in text else text
    return {"reasoning": text, "answer": answer}

result = chain_of_thought(
    "If a train travels 120km in 1.5 hours, then slows to 60km/h for 45 minutes, what is the total distance?"
)
print(result["answer"])
```

## Variants

| Variant | Description | Best For |
|---|---|---|
| **Zero-shot CoT** | "Think step by step" suffix | Quick, no examples needed |
| **Few-shot CoT** | Provide 2-3 worked examples | Higher accuracy, domain-specific |
| **Self-consistency** | Sample N traces, majority vote | Maximum accuracy, higher cost |
| **Program of Thought** | Write code instead of prose | Math, computation |
| **Step-Back** | Ask a general principle first | Abstract reasoning |

## Failure Modes

| Failure | Cause | Fix |
|---|---|---|
| Confident wrong reasoning | Model commits to early error | Use self-consistency (sample 5, vote) |
| Verbose but wrong | Long trace ≠ correct trace | Add "verify each step" instruction |
| Skips steps on easy problems | Model shortcuts | Enforce step count in prompt |

## Related Skills

- [`react.md`](react.md) — CoT + tool calls
- [`tree-of-thought.md`](tree-of-thought.md) — Branching reasoning
- [`self-consistency.md`](self-consistency.md) — Majority-vote sampling

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-02 | Initial entry |
| v2 | 2026-04 | Added variants table, runnable example, failure modes |
