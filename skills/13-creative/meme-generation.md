---
title: "Meme Generation"
category: 13-creative
level: advanced
stability: stable
description: "Apply meme generation in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-13-creative-meme-generation.json)

**Category:** Creative
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2025-03

### Description
Generates culturally resonant meme concepts by matching a topic to a suitable template, writing caption text, and optionally producing an image prompt. Requires awareness of current meme formats and internet culture subtext.

### Example
```python
import anthropic, json

client = anthropic.Anthropic()

def generate_meme(topic: str, tone: str = "sarcastic") -> dict:
    resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=300,
        messages=[{"role": "user", "content": (
            f"Generate a meme concept about '{topic}' with a {tone} tone.\n"
            "Return JSON: {template, top_text, bottom_text, image_gen_prompt}"
        )}]
    )
    return json.loads(resp.content[0].text)

print(generate_meme("deploying on Friday"))
```

### Related Skills
- [Creative Writing](creative-writing.md)
- [Image Generation Prompt](image-gen-prompt.md)
