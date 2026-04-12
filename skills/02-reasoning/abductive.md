# Abductive Reasoning

**Category:** `reasoning`  
**Skill Level:** `advanced`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Infer the most plausible explanation for an incomplete set of observations — the logical "inference to the best explanation." Given partial evidence (symptoms, logs, user complaints, sensor spikes), the agent generates ranked hypotheses ordered by likelihood, identifies what evidence supports each, and suggests what additional data would confirm or rule out each candidate. Useful for root-cause analysis, medical triage, debugging, and scientific hypothesis generation.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `observations` | `list` | ✅ | List of observed facts or symptoms |
| `domain` | `string` | ❌ | Domain hint: `medical`, `software`, `mechanical`, etc. |
| `top_n` | `int` | ❌ | Number of hypotheses to return (default: 3) |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `hypotheses` | `list` | `[{hypothesis, plausibility, supporting_evidence, falsification_test}]` |
| `best_explanation` | `string` | Top-ranked hypothesis |
| `confidence` | `string` | `high` / `medium` / `low` |

---

## Example

```python
import anthropic
import json

client = anthropic.Anthropic()

def abductive_analysis(observations: list[str], domain: str = "") -> dict:
    """
    Return ranked hypotheses explaining the given observations.
    observations: list of factual observations (e.g. error messages, symptoms)
    """
    obs_text = "\n".join(f"- {o}" for o in observations)
    domain_hint = f"Domain context: {domain}\n" if domain else ""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": (
                f"{domain_hint}"
                "Observations:\n"
                f"{obs_text}\n\n"
                "Using abductive reasoning, return JSON with:\n"
                "- hypotheses: top 3 [{hypothesis, plausibility (0-1), "
                "supporting_evidence (list), falsification_test}]\n"
                "- best_explanation: string\n"
                "- confidence: high | medium | low\n"
                "- missing_evidence: what additional data would help\n"
                "Return ONLY valid JSON."
            )
        }]
    )
    return json.loads(response.content[0].text)

result = abductive_analysis(
    observations=[
        "Server CPU spiked to 100% at 03:17 UTC",
        "Database slow query log shows 450ms average at the same time",
        "No deployments in the past 24 hours",
        "Traffic was 30% below normal"
    ],
    domain="software infrastructure"
)
print(json.dumps(result, indent=2))
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Claude claude-opus-4-5 | Extended thinking + direct prompt | 2025-01 |
| GPT-4o | Chain-of-thought prompt | 2024-05 |
| LangGraph | Multi-step hypothesis graph node | v0.1 |

---

## Notes

- Enable extended thinking for complex multi-variable observations
- Frame observations as factual statements, not already-interpreted conclusions
- For software debugging, attach relevant log snippets to the observations list

---

## Related Skills

- [Causal Reasoning](causal.md) — determining cause-effect chains
- [Commonsense Reasoning](commonsense.md) — background world knowledge
- [Fact Verification](../03-memory/fact-verification.md) — checking hypothesis claims

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: full description, I/O table, root-cause analysis example |
| `2025-03` | Initial stub entry |
