# Fact Verification

**Category:** `memory`  
**Skill Level:** `advanced`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Verify factual claims against authoritative sources, retrieved context, or tool-accessible knowledge. Classifies each claim as `verified`, `unverified`, `contradicted`, or `uncertain`, and provides a citation or counter-evidence. Applies to hallucination detection in generated text, claim-checking user inputs, and research QA pipelines.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `claims` | `list` | ✅ | List of factual statements to verify |
| `context` | `string` | ❌ | Reference text to verify against (if available) |
| `tool_use` | `bool` | ❌ | Allow web search for verification (default: false) |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `results` | `list` | `[{claim, verdict, confidence, evidence, source}]` |
| `overall_reliability` | `string` | `high` / `medium` / `low` |
| `unverifiable_claims` | `list` | Claims that cannot be checked without external tools |

---

## Example

```python
import anthropic
import json

client = anthropic.Anthropic()

def verify_claims(claims: list[str], context: str = "") -> dict:
    """
    Verify a list of factual claims, optionally against a reference context.
    """
    claims_text = "\n".join(f"{i+1}. {c}" for i, c in enumerate(claims))
    ctx_block = f"\nReference context:\n{context}\n" if context else ""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": (
                f"Claims to verify:\n{claims_text}{ctx_block}\n"
                "For each claim return JSON with:\n"
                "- results: [{claim, verdict (verified|unverified|contradicted|uncertain), "
                "confidence (0-1), evidence, source}]\n"
                "- overall_reliability: high | medium | low\n"
                "- unverifiable_claims: list\n"
                "Return ONLY valid JSON."
            )
        }]
    )
    return json.loads(response.content[0].text)

result = verify_claims(
    claims=[
        "Python was created by Guido van Rossum",
        "Python 3.0 was released in 2005",
        "Python is the most popular language for data science"
    ]
)
print(json.dumps(result, indent=2))
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Claude claude-opus-4-5 | Direct prompt with context | 2024-06 |
| LangChain | `LLMCheckerChain` | v0.1 |
| LangGraph | Verification node in fact-check pipeline | v0.1 |

---

## Notes

- For real-time verification, attach a web search tool (Brave Search, Tavily) and set `tool_use: true`
- Model knowledge has a training cutoff — for recent events, always provide retrieved context
- Distinguish `unverified` (no evidence found) from `contradicted` (counter-evidence found)

---

## Related Skills

- [Memory Summarization](memory-summarization.md) — condensing verified knowledge
- [Procedural Memory](procedural.md) — verifying how-to knowledge
- [Abductive Reasoning](../02-reasoning/abductive.md) — hypothesis-based inference

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: full description, I/O table, claim-checker example |
| `2025-03` | Initial stub entry |
