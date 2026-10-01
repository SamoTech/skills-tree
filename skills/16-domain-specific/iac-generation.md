---
title: "Iac Generation"
category: 16-domain-specific
level: advanced
stability: stable
description: "Draft Infrastructure as Code from a declared infrastructure specification, with explicit assumptions, review points, and deployment-safety boundaries."
added: "2025-03"
related: ["16-domain-specific", "input-guardrails", "output-guardrails"]
---

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable

## Description
Draft Infrastructure as Code from a declared infrastructure specification, with explicit assumptions, review points, and deployment-safety boundaries.

## When to Use
Use when the target platform, resources, environment, and operational constraints are known.

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
source = {"capability": "iac-generation", "validated": True}
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
Generated IaC must be reviewed, validated, and planned in the target environment before deployment; never assume provider defaults are safe.

## Evidence
The canonical skill file is the authoritative repository implementation. Repository schema, validation workflows, and the Agent Skills projection contract define structural conformance. Domain-specific factual claims must remain traceable to supplied or independently verified authoritative sources.

## Related
- 16-domain-specific
- input-guardrails
- output-guardrails
