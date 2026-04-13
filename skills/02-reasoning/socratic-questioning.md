![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-socratic-questioning.json)

# Socratic Questioning
Category: reasoning | Level: intermediate | Stability: stable | Version: v1

## Description
Drive deeper understanding by generating clarifying questions that expose assumptions and hidden complexity.

## Example
```python
import anthropic
client = anthropic.Anthropic()
statement = "We should use microservices for our new app."
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=512,
    messages=[{"role": "user", "content": f"Generate 5 Socratic questions to test the assumptions behind: '{statement}'"}]
)
print(response.content[0].text)
```

## Failure Modes
- Questions too abstract to drive action
- Exhausting the user with too many questions

## Related
- `self-reflection.md` · `causal.md`

## Changelog
- v1 (2026-04): Initial entry
