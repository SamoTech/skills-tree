---
title: "Logo Design"
category: 13-creative
level: advanced
stability: stable
description: "Apply logo design in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-13-creative-logo-design.json)

**Category:** Creative
**Skill Level:** Advanced
**Stability:** stable
**Added:** 2025-03

### Description
Designs brand logos as production-ready SVG code. Applies brand design principles: geometric abstraction, scalability from 16px favicon to billboard, monochrome-first approach with optional colour variants, and `currentColor` for theme adaptability.

### Example
```python
import anthropic

client = anthropic.Anthropic()

prompt = """
Design an SVG logo for 'Orbit Analytics' — a data analytics SaaS.
Requirements:
- viewBox="0 0 200 60"
- Wordmark + icon mark side by side
- Icon: abstract orbital ring around a data point
- Font equivalent via SVG path for 'Orbit' text (or use <text> with Google Font)
- Colors: #0066FF primary, #001A3D dark background variant
- Include a <title> element for accessibility
Output ONLY the SVG.
"""

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=2048,
    messages=[{"role": "user", "content": prompt}]
)
print(message.content[0].text)
```

### Related Skills
- [SVG/Vector Art Generation](svg-generation.md)
- [Avatar/Character Design](avatar-design.md)
- [Image Generation (Prompt)](image-gen-prompt.md)
