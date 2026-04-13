![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-essay-grading.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Scores student essays against a multi-criteria rubric covering thesis strength, evidence quality, argument coherence, structure, and mechanics. Returns numeric scores per dimension plus actionable feedback comments and an overall grade.

### Example
```python
import anthropic, json

client = anthropic.Anthropic()

RUBRIC = {"thesis": 5, "evidence": 5, "coherence": 5, "structure": 5, "mechanics": 5}

def grade_essay(essay: str) -> dict:
    prompt = (
        "Grade this essay on the rubric: thesis (0-5), evidence (0-5), coherence (0-5), "
        "structure (0-5), mechanics (0-5). Return JSON: {scores, total, feedback}.\n\n" + essay
    )
    resp = client.messages.create(
        model="claude-opus-4-5", max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(resp.content[0].text)

print(grade_essay("Renewable energy is crucial because fossil fuels are depleting..."))
```

### Related Skills
- [Lesson Plan Writing](lesson-plan.md)
- [Report Writing](../06-communication/report-writing.md)
- [Argument Construction](../06-communication/argument-construction.md)
