---
title: "Video Script"
category: 13-creative
level: advanced
stability: stable
version: v2
added: "2025-03"
description: "Create timed video scripts with hooks, narration, on-screen text, visual cues, and calls to action while keeping factual claims traceable to the source brief."

related: [blog-writing, presentation-gen, social-media-post]---

# Video Script

## Description

Convert a source brief into a production-oriented script. The script should expose timing, narration, visual direction, and on-screen text so downstream editing tools or humans can execute it.

## Inputs / Outputs

| Item | Type | Required | Notes |
|---|---|---:|---|
| Topic/source brief | str | yes | Canonical factual input |
| Duration | int | yes | Target seconds |
| Audience | str | yes | Intended viewer |
| Scenes | list[dict] | yes | Timed production units |
| Claims | list[str] | recommended | Claims requiring source traceability |

## Runnable Example

```python
from dataclasses import dataclass

@dataclass
class Scene:
    start: int
    end: int
    narration: str
    visual: str
    on_screen: str

def build_script(topic: str, duration: int = 60) -> list[Scene]:
    first = min(5, duration)
    return [
        Scene(0, first, f"Here is the core question: {topic}.", "Opening title", topic),
        Scene(first, duration, "Explain the topic using only the supplied source brief.", "Supporting footage or diagram", ""),
    ]

for scene in build_script("How retrieval grounds generation"):
    print(scene)
```

## Production Rules

- Use time ranges that sum to the intended duration.
- Keep narration separate from visual direction.
- Mark B-roll, screen captures, graphics, and on-screen text explicitly.
- Keep factual claims tied to the source brief.
- Do not manufacture testimonials, results, statistics, or urgency.
- Treat publishing as a separate authorization step.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Timing mismatch | Scene durations do not cover target runtime | Validate non-overlapping contiguous intervals |
| Unsupported claim | Script invents detail | Remove or source the claim |
| Editing ambiguity | Visual direction is vague | Specify asset type and purpose |
| Accidental publication | Generation coupled to publishing | Keep publishing outside the skill boundary |

## Evidence

This skill defines a production structure rather than claims about a particular video platform.

Evidence status: no performance, retention, or conversion claim is made.

## Related

- blog-writing
- presentation-gen
- social-media-post

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-03 | Initial entry |
| v2 | 2026-10 | Added timed scene contract, claim discipline, and deterministic example |
