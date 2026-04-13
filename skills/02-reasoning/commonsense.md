---
title: "Commonsense Reasoning"
category: 02-reasoning
level: basic
stability: stable
description: "Apply commonsense reasoning in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-commonsense.json)

# Commonsense Reasoning

**Category:** `reasoning`  
**Skill Level:** `basic`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Apply everyday background knowledge — physical laws, social norms, typical object properties, default assumptions about human intent — to fill in gaps that are never explicitly stated. Handles physical common sense (objects fall, fire burns), social common sense (politeness norms, turn-taking), temporal common sense (events have duration, order matters), and causal common sense (switching a lamp off makes it dark).

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `situation` | `string` | ✅ | Situation or text requiring implicit knowledge to interpret |
| `question` | `string` | ❌ | Specific question about the situation |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `inference` | `string` | Commonsense conclusion |
| `implicit_assumptions` | `list` | Unstated facts relied upon |
| `confidence` | `string` | `high` / `medium` / `low` |

---

## Example

```python
import anthropic
import json

client = anthropic.Anthropic()

def commonsense_inference(situation: str, question: str = "") -> dict:
    """
    Fill in implicit gaps in a situation using commonsense knowledge.
    """
    q_hint = f"\nQuestion: {question}" if question else ""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": (
                f"Situation:\n{situation}{q_hint}\n\n"
                "Apply commonsense reasoning and return JSON with:\n"
                "- inference: the commonsense conclusion\n"
                "- implicit_assumptions: list of unstated facts you relied on\n"
                "- knowledge_type: physical | social | temporal | causal | mixed\n"
                "- confidence: high | medium | low\n"
                "Return ONLY valid JSON."
            )
        }]
    )
    return json.loads(response.content[0].text)

result = commonsense_inference(
    situation="Maria left her umbrella at home this morning. She is walking back from the office.",
    question="What is Maria probably thinking about?"
)
print(json.dumps(result, indent=2))
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Claude claude-opus-4-5 | Direct prompt | 2024-06 |
| GPT-4o | Direct prompt | 2024-05 |
| LangGraph | Lightweight reasoning node | v0.1 |

---

## Notes

- Modern LLMs handle commonsense reasoning well for typical scenarios; accuracy drops for unusual edge cases
- Explicitly request `implicit_assumptions` to make reasoning transparent and auditable
- For safety-critical applications, verify commonsense inferences with factual grounding from [Fact Verification](../03-memory/fact-verification.md)

---

## Related Skills

- [Abductive Reasoning](abductive.md) — hypothesis generation
- [Causal Reasoning](causal.md) — cause-effect chains
- [Analogical Reasoning](analogical.md) — cross-domain mapping

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: full description, I/O table, umbrella example |
| `2025-03` | Initial stub entry |
