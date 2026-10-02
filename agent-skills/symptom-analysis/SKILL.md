---
name: symptom-analysis
description: Structure symptom information into questions, red-flag checks, and uncertainty-aware triage support without claiming a diagnosis.
metadata:
  source: skills/16-domain-specific/symptom-analysis.md
  category: 16-domain-specific
---

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable

## Description
Structure symptom information into questions, red-flag checks, and uncertainty-aware triage support without claiming a diagnosis.

## When to Use
Use only as an information-structuring aid when symptom details and relevant context are supplied.

## Inputs / Outputs / Failure Modes
| Area | Contract |
|---|---|
| Inputs | Source material, domain context, task constraints, and required output format. |
| Outputs | Structured result with provenance, assumptions, uncertainty, and validation findings where material. |
| Failure modes | Missing context, stale/conflicting evidence, unsupported inference, malformed output, or skipped verification. |

## Procedure
1. Establish task scope, source boundaries, and required output schema.
2. Validate that the source material and domain context are sufficient.
3. Produce the result while preserving source meaning and separating evidence from inference.
4. Validate calculations, claims, citations, constraints, and required fields.
5. Escalate material ambiguity instead of inventing missing facts.

## Runnable Example
```python
task = {"capability": "symptom-analysis", "validated": True}
assert task["validated"]
result = {"status": "review_required", "capability": task["capability"]}
print(result)
```

## Failure Modes
- Missing or ambiguous source context.
- Unsupported domain inference.
- Stale, conflicting, or unverifiable evidence.
- Presenting generated output as authoritative professional advice.
- Skipping validation or provenance checks.

## Domain Boundary
This is not diagnosis or medical advice; urgent red flags require appropriate professional or emergency evaluation.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Domain-specific factual claims must remain traceable to supplied or independently verified authoritative sources.

## Related
- 16-domain-specific
- input-guardrails
- output-guardrails
