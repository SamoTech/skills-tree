# Spatial Reasoning
Category: reasoning | Level: intermediate | Stability: stable | Version: v1

## Description
Reason about positions, directions, distances, and spatial relationships in 2D and 3D environments.

## Example
```python
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=512,
    messages=[{"role": "user", "content": "A is north of B. C is east of A. D is south of C. Is D east of B? Think step by step."}]
)
print(response.content[0].text)
```

## Failure Modes
- Relative vs absolute directions confused
- 3D reasoning degrades without visual grounding

## Related
- `analogical.md` · `mathematical-reasoning.md`

## Changelog
- v1 (2026-04): Initial entry
