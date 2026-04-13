![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-trade-off-analysis.json)

# Trade-off Analysis
Category: reasoning | Level: intermediate | Stability: stable | Version: v1

## Description
Structurally compare options across multiple dimensions to surface the best choice given constraints.

## Example
```python
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Compare PostgreSQL vs MongoDB for a chat app with 10M messages/day. Dimensions: query flexibility, horizontal scale, operational complexity, cost. Recommend with reasoning."}]
)
print(response.content[0].text)
```

## Failure Modes
- Cherry-picking dimensions favoring preferred option
- Ignoring constraints (budget, team expertise)

## Related
- `decision-making.md` · `risk-assessment.md`

## Changelog
- v1 (2026-04): Initial entry
