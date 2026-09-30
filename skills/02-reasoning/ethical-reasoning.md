---
title: "Ethical Reasoning"
category: 02-reasoning
level: intermediate
stability: stable
version: v2
description: "Analyze decisions across explicit ethical frameworks and stakeholder impacts without presenting a framework-dependent judgment as objective fact."
added: "2025-03"
related: []
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-ethical-reasoning.json)

# Ethical Reasoning
Category: reasoning | Level: advanced | Stability: stable | Version: v1

## Description
Evaluate actions and decisions against ethical frameworks (utilitarian, deontological, virtue ethics) and stakeholder impacts.

## Example
```python
import anthropic
client = anthropic.Anthropic()
dilemma = "An AI system can reduce hospital costs by 20% but will eliminate 15% of admin jobs."
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": f"Analyze this using utilitarian, deontological, and virtue ethics frameworks: {dilemma}"}]
)
print(response.content[0].text)
```

## Failure Modes
- Framework selection bias
- Missing affected stakeholder groups

## Related
- `decision-making.md` · `causal.md`

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

- Unsupported assumptions: state assumptions explicitly and separate them from observed inputs.
- Ambiguous or incomplete premises: return uncertainty rather than fabricating missing constraints.
- Resource explosion: bound candidate counts, iterations, recursion, and external tool calls.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
