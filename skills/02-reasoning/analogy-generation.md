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
