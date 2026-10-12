---
name: plain-language-writing
description: Rewrite technical statements so a busy reader needs no extra context — short sentences, concrete nouns, active verbs, and no jargon left undefined.
metadata:
  source: skills/06-communication/plain-language-writing.md
  category: 06-communication
  version: "v1"
---

# Plain Language Writing

Category: Communication | Level: basic | Stability: experimental | Version: v1

## Description

Plain language is not simplified thinking; it is text that survives first contact with a reader who has no reason to reread it. This skill works mostly by subtraction: state the point in one sentence, prefer words the reader already owns, split sentences that carry more than one idea, and cut hedges until a claim stands alone. Terms of art survive only when they are load-bearing, and then they are defined on first use.

## When to Use

Use for mixed or non-specialist audiences — documentation, summaries, status updates, user-facing messages — wherever the reader cannot be assumed to share the vocabulary of the author.

Do not strip precision that the audience needs; plain language is calibrated to its readers, and for a specialist audience the shared vocabulary is part of the clarity, not an obstacle to it.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `draft` | `text` | Yes | The passage to rewrite |
| `audience` | `string` | Yes | Who will read it and what they already know |
| `purpose` | `string` | Yes | The single takeaway or action the reader should leave with |

## Procedure

1. Write the point in one sentence before touching the draft; if that sentence does not exist, the passage has no spine yet.
2. Replace each term of art with plain wording, or keep it and define it on first use when the term is load-bearing.
3. Split any sentence that carries more than one idea, and put the actor before the verb in each half.
4. Cut throat-clearing openings and stacked hedges; say the claim once and let it stand.
5. Pair every number with a reference point, because bare figures force the reader to supply the missing scale.
6. Reread as the target reader, and delete anything that survives only to comfort the author.

## Outputs

| Output | Type | Description |
|---|---|---|
| `rewrite` | `text` | The plain-language version of the passage |
| `terms` | `list` | Kept terms of art, each with its plain definition |

## Runnable Example

```python
import re

JARGON = {
    "serialize": "convert into a storable form",
    "idempotent": "safe to run more than once",
}

def plainify(sentence):
    for term, meaning in JARGON.items():
        pattern = r"\b" + term + r"\b"
        sentence = re.sub(pattern, f"{term} ({meaning})", sentence)
    return sentence

draft = "The worker runs a serialize step, so a retry stays idempotent."
print(plainify(draft))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Simplified into vagueness | Plain wording dropped load-bearing precision | Keep the technical term and define it inline |
| Audience mismatch | Text calibrated to the wrong prior knowledge | Fix the audience statement before rewriting |
| Hedge fog | Qualifiers stacked until nothing is asserted | State the claim once, plainly |
| Sentence sprawl | One sentence carrying three ideas | Split at idea boundaries |
| Naked numbers | Figures with no comparison given | Attach a reference point to every number |

## Security and Authority Boundary

Plain text travels: writing for a broad audience multiplies the chance a passage is quoted out of context, so a rewrite must not widen disclosure — anything sensitive stays in documents scoped to the audience that may see it, and the plain version inherits the classification of its source.

## Evidence

This skill is grounded in dated public implementation references:

1. The PlainLanguage.gov guidelines (https://www.plainlanguage.gov/guidelines/).
2. Wikipedia's overview of plain language (https://en.wikipedia.org/wiki/Plain_language).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Paraphrasing](paraphrasing.md) — restating existing material at a chosen register.
- [Summarization](summarization.md) — compressing a source while keeping its claims.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
