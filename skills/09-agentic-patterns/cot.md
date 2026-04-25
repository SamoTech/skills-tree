---
title: "Chain of Thought (CoT)"
category: 09-agentic-patterns
level: intermediate
stability: stable
description: "Prompt the model to produce explicit step-by-step reasoning before its answer. Reliably lifts accuracy on multi-step problems with no extra tools."
added: "2025-03"
version: v3
tags: [reasoning, prompting, accuracy]
updated: "2026-04"
dependencies:
  - package: anthropic
    min_version: "0.39.0"
    tested_version: "0.39.0"
    confidence: verified
code_blocks:
  - id: "example-cot"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-cot.json)

# Chain of Thought (CoT)

## Description

Forces the model to write out intermediate reasoning steps before its final answer. Pure prompting — no tools, no extra calls. On multi-step arithmetic, logic, and constrained planning, well-applied CoT typically lifts accuracy by **5–25 points** on frontier models, and far more on smaller ones.

## When to Use

- The problem decomposes naturally into sequential steps (math, multi-fact reasoning, constrained planning).
- Latency is acceptable (CoT roughly doubles output tokens).
- You don't need the model to call external tools — for those, use [ReAct](react.md).

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `question` | `str` | The user prompt |
| `style` | `Literal["zero_shot","few_shot","self_consistency"]` | Which CoT pattern to apply |
| `n_samples` | `int` | Used by `self_consistency`; default 5 |
| → `answer` | `str` | Final answer (parsed) |
| → `reasoning` | `str` | The full step-by-step trace |

## Runnable Example

```python
# pip install anthropic
from __future__ import annotations
import re
from collections import Counter
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-opus-4-5"

ZERO_SHOT = "Solve the problem step by step. End with a line: 'Answer: <value>'."
FEW_SHOT = """Solve step by step.

Q: A bag holds 12 marbles. 3 are red, 4 blue, the rest green. P(green)?
Step 1: 12 - 3 - 4 = 5 green.
Step 2: 5 / 12.
Answer: 5/12

Q: {question}"""

def parse_final(text: str) -> str:
    m = re.search(r"Answer:\s*(.+?)(?:\n|$)", text)
    return m.group(1).strip() if m else text.strip().splitlines()[-1]

def cot(question: str, style: str = "zero_shot", n_samples: int = 5) -> dict:
    if style == "zero_shot":
        msg = client.messages.create(
            model=MODEL, max_tokens=512,
            system=ZERO_SHOT,
            messages=[{"role": "user", "content": question}],
        )
        text = msg.content[0].text
        return {"answer": parse_final(text), "reasoning": text}

    if style == "few_shot":
        msg = client.messages.create(
            model=MODEL, max_tokens=512,
            messages=[{"role": "user", "content": FEW_SHOT.format(question=question)}],
        )
        text = msg.content[0].text
        return {"answer": parse_final(text), "reasoning": text}

    if style == "self_consistency":
        # Sample N reasoning chains with temperature, majority-vote the answer.
        answers, traces = [], []
        for _ in range(n_samples):
            msg = client.messages.create(
                model=MODEL, max_tokens=512, temperature=0.7,
                system=ZERO_SHOT,
                messages=[{"role": "user", "content": question}],
            )
            text = msg.content[0].text
            traces.append(text)
            answers.append(parse_final(text))
        majority, _ = Counter(answers).most_common(1)[0]
        return {"answer": majority, "reasoning": "\n---\n".join(traces),
                "vote_distribution": dict(Counter(answers))}

    raise ValueError(f"unknown style: {style}")

if __name__ == "__main__":
    q = "Alice has 14 apples at $0.50 each. She returns 3. How much did she pay net?"
    print(cot(q, style="zero_shot"))
    print(cot(q, style="self_consistency", n_samples=5))
```

## Variants

| Variant | Description | Best for |
|---|---|---|
| **Zero-shot CoT** | Append "think step by step" | Quick wins, no examples needed |
| **Few-shot CoT** | Show 2–4 worked examples | Domain-specific reasoning, schema adherence |
| **Self-consistency** | Sample N chains, majority-vote the answer | Math, multiple-choice — costs N× tokens |
| **Least-to-most** | Decompose into sub-problems first, solve each | Long, multi-part problems |
| **Auto-CoT** | Cluster similar Qs, generate diverse demos | When few-shot examples are scarce |

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Plausible-sounding wrong reasoning | Model commits to a flawed first step | Use self-consistency (vote across samples) |
| "Trace" matches a template, answer doesn't follow | Model copied few-shot pattern without solving | Inject a verifier step or decompose with [Planning](../02-reasoning/planning.md) (least-to-most) |
| Cost / latency blow-up | CoT roughly doubles output tokens | Cap output; turn off CoT for trivial classification |
| Final answer hard to parse | Free-form output | Force "Answer: <X>" suffix or structured output |
| Model leaks chain-of-thought in production | Reasoning shown to end users | Strip everything before "Answer:" before display |

## Frameworks & Models

| Framework | Implementation |
|---|---|
| Direct prompting | Any LLM API |
| LangChain | `ChatPromptTemplate` + parser |
| DSPy | `dspy.ChainOfThought(signature)` (auto-tunes the prompt) |
| OpenAI o-series | Reasoning is built-in; CoT is implicit |

## Model Comparison

| Capability | claude-opus-4-5 | gpt-4o | gemini-2.0-flash |
|---|---|---|---|
| GSM8K-style arithmetic | 5 | 5 | 4 |
| Multi-fact deduction | 5 | 4 | 3 |
| Trace fidelity (no leaps) | 5 | 4 | 3 |
| Cost-efficiency for self-consistency | 3 | 4 | 5 |

## Related Skills

- [ReAct](react.md) — CoT + tools
- [Tree of Thought](tot.md) — branched reasoning
- [Self-Consistency](../02-reasoning/self-consistency.md)
- [Planning](../02-reasoning/planning.md) — least-to-most variant lives here

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial entry |
| 2026-02 | v2 | Added variants table |
| 2026-04 | v3 | Full runnable example w/ self-consistency, failure modes, model comparison |
