---
title: "Self-Consistency"
category: 02-reasoning
level: intermediate
stability: stable
description: "Sample N independent reasoning chains for the same question and majority-vote the final answer. Trades cost for accuracy — robust on math and logic, surprisingly cheap with smaller-than-frontier models."
added: "2025-03"
version: v3
tags: [reasoning, sampling, accuracy, ensembling]
updated: "2026-04"
dependencies:
  - package: anthropic
    min_version: "0.39.0"
    tested_version: "0.39.0"
    confidence: verified
code_blocks:
  - id: "example-self-consistency"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-self-consistency.json)

# Self-Consistency

## Description

Self-consistency ([Wang et al., 2022](https://arxiv.org/abs/2203.11171)) augments [Chain of Thought](../09-agentic-patterns/cot.md) by sampling **N independent reasoning chains at temperature > 0**, parsing each one's final answer, and **majority-voting**. Wrong reasoning chains tend to scatter across many wrong answers; correct reasoning converges. So the modal answer is usually the right one.

It's the simplest "test-time compute" trick that exists, and it works. On GSM8K-style arithmetic, self-consistency typically lifts accuracy by 5–15 points over single-shot CoT at the cost of ~N× tokens.

## When to Use

- The task has a **single, parseable final answer** (math, logic, multiple-choice, classification).
- You can afford N× cost (typically 5).
- You don't have access to a reasoning-tuned model that already does this implicitly.
- **Don't use** when the answer is open-ended text — voting is meaningless on prose.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `question` | `str` | The prompt |
| `n_samples` | `int` | Number of independent chains (default 5) |
| `temperature` | `float` | Sampling temperature (default 0.7) |
| `parse_answer` | `Callable[[str], str]` | Extracts the final answer from a chain |
| → `answer` | `str` | Majority-voted answer |
| → `confidence` | `float` | `votes_for_winner / n_samples` |
| → `vote_distribution` | `dict[str,int]` | All answers seen |

## Runnable Example

```python
# pip install anthropic
from __future__ import annotations
import re
from collections import Counter
from typing import Callable
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-opus-4-5"

SYSTEM = (
    "Solve the problem step by step. End with a line exactly: 'Answer: <value>' "
    "where <value> is the final numeric or short-form answer."
)

def default_parse(text: str) -> str:
    m = re.search(r"Answer:\s*(.+?)(?:\n|$)", text)
    return m.group(1).strip().rstrip(".") if m else ""

def self_consistency(
    question: str,
    *,
    n_samples: int = 5,
    temperature: float = 0.7,
    parse_answer: Callable[[str], str] = default_parse,
) -> dict:
    answers: list[str] = []
    traces: list[str] = []
    for _ in range(n_samples):
        r = client.messages.create(
            model=MODEL, max_tokens=512, temperature=temperature,
            system=SYSTEM,
            messages=[{"role": "user", "content": question}],
        )
        text = r.content[0].text
        traces.append(text)
        ans = parse_answer(text)
        if ans:
            answers.append(ans)

    if not answers:
        raise ValueError("no parseable answers across samples")

    counter = Counter(answers)
    winner, count = counter.most_common(1)[0]
    return {
        "answer": winner,
        "confidence": count / n_samples,
        "vote_distribution": dict(counter),
        "traces": traces,
    }

if __name__ == "__main__":
    q = ("A train leaves town at 60 mph. After 2 hours, a second train leaves "
         "the same town at 90 mph. How long until the second catches the first?")
    out = self_consistency(q, n_samples=5)
    print(f"answer={out['answer']!r}  confidence={out['confidence']:.0%}")
    print(out["vote_distribution"])
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Tied vote (2-2-1) | Even N or genuinely uncertain | Use odd `n_samples`; on tie, increase N or surface low-confidence |
| All wrong, agreeing | Systematic bias in the model | Self-consistency does NOT fix this — change model or add a verifier |
| Answer parser drops valid responses | Format drift across samples | Make the system prompt rigid about the "Answer:" suffix |
| Cost spike at scale | N× tokens for every query | Only invoke when CoT confidence is low (cascade pattern) |
| High variance with temp=0 | Greedy decoding gives identical chains | Use `temperature ≥ 0.5`; lower kills diversity |

## Variants

| Variant | Description |
|---|---|
| **Vanilla self-consistency** | Above — equal-weight majority vote |
| **Weighted by chain length** | Penalise short, lazy chains |
| **Verifier-weighted** | Weight votes by a learned verifier's score |
| **Cascade** | Cheap single-shot first; only run self-consistency on low-confidence |
| **Implicit** (o-series, Claude reasoning) | The model does N internal samples; you just call it once |

## Frameworks & Models

| Framework | Notes |
|---|---|
| Direct API (above) | Full control over N, T, parser |
| OpenAI o-series | Self-consistency is internal — passing a higher `reasoning_effort` is your knob |
| Anthropic extended thinking | Same — `thinking.budget_tokens` is the knob |
| DSPy `Refine` / `Ensemble` | Programmatic |

## Model Comparison

| Capability | claude-opus-4-5 | gpt-4o | claude-haiku-4-5 |
|---|---|---|---|
| Diversity at temp=0.7 | 5 | 4 | 5 |
| Final-answer formatting | 5 | 5 | 4 |
| Cost-per-sample | 2 | 3 | 5 |
| Lift over single-shot CoT | 4 | 4 | 5 |

## Related Skills

- [Chain of Thought](../09-agentic-patterns/cot.md) — produces the chains
- [Reflection](../09-agentic-patterns/reflection.md) — alternative way to fix wrong answers
- [Tree of Thought](../09-agentic-patterns/tot.md) — branched search instead of i.i.d. sampling

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Stub (file did not exist; was a broken link target) |
| 2026-04 | v3 | Battle-tested skill: typed I/O, voting, failure modes, model comparison |
