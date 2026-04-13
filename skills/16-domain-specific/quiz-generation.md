---
title: "Quiz Generation"
category: 16-domain-specific
level: advanced
stability: stable
description: "Apply quiz generation in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-quiz-generation.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Generates multi-format assessments (MCQ, true/false, short-answer, fill-in-the-blank) from source material with calibrated difficulty, plausible distractors, and answer explanations. Supports Bloom's taxonomy alignment and export to quiz platforms.

### Example
```python
import anthropic, json

client = anthropic.Anthropic()

def generate_quiz(text: str, n: int = 3) -> list[dict]:
    prompt = (
        f"Generate {n} multiple-choice questions from this text. "
        "Return JSON array, each item: {question, options: [A,B,C,D], answer, explanation}.\n\n" + text
    )
    resp = client.messages.create(
        model="claude-opus-4-5", max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(resp.content[0].text)

content = "The mitochondria produce ATP through oxidative phosphorylation."
for q in generate_quiz(content):
    print(q["question"], "->", q["answer"])
```

### Related Skills
- [Lesson Plan Writing](lesson-plan.md)
- [Flashcard Creation](flashcard-creation.md)
- [Structured Output](../06-communication/structured-output.md)
