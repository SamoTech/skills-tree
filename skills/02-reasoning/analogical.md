![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-analogical.json)

# Analogical Reasoning

**Category:** `reasoning`  
**Skill Level:** `advanced`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Transfer structure, patterns, and solutions from one domain to another by identifying structural parallels. Given a source scenario and a target problem, the agent maps corresponding elements, adapts the known solution, and explains where the analogy holds and where it breaks down. Supports creative problem-solving, technical explanation, concept teaching, and inter-domain innovation.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `target_problem` | `string` | ✅ | Problem to solve in the target domain |
| `source_domain` | `string` | ❌ | Known domain to draw the analogy from |
| `depth` | `string` | ❌ | `surface` (shared attributes) or `structural` (relations between relations) |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `analogy` | `string` | Proposed analogy |
| `mapping` | `list` | `[{source_element, target_element, rationale}]` |
| `adapted_solution` | `string` | Solution transferred from source to target |
| `limitations` | `list` | Ways the analogy breaks down |

---

## Example

```python
import anthropic
import json

client = anthropic.Anthropic()

def reason_by_analogy(target_problem: str, source_domain: str = "") -> dict:
    """
    Solve a problem by finding a structural analogy from another domain.
    """
    source_hint = f"Draw the analogy from: {source_domain}\n" if source_domain else ""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": (
                f"{source_hint}"
                f"Target problem: {target_problem}\n\n"
                "Use analogical reasoning to return JSON with:\n"
                "- analogy: one-sentence analogy statement\n"
                "- source_domain: domain used\n"
                "- mapping: [{source_element, target_element, rationale}]\n"
                "- adapted_solution: solution transferred to the target domain\n"
                "- limitations: list of ways the analogy breaks down\n"
                "Return ONLY valid JSON."
            )
        }]
    )
    return json.loads(response.content[0].text)

result = reason_by_analogy(
    target_problem="How should we design a rate-limiter for a public API?",
    source_domain="traffic management on highways"
)
print(json.dumps(result, indent=2))
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Claude claude-opus-4-5 | Direct prompt with explicit mapping request | 2024-06 |
| GPT-4o | Chain-of-thought prompt | 2024-05 |
| LangGraph | Reasoning node | v0.1 |

---

## Notes

- Specify a source domain when you want a particular lens; omit it to let the model choose
- Structural analogies (mapping relations) are more powerful than surface analogies (shared features)
- Always include the `limitations` field to surface where the analogy misleads

---

## Related Skills

- [Causal Reasoning](causal.md) — for cause-effect inference
- [Commonsense Reasoning](commonsense.md) — world knowledge supporting analogies
- [Abductive Reasoning](abductive.md) — hypothesis generation

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: full description, I/O table, API rate-limiter analogy example |
| `2025-03` | Initial stub entry |
