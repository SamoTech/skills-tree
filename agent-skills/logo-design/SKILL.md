---
name: logo-design
description: Develop a logo concept and production specification emphasizing legibility, scalability, accessibility, and brand constraints.
metadata:
  source: skills/13-creative/logo-design.md
  category: 13-creative
---

## Description

Develop a logo concept and production specification emphasizing legibility, scalability, accessibility, and brand constraints.

## When to Use

Use when the creative brief, audience, deliverable, and acceptance criteria are explicit.

## Inputs / Outputs / Failure Modes

| Area | Contract |
|---|---|
| Inputs | brand brief, audience, usage sizes, visual constraints, and deliverable format. |
| Outputs | logo specification, variants, and validation checklist. |
| Failure modes | Ambiguous brief, unsupported factual claims, style/constraint drift, unauthorized source imitation, or output accepted without checking the requested structure. |

## Procedure

1. Parse the creative brief, audience, purpose, and protected constraints.
2. Establish originality, attribution, and source-use boundaries.
3. Generate within explicit length, format, and complexity limits.
4. Check structure, consistency, factual claims, and requested style constraints.
5. Preserve user-supplied facts and distinguish invention from source material.
6. Validate the final artifact against the brief before delivery.

## Runnable Example

```python
task = {"capability": "logo-design", "brief_validated": True, "budget": 4}
assert task["brief_validated"] and task["budget"] > 0
print({"status": "creative_contract_checked", "capability": task["capability"]})
```

## Failure Modes

- Creative brief is underspecified or internally inconsistent.
- Factual or product claims are invented.
- Output violates required structure or audience constraints.
- Existing copyrighted material is reproduced or imitated beyond authorized transformation.
- Personal likenesses or source images are used without authorization.
- Completion is reported without checking the deliverable contract.

## Safety Boundary

Creative generation does not authorize deceptive claims, unauthorized likenesses, private data, or reproduction of copyrighted material. Keep source attribution and user-provided assets within their declared permissions.

## Evidence

Canonical repository skill: this file. Structural conformance is governed by the repository schema, validation workflows, Agent Skills contract, and security gates. Creative output is an artifact, not evidence of factual claims.

## Related

- 13-creative
- input-guardrails
- output-guardrails
