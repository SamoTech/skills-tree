---
name: invoice-processing
description: Extract and validate structured invoice data from supplied source material.
---

# invoice processing

## Description
Extract and validate structured invoice data from supplied source material.

## Evidence
Canonical source: `skills/16-domain-specific/invoice-processing.md`. Structural conformance is enforced by the repository skill schema, Agent Skills validator, security gates, and CI quality checks.

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
