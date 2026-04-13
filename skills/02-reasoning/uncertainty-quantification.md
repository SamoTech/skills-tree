# Uncertainty Quantification
Category: reasoning | Level: advanced | Stability: stable | Version: v1

## Description
Express confidence levels in claims using explicit probability estimates, confidence intervals, or verbal hedges.

## Example
```python
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=512,
    messages=[{"role": "user", "content": "What is the probability that AGI will be achieved by 2030? Give a calibrated estimate with reasoning and confidence interval."}]
)
print(response.content[0].text)
```

## Failure Modes
- Overconfidence (99% on hard empirical questions)
- Refusing to estimate when asked

## Related
- `bayesian-reasoning.md` · `numerical-estimation.md`

## Changelog
- v1 (2026-04): Initial entry
