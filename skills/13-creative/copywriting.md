---
title: "Copywriting"
category: 13-creative
level: advanced
stability: stable
description: "Apply copywriting in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-13-creative-copywriting.json)

**Category:** Creative
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2025-03

### Description
Crafts persuasive marketing copy for landing pages, email campaigns, ads, and sales collateral. Masters AIDA and PAS frameworks, audience tone matching, and conversion-optimised structure.

### Example
```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=512,
    messages=[{"role": "user", "content": (
        "Write a 100-word landing page hero section for an AI writing tool targeting busy founders. "
        "Use the PAS framework. End with a CTA button label."
    )}]
)
print(message.content[0].text)
```

### Related Skills
- [Blog Writing](blog-writing.md)
- [Ad Copy Generation](../16-domain-specific/ad-copy.md)
- [Tone Adjustment](../06-communication/tone-adjustment.md)
