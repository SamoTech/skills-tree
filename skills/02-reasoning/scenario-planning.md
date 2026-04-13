![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-scenario-planning.json)

# Scenario Planning
Category: reasoning | Level: advanced | Stability: stable | Version: v1

## Description
Generate and evaluate multiple plausible future scenarios to support robust decision-making under uncertainty.

## Example
```python
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Generate 3 distinct 2030 scenarios for the electric vehicle market (optimistic, base, pessimistic). For each: key assumptions, market share, implications for battery manufacturers."}]
)
print(response.content[0].text)
```

## Failure Modes
- Scenarios not truly distinct (variants of same outcome)
- Overconfidence in base case probability

## Related
- `counterfactual-reasoning.md` · `risk-assessment.md`

## Changelog
- v1 (2026-04): Initial entry
