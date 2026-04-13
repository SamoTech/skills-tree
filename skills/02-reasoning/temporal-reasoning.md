![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-temporal-reasoning.json)

# Temporal Reasoning
Category: reasoning | Level: intermediate | Stability: stable | Version: v1

## Description
Reason about time relationships: before/after, duration, frequency, deadlines, and sequence ordering.

## Example
```python
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=512,
    messages=[{"role": "user", "content": "Project A ends on May 10. Project B must start 2 weeks after A ends and lasts 3 weeks. What is B's end date?"}]
)
print(response.content[0].text)  # May 31
```

## Failure Modes
- Ambiguous 'next Monday' (this week or next?)
- Timezone mismatches in multi-region deadlines

## Related
- `planning.md` · `causal.md`

## Changelog
- v1 (2026-04): Initial entry
