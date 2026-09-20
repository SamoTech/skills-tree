---
title: "Argument Structure Analysis"
category: 02-reasoning
level: intermediate
stability: stable
description: "Decompose arguments into premises, conclusions, inference links, and explicit gaps so agents distinguish stated evidence from unsupported claims."
added: "2025-03"
version: v2
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-argument-structure-analysis.json)

# Argument Structure Analysis
Category: reasoning | Level: intermediate | Stability: stable | Version: v1

## Description
Identify premises, conclusions, and logical connectives in text; detect fallacies and weak inferences.

## Example
```python
import anthropic
client = anthropic.Anthropic()
text = "All mammals are warm-blooded. Whales are mammals. Therefore whales are warm-blooded."
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=512,
    messages=[{"role": "user", "content": f"Identify: premises, conclusion, argument type, any fallacies in:\n{text}"}]
)
print(response.content[0].text)
```

## Failure Modes
- Implied premises not surfaced
- Circular arguments hard to detect automatically

## Related
- `deductive-reasoning.md` · `inductive-reasoning.md`

## Changelog
- v1 (2026-04): Initial entry
