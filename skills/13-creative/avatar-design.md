---
title: "Avatar Design"
category: 13-creative
level: advanced
stability: stable
description: "Apply avatar design in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-13-creative-avatar-design.json)

**Category:** Creative
**Skill Level:** Advanced
**Stability:** stable
**Added:** 2025-03

### Description
Creates detailed character design documents including appearance, personality, backstory, abilities, and visual design notes suitable for character sheets, games, fiction, or avatar generation prompts.

### Example
```python
import anthropic

client = anthropic.Anthropic()

prompt = """
Create a complete character design sheet for a sci-fi RPG character.
Output structured JSON with these keys:
- name, age, species, role
- appearance: {height, build, hair, eyes, distinguishing_features}
- personality: {traits: [], flaws: [], motivation}
- backstory: string (150 words)
- abilities: [{name, description, power_level}] (3 abilities)
- image_prompt: optimised DALL-E prompt to visualise this character
"""

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)
print(message.content[0].text)
```

### Related Skills
- [Creative Writing](creative-writing.md)
- [Image Generation (Prompt)](image-gen-prompt.md)
- [Persona Adoption](../06-communication/persona-adoption.md)
