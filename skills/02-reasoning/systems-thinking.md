# Systems Thinking
Category: reasoning | Level: advanced | Stability: stable | Version: v1

## Description
Identify feedback loops, leverage points, and emergent properties in complex systems.

## Example
```python
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Map the feedback loops in a SaaS business where: more users → more revenue → more R&D → better product → more users. Identify balancing and reinforcing loops."}]
)
print(response.content[0].text)
```

## Failure Modes
- Ignoring time delays in feedback loops
- Confusing correlation with causal links

## Related
- `causal.md` · `planning.md`

## Changelog
- v1 (2026-04): Initial entry
