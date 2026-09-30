---
title: "Analogy Generation"
category: 02-reasoning
level: intermediate
stability: stable
version: v2
description: "Generate structural analogies that map a source concept to a target concept while explicitly checking which relationships transfer and which do not."
added: "2025-03"
related: []
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-analogy-generation.json)

# Analogy Generation
Category: reasoning | Level: basic | Stability: stable | Version: v1

## Description
Create clear analogies to explain complex concepts by mapping structure from a familiar domain to an unfamiliar one.

## Example
```python
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=512,
    messages=[{"role": "user", "content": "Generate 3 analogies to explain transformer attention mechanisms to a 12-year-old."}]
)
print(response.content[0].text)
```

## Failure Modes
- False analogies that mislead more than clarify
- Over-stretching analogy beyond its valid mapping

## Related
- `analogical.md` · `commonsense.md`

## Changelog
- v1 (2026-04): Initial entry

## Failure Modes

- Unsupported assumptions: state assumptions explicitly and separate them from observed inputs.
- Ambiguous or incomplete premises: return uncertainty or request the missing constraint rather than fabricating one.
- Resource or search explosion: bound candidate counts, iterations, recursion, and external tool calls.

## Evidence

- https://agentskills.io/specification
- https://github.com/openai/openai-python

Evidence status: references support implementation guidance; no performance benchmark is claimed without reproducible benchmark evidence.

## Failure Modes

- False mapping: identify which relationships do not transfer.
- Missing context: state assumptions before generating an analogy.
- Overextension: stop when the analogy no longer explains the target concept.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
