---
title: "Paraphrasing"
category: 06-communication
level: basic
stability: stable
description: "Restate text in different words while preserving meaning. Used to simplify, vary, dedup near-duplicate corpora, or augment training data."
added: "2025-03"
version: v3
tags: [paraphrasing, rewriting, augmentation, simplification]
updated: "2026-04"
dependencies:
  - package: anthropic
    min_version: "0.39.0"
    tested_version: "0.39.0"
    confidence: verified
code_blocks:
  - id: "example-paraphrase"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-06-communication-paraphrasing.json)

# Paraphrasing

## Description

Rewrites a passage in different words while preserving its meaning. Common modes:

- **Simplify** — Reduce vocabulary level, shorter sentences.
- **Formalize / informalize** — Shift register without changing facts.
- **Diversify** — N independent rewrites for data augmentation or A/B test variants.
- **De-quote** — Rephrase a quote so it can be used without attribution liability.

## When to Use

- A summary or auto-generated answer reads exactly like training data and you want variation.
- Building dataset augmentation for a small classifier.
- Producing accessible / plain-language versions of dense text.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `text` | `str` | Source passage |
| `mode` | `Literal["simplify","formal","casual","diverse"]` | Style target |
| `n` | `int` | Number of variants when `mode="diverse"` |
| `preserve` | `list[str]` | Substrings that must appear verbatim |
| → `variants` | `list[str]` | One or more rewrites |

## Runnable Example

```python
# pip install anthropic
from __future__ import annotations
import json
import anthropic

client = anthropic.Anthropic()

SYSTEMS = {
    "simplify": "Rewrite for an 8th-grade reading level. Same facts, plainer words, shorter sentences.",
    "formal":   "Rewrite in a formal register suitable for business writing.",
    "casual":   "Rewrite in a casual, conversational tone.",
    "diverse":  "Produce {n} substantively different rewrites that all preserve the original meaning. Vary syntax and lexical choices.",
}

def paraphrase(text: str, mode: str = "simplify", n: int = 1,
               preserve: list[str] | None = None) -> list[str]:
    sys_prompt = SYSTEMS[mode].format(n=n)
    if preserve:
        sys_prompt += "\nThese substrings MUST appear unchanged: " + json.dumps(preserve)
    sys_prompt += "\nReply with a JSON list of strings."
    msg = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=sys_prompt,
        messages=[{"role": "user", "content": text}],
    )
    out = json.loads(msg.content[0].text)
    if not isinstance(out, list):
        raise ValueError("model did not return a JSON list")
    return out[:max(1, n)]

if __name__ == "__main__":
    src = ("Notwithstanding the foregoing, the licensor disclaims all warranties, "
           "whether express or implied, to the maximum extent permitted by applicable law.")
    print("Simplify:", paraphrase(src, mode="simplify"))
    print("Diverse :", paraphrase(src, mode="diverse", n=3))
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Meaning drift | Model adds or removes facts | Pair with an entailment check (NLI model) and reject non-entailed variants |
| Output identical to input | Source already optimal for chosen register | Detect via Jaccard similarity > 0.85 → retry with higher temperature |
| Lost named entities | Model rewrites proper nouns | Pass entities via `preserve=` |
| Style collapse on `diverse` | Low temperature | Sample with temperature ≥ 0.7 for `diverse` |
| Hallucinated citations | Model adds sources that weren't there | Strip or block bracketed references in post-processing |

## Frameworks & Models

| Framework | Implementation |
|---|---|
| Direct LLM | Any frontier chat API (above) |
| sentence-transformers + entailment | Verify meaning preservation locally |
| `pegasus-paraphrase` | Open-source seq2seq fallback |

## Model Comparison

| Capability | claude-opus-4-5 | gpt-4o | gemini-2.0-flash |
|---|---|---|---|
| Meaning preservation | 5 | 4 | 4 |
| Register control | 5 | 4 | 3 |
| Diversity at high `n` | 4 | 4 | 4 |
| Cost per variant | 3 | 4 | 5 |

## Related Skills

- [Translation](translation.md)
- [Tone Adjustment](tone-adjustment.md)
- [Summarize](summarization.md)
- [Multilingual Output](multilingual-output.md)

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial entry |
| 2026-04 | v3 | Modes, JSON output, preserve list, failure modes, model comparison |
