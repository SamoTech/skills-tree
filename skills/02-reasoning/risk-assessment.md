---
title: "Risk Assessment"
category: 02-reasoning
level: intermediate
stability: stable
description: "Apply risk assessment in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-risk-assessment.json)

# Risk Assessment
Category: reasoning | Level: intermediate | Stability: stable | Version: v1

## Description
Identify, quantify, and prioritize risks using probability × impact matrices.

## Example
```python
import anthropic, json
client = anthropic.Anthropic()
context = "Launching a new payment feature in 2 weeks with 3 engineers."
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": f"Identify top 5 risks for: {context}. Return JSON: [{{risk, probability, impact, mitigation}}]"}]
)
risks = json.loads(response.content[0].text)
for r in sorted(risks, key=lambda x: x['probability']*x['impact'], reverse=True):
    print(f"[{r['probability']*r['impact']:.2f}] {r['risk']}: {r['mitigation']}")
```

## Failure Modes
- Unknown unknowns not surfaced
- Correlation between risks ignored

## Related
- `decision-making.md` · `planning.md`

## Changelog
- v1 (2026-04): Initial entry
