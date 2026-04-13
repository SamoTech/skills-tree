![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-causal.json)

# Causal Reasoning

**Category:** `reasoning`  
**Skill Level:** `advanced`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Identify and reason about cause-and-effect relationships in text, data, or system descriptions. Distinguishes correlation from causation, builds causal chains, evaluates counterfactuals ("what if X hadn't happened?"), and identifies confounders. Applies to root-cause analysis, policy evaluation, experiment design, and business impact attribution.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `scenario` | `string` | ✅ | Description of the situation or event to analyze |
| `question` | `string` | ❌ | Specific causal question (default: general causal analysis) |
| `mode` | `string` | ❌ | `forward` (effects of cause) or `backward` (causes of effect) |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `causal_chain` | `list` | `[{step, cause, effect, mechanism}]` |
| `confounders` | `list` | Factors that complicate attribution |
| `counterfactual` | `string` | What would have happened without the root cause |
| `confidence` | `string` | `high` / `medium` / `low` |

---

## Example

```python
import anthropic
import json

client = anthropic.Anthropic()

def causal_analysis(scenario: str, question: str = "") -> dict:
    """
    Analyze causal relationships in a scenario.
    """
    q_hint = f"\nSpecific question: {question}" if question else ""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": (
                f"Scenario:\n{scenario}{q_hint}\n\n"
                "Perform causal analysis and return JSON with:\n"
                "- causal_chain: [{step, cause, effect, mechanism}]\n"
                "- root_cause: string\n"
                "- confounders: list of complicating factors\n"
                "- counterfactual: what would have happened without the root cause\n"
                "- confidence: high | medium | low\n"
                "- prevention_recommendations: list of actions to prevent recurrence\n"
                "Return ONLY valid JSON."
            )
        }]
    )
    return json.loads(response.content[0].text)

result = causal_analysis(
    scenario=(
        "A web app's checkout conversion rate dropped 18% on Tuesday afternoon. "
        "A UI library was upgraded that morning. Load times on the checkout page "
        "increased by 1.2s. No backend errors were logged."
    ),
    question="What caused the conversion drop?"
)
print(json.dumps(result, indent=2))
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Claude claude-opus-4-5 | Extended thinking for deep causal chains | 2025-01 |
| GPT-4o | Chain-of-thought prompt | 2024-05 |
| LangGraph | Multi-step causal graph node | v0.1 |

---

## Notes

- Enable extended thinking for complex multi-variable chains
- Provide a timeline or sequence of events when available
- Always request confounders — models tend to over-attribute causation without explicit prompting

---

## Related Skills

- [Abductive Reasoning](abductive.md) — hypothesis inference from incomplete observations
- [Analogical Reasoning](analogical.md) — cross-domain solution transfer
- [Commonsense Reasoning](commonsense.md) — everyday causal knowledge

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: full description, I/O table, conversion-drop case study |
| `2025-03` | Initial stub entry |
