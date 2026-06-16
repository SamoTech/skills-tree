---
title: "Reasoning Under Uncertainty"
category: 02-reasoning
level: advanced
stability: evolving
description: "Reason and make decisions when information is incomplete, ambiguous, or contradictory. Combines confidence calibration, hedged reasoning, and explicit uncertainty representation to produce reliable agent decisions under incomplete knowledge."
added: "2025-06"
version: v2
tags: [reasoning, uncertainty, calibration, confidence]
updated: "2026-06"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-02-reasoning-reasoning-under-uncertainty.json)

# Reasoning Under Uncertainty

## Description

Reasoning Under Uncertainty (RuU) is the agent capability to:

1. **Explicitly represent uncertainty** — "I am 70% confident this is correct"
2. **Hedge conclusions appropriately** — distinguish facts from inferences from guesses
3. **Request clarification or additional evidence** when uncertainty is too high to proceed
4. **Commit to a best-estimate decision** even under incomplete information when action is required

This is distinct from Uncertainty Quantification (which measures statistical uncertainty in model outputs) — RuU is the reasoning *approach* an agent uses when facing incomplete knowledge.

Used in: Anthropic's extended thinking (uncertainty-driven budget allocation), GPT-4's calibrated confidence expressions, LangChain's agent fallback chains, and medical/legal reasoning agents where hedged outputs are required.

## When to Use

- The agent must act despite missing information (incomplete evidence).
- Downstream systems need to know confidence level (for human review routing).
- Multiple contradictory sources require explicit confidence weighting.
- **Don't use** for tasks with deterministic answers; hedge signals waste tokens.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `question` | `str` | Question or decision to reason about |
| `evidence` | `list[str]` | Available evidence items |
| `confidence_threshold` | `float` | Minimum confidence to proceed (default 0.7) |
| → `answer` | `str` | Best-estimate answer with hedges |
| → `confidence` | `float` | 0.0–1.0 confidence score |
| → `missing_info` | `list[str]` | What additional evidence would improve confidence |
| → `action` | `str` | proceed / clarify / escalate |

## Runnable Example

```python
import json
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-opus-4-5"

RUU_PROMPT = """You are reasoning about a question with incomplete evidence.
Explicitly state your confidence (0.0-1.0) and what additional info would help.
Output JSON: {"answer": str, "confidence": float, "reasoning": str, "missing_info": [str], "action": "proceed|clarify|escalate"}

Question: {question}
Evidence: {evidence}
Confidence threshold to proceed: {threshold}"""

def reason_under_uncertainty(
    question: str,
    evidence: list[str],
    confidence_threshold: float = 0.7
) -> dict:
    resp = client.messages.create(
        model=MODEL, max_tokens=1024,
        messages=[{"role": "user", "content": RUU_PROMPT.format(
            question=question,
            evidence="\n".join(f"- {e}" for e in evidence),
            threshold=confidence_threshold
        )}]
    )
    text = resp.content[0].text.strip()
    start = text.find("{")
    end = text.rfind("}") + 1
    return json.loads(text[start:end])

if __name__ == "__main__":
    result = reason_under_uncertainty(
        question="Was the API outage caused by the deployment at 14:00?",
        evidence=[
            "Deployment occurred at 14:00",
            "Error rate spiked at 14:02",
            "Another team reported network issues at 13:55",
            "Rollback at 14:15 restored 80% of traffic"
        ]
    )
    print(f"Answer: {result['answer']}")
    print(f"Confidence: {result['confidence']:.0%}")
    print(f"Action: {result['action']}")
    print(f"Missing info: {result['missing_info']}")
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Overconfidence (confidence=1.0 always) | Model calibration issue | Require explicit evidence citation for confidence |
| Refusal to act below threshold | Threshold too high | Tune threshold per risk tolerance |
| Confidence not propagated downstream | No structured output | Use JSON schema with `confidence` field |

## Production Applications

- **G02 Research Agent:** Classify research findings by evidence strength before synthesis
- **G01 Coding Agent:** Hedge before modifying unfamiliar codebases; request context when uncertain
- **G04 RAG Assistant:** Score retrieved chunks by relevance confidence before including

## Related Skills

- [Self-Consistency](self-consistency.md) — uses voting to reduce uncertainty in answers
- [Hypothesis Generation](hypothesis-generation.md) — generates candidate explanations for uncertain situations
- [Reflection Pattern](../09-agentic-patterns/reflection-pattern.md) — re-evaluates low-confidence outputs
- [RAG Retrieval](../03-memory/rag-retrieval.md) — retrieves evidence to reduce uncertainty

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-06 | v1 | Initial skill file |
| 2026-06 | v2 | Full runnable example, structured output, action routing |
