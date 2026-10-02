---
name: flashcard-creation
description: Convert supplied learning material into concise study cards while preserving source meaning, avoiding unsupported facts, and making difficulty or recall prompts explicit.
metadata:
  source: skills/16-domain-specific/flashcard-creation.md
  category: 16-domain-specific
---

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable

## Description
Convert supplied learning material into concise study cards while preserving source meaning, avoiding unsupported facts, and making difficulty or recall prompts explicit.

## When to Use
Use when source material is available and the task is to create reviewable question/answer units.

## Inputs / Outputs / Failure Modes
| Area | Contract |
|---|---|
| Inputs | Source material, domain context, task constraints, and required output format. |
| Outputs | Structured result with assumptions, uncertainty, provenance, or validation findings where material. |
| Failure modes | Missing context, stale/conflicting evidence, unsupported inference, malformed output, or skipped verification. |

## Procedure
1. Establish the task scope, source boundaries, and required output schema.
2. Validate that the supplied material is sufficient for the requested domain task.
3. Produce the result while preserving source meaning and distinguishing inference from evidence.
4. Validate calculations, citations, constraints, and required fields before downstream use.
5. Escalate material ambiguity or domain-specific uncertainty instead of inventing an answer.

## Runnable Example
```python
source = {"capability": "flashcard-creation", "validated": True}
assert source["validated"]
result = {"status": "review_required", "capability": source["capability"]}
print(result)
```

## Failure Modes
- Missing or ambiguous source context.
- Unsupported inference or domain-rule mismatch.
- Stale, conflicting, or unverifiable evidence.
- Treating generated output as authoritative professional advice.
- Skipping post-generation validation or provenance checks.

## Domain Boundary
Educational output is not a substitute for instructor assessment; verify terminology and source coverage.

## Evidence
The canonical skill file is the authoritative repository implementation. Repository schema, validation workflows, and the Agent Skills projection contract define structural conformance. Domain-specific factual claims must remain traceable to supplied or independently verified authoritative sources.

## Related
- 16-domain-specific
- input-guardrails
- output-guardrails
