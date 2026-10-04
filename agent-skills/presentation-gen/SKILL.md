---
name: presentation-gen
description: Generate structured presentation plans with slide purpose, evidence-backed content, speaker notes, and visual direction while keeping claims traceable to supplied source material.
metadata:
  source: skills/13-creative/presentation-gen.md
  category: 13-creative
  version: "v2"
---

# Presentation Generation

## Description

Turn a topic or source pack into a slide-by-slide presentation specification. The output should separate factual claims from interpretation and should identify which source supports important claims.

## Inputs / Outputs

| Item | Type | Required | Notes |
|---|---|---:|---|
| Topic | str | yes | Presentation subject |
| Audience | str | yes | Technical level and context |
| Slide count | int | yes | Desired maximum |
| Source material | list[dict] | recommended | Evidence for factual claims |
| Output | list[dict] | yes | Slide title, purpose, content, notes, visual direction |

## Runnable Example

```python
from dataclasses import dataclass

@dataclass
class Slide:
    number: int
    title: str
    purpose: str
    bullets: list[str]
    visual: str

def build_outline(topic: str, slides: int = 5) -> list[Slide]:
    titles = [
        "Problem",
        "Context",
        "Approach",
        "Evidence",
        "Decision / Next Step",
    ]
    return [
        Slide(i + 1, title, f"Explain {title.lower()} for {topic}", [], "Choose a visual that supports the slide claim")
        for i, title in enumerate(titles[:slides])
    ]

for slide in build_outline("RAG architecture"):
    print(slide.number, slide.title)
```

## Quality Rules

- One primary purpose per slide.
- Keep factual claims traceable to supplied evidence.
- Do not invent metrics, customer results, or benchmark outcomes.
- Speaker notes may contain detail omitted from the slide, but must not contradict it.
- Visual suggestions should communicate structure or evidence, not merely decorate the slide.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Unsupported claim | Model fills missing evidence | Mark claim as unsupported or request a source |
| Overloaded slide | Too many ideas | Enforce one primary purpose |
| Narrative drift | Slides do not build on each other | Validate outline order against audience objective |
| Decorative visuals | Visuals do not explain content | Require a stated visual purpose |

## Evidence

This skill describes a generation workflow rather than a factual claim about a specific presentation library. Implementation examples use only Python standard-library constructs.

Evidence status: no performance or engagement claim is made.

## Related

- blog-writing
- structured-output
- svg-generation

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-03 | Initial entry |
| v2 | 2026-10 | Added typed output contract, evidence discipline, and deterministic example |
