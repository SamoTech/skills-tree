---
id: lab-reasoning-self-consistency
title: Self-Consistency Sampling
category: reasoning
status: experimental
stability: beta
author: OssamaHashim
updated: 2026-04-13
tags: [reasoning, sampling, ensemble, labs]
readiness: Beta — works well for closed-form tasks, limited for open-ended
---

# Lab: Self-Consistency Sampling

> **⚗️ Experimental (Beta)** — Well-established in research; production-viable for closed-form tasks (math, classification). Open for contribution to extend to open-ended tasks.

## What Is It?

Self-consistency samples the model multiple times with temperature > 0, then takes a **majority vote** across outputs. It exploits the insight that correct reasoning paths are more diverse than incorrect ones — wrong answers cluster at local optima while right answers spread across valid solution paths.

## When It Helps

- **Multi-step math**: +8-15% over greedy on GSM8K-class problems
- **Code generation**: Majority vote across N completions improves pass@1
- **Classification with CoT**: More stable than single-sample

## When It Doesn't

- Open-ended text generation (no canonical "majority")
- Tasks requiring tool calls (outputs aren't easily comparable)
- Latency-critical applications (N× cost)

## Implementation

```python
import anthropic
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

client = anthropic.Anthropic()

def single_sample(prompt: str, model: str, temperature: float) -> str:
    resp = client.messages.create(
        model=model,
        max_tokens=512,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.content[0].text.strip()

def extract_answer(text: str) -> str:
    """Extract final answer from CoT output."""
    for line in reversed(text.splitlines()):
        line = line.strip()
        if line.startswith('Answer:'):
            return line.replace('Answer:', '').strip()
    # Fallback: last non-empty line
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return lines[-1] if lines else text

def self_consistency(
    problem: str,
    n_samples: int = 5,
    temperature: float = 0.7,
    model: str = "claude-haiku-4-5"
) -> dict:
    prompt = f"""Solve step by step. End with: Answer: <value>\n\nProblem: {problem}"""

    with ThreadPoolExecutor(max_workers=n_samples) as ex:
        futures = [ex.submit(single_sample, prompt, model, temperature)
                   for _ in range(n_samples)]
        samples = [f.result() for f in futures]

    answers = [extract_answer(s) for s in samples]
    vote_counts = Counter(answers)
    winner, votes = vote_counts.most_common(1)[0]
    confidence = votes / n_samples

    return {
        'answer': winner,
        'confidence': confidence,
        'votes': dict(vote_counts),
        'samples': samples
    }

# Usage
result = self_consistency(
    "If a rectangle has perimeter 40 and width 8, what is its area?",
    n_samples=7,
    temperature=0.8
)
print(f"Answer: {result['answer']} (confidence: {result['confidence']:.0%})")
# Expected: 96 (length=12, area=12*8=96)
```

## Graduation Criteria

- [ ] Benchmark against greedy on ≥3 task types documented
- [ ] Open-ended output clustering strategy proposed
- [ ] Cost/accuracy curve plotted for N=1..10 samples
