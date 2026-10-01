---
name: lesson-plan
description: Generate structured lesson plans from explicit learning objectives and instructional constraints.
---

# lesson plan

## Description
Generate structured lesson plans from explicit learning objectives and instructional constraints.

## Evidence
Canonical source: `skills/16-domain-specific/lesson-plan.md`. Structural conformance is enforced by the repository skill schema, Agent Skills validator, security gates, and CI quality checks.

## Usage
Use only when task scope and source material are established. Preserve provenance and state uncertainty when evidence is incomplete.

## Failure modes
- Missing or ambiguous source context.
- Unsupported domain inference.
- Stale or conflicting evidence.
- Treating generated output as authoritative professional advice.
- Skipping validation or source verification.

## Related
- `16-domain-specific`
- `input-guardrails`
- `output-guardrails`
