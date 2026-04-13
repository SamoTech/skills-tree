![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-hypothesis-generation.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Generates testable scientific or product hypotheses from observations, experimental data, or literature gaps. Frames each hypothesis with a falsifiability criterion, suggested experiment design, and expected outcome.

### Example
```python
import anthropic, json

client = anthropic.Anthropic()

def generate_hypotheses(observations: list[str], domain: str, n: int = 3) -> list[dict]:
    obs_text = "\n".join(f"- {o}" for o in observations)
    prompt = (
        f"Given these observations in {domain}, generate {n} testable hypotheses.\n"
        "Return JSON array: [{hypothesis, falsifiability_test, expected_outcome, confidence}].\n\n"
        + obs_text
    )
    resp = client.messages.create(
        model="claude-opus-4-5", max_tokens=900,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(resp.content[0].text)

obs = ["Conversion rose 22% after reducing checkout fields from 8 to 3",
       "Mobile bounce rate dropped when form was split into steps"]
print(generate_hypotheses(obs, "UX research"))
```

### Related Skills
- [Literature Review](literature-review.md)
- [Inductive Reasoning](../02-reasoning/inductive-reasoning.md)
