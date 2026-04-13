---
title: "Numerical Estimation"
category: 02-reasoning
level: intermediate
stability: stable
description: "Apply numerical estimation in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-numerical-estimation.json)

# Numerical Estimation
Category: reasoning | Level: basic | Stability: stable | Version: v1

## Description
Estimate quantities using Fermi decomposition: break unknown into known sub-components and multiply.

## Example
```python
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=512,
    messages=[{"role": "user", "content": "Estimate the number of piano tuners in Chicago. Show your Fermi estimation steps."}]
)
print(response.content[0].text)
```

## Failure Modes
- Errors compound multiplicatively across steps
- Anchoring bias on initial estimates

## Related
- `mathematical-reasoning.md` · `commonsense.md`

## Changelog
- v1 (2026-04): Initial entry
