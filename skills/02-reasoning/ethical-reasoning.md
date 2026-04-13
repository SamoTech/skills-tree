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
