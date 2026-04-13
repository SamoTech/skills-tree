---
title: "Meta-Cognition"
category: 02-reasoning
level: intermediate
stability: stable
description: "Apply meta-cognition in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-meta-cognition.json)

# Meta-Cognition
Category: reasoning | Level: advanced | Stability: stable | Version: v1

## Description
Monitor and regulate the reasoning process itself — detect when the agent is stuck, hallucinating, or needs more information.

## Example
```python
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=512,
    messages=[{"role": "user", "content": "Before answering: assess your confidence level (0-100%), list what you know vs. what you'd need to verify, and flag any potential gaps. Then answer: What is the exact population of Cairo as of today?"}]
)
print(response.content[0].text)
```

## Failure Modes
- Overconfidence masking actual ignorance
- Excessive hedging slowing response time

## Related
- `self-reflection.md` · `uncertainty-quantification.md`

## Changelog
- v1 (2026-04): Initial entry
