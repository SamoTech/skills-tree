---
title: "Flashcard Creation"
category: 16-domain-specific
level: advanced
stability: stable
description: "Apply flashcard creation in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-flashcard-creation.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Converts dense study material into compact front/back flashcard pairs optimised for spaced-repetition review. Applies minimum-information principle, deduplication, and automatic difficulty tagging, then exports to Anki, Quizlet, or JSON.

### Example
```python
import anthropic, json

client = anthropic.Anthropic()

def make_flashcards(text: str, n: int = 5) -> list[dict]:
    prompt = (
        f"Create {n} flashcards from the text below. "
        "Return JSON array: [{front, back, difficulty: easy|medium|hard}].\n\n" + text
    )
    resp = client.messages.create(
        model="claude-opus-4-5", max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(resp.content[0].text)

cards = make_flashcards("TCP guarantees delivery via acknowledgements and retransmission.")
for c in cards:
    print(f"Q: {c['front']}  A: {c['back']}  ({c['difficulty']})")
```

### Related Skills
- [Quiz Generation](quiz-generation.md)
- [Summarization](../06-communication/summarization.md)
