---
title: "Systems Thinking"
category: 02-reasoning
level: intermediate
stability: stable
description: "Apply systems thinking in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-systems-thinking.json)

# Systems Thinking
Category: reasoning | Level: advanced | Stability: stable | Version: v1

## Description
Identify feedback loops, leverage points, and emergent properties in complex systems.

## Example
```python
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Map the feedback loops in a SaaS business where: more users → more revenue → more R&D → better product → more users. Identify balancing and reinforcing loops."}]
)
print(response.content[0].text)
```

## Failure Modes
- Ignoring time delays in feedback loops
- Confusing correlation with causal links

## Related
- `causal.md` · `planning.md`

## Changelog
- v1 (2026-04): Initial entry
