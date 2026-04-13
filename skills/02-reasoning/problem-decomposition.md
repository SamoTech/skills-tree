# Problem Decomposition
Category: reasoning | Level: basic | Stability: stable | Version: v1

## Description
Break complex problems into smaller, independently solvable sub-problems using divide-and-conquer or issue tree approaches.

## Example
```python
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Decompose the problem 'reduce user churn by 20%' into a MECE issue tree with 3 levels."}]
)
print(response.content[0].text)
```

## Failure Modes
- Non-MECE decomposition leads to double-counting
- Sub-problems too fine-grained to be actionable

## Related
- `planning.md` · `goal-setting.md`

## Changelog
- v1 (2026-04): Initial entry
