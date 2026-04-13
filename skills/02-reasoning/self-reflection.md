![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-self-reflection.json)

# Self-Reflection
Category: reasoning | Level: intermediate | Stability: stable | Version: v1

## Description
Prompt an agent to critique its own previous output, identify errors, and produce an improved version.

## Example
```python
import anthropic
client = anthropic.Anthropic()
first = client.messages.create(model="claude-opus-4-5", max_tokens=512,
    messages=[{"role": "user", "content": "Summarize quantum entanglement in 3 sentences."}])
answer = first.content[0].text
reflect = client.messages.create(model="claude-opus-4-5", max_tokens=512,
    messages=[
        {"role": "user", "content": "Summarize quantum entanglement in 3 sentences."},
        {"role": "assistant", "content": answer},
        {"role": "user", "content": "Review your answer for accuracy and clarity. What would you improve? Then give the improved version."},
    ])
print(reflect.content[0].text)
```

## Failure Modes
- Model agrees with itself rather than critiquing
- Reflection loop runs indefinitely

## Related
- `chain-of-thought.md` · `debate.md` (09-agentic-patterns)

## Changelog
- v1 (2026-04): Initial entry
