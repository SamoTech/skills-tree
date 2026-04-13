---
title: "Lesson Plan"
category: 16-domain-specific
level: advanced
stability: stable
description: "Apply lesson plan in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-lesson-plan.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Generates structured lesson plans with learning objectives, pacing, activities, materials, differentiation strategies, and formative assessments aligned to a specified curriculum standard. Supports K-12, higher education, and professional training contexts.

### Example
```python
import anthropic

client = anthropic.Anthropic()

def create_lesson_plan(topic: str, grade: str, duration_min: int) -> str:
    prompt = (
        f"Create a {duration_min}-minute lesson plan for {grade} on '{topic}'.\n"
        "Include: Learning Objectives, Warm-up (5 min), Instruction, Guided Practice, "
        "Independent Practice, Closure, Assessment method, and Materials."
    )
    resp = client.messages.create(
        model="claude-opus-4-5", max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.content[0].text

print(create_lesson_plan("Introduction to Fractions", "Grade 4", 45))
```

### Related Skills
- [Quiz Generation](quiz-generation.md)
- [Essay Grading](essay-grading.md)
- [Planning](../02-reasoning/planning.md)
