---
title: "Creative Writing"
category: 13-creative
level: advanced
stability: stable
description: "Apply creative writing in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-13-creative-creative-writing.json)

**Category:** Creative
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2025-03

### Description
Generates original fiction, poetry, screenplays, and experimental prose with strong narrative structure, voice, and stylistic intentionality. Handles character development, plot arcs, and genre constraints.

### Example
```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=800,
    messages=[{"role": "user", "content": (
        "Write the opening scene (300 words) of a near-future thriller where "
        "an AI agent discovers it is being used to manipulate elections. "
        "Write in close third-person, present tense."
    )}]
)
print(message.content[0].text)
```

### Related Skills
- [Copywriting](copywriting.md)
- [Persona Adoption](../06-communication/persona-adoption.md)
- [Tone Adjustment](../06-communication/tone-adjustment.md)
