---
name: video-frame-extraction
description: Extract representative or task-specific video frames using bounded sampling and preserve exact timestamps and source provenance. Use explicit evidence boundaries, bounded execution, and postcondition verification.
---

# Video Frame Extraction

## Description

Extract representative or task-specific video frames using bounded sampling and preserve exact timestamps and source provenance.

## When to Use

Use when the input modality and acceptance criteria are explicit and the workflow can verify its output.

## Inputs / Outputs

- Inputs: validated multimodal input, task constraints, and evidence boundary.
- Outputs: structured result or artifact with provenance, confidence, and unresolved uncertainty where material.

## Procedure

1. Validate modality, scope, and constraints.
2. Establish preprocessing or sampling bounds.
3. Execute within an explicit resource budget.
4. Preserve provenance and distinguish observation from inference.
5. Verify the output against the declared criteria.
6. Report uncertainty and incomplete coverage.

## Failure Modes

- Unsupported or corrupted input.
- Relevant evidence lost during preprocessing or sampling.
- Model confidence treated as proof.
- Sensitive media exposed outside authorization.
- Unverified or irreproducible output.

## Runnable Example

```python
task = {"capability": "video-frame-extraction", "validated": True, "budget": 4}
assert task["validated"] and task["budget"] > 0
print({"status": "bounded_execution", "capability": task["capability"]})
```

## Evidence

Canonical repository skill: skills/08-multimodal/video-frame-extraction.md. Repository schema, validation workflows, Agent Skills contract, and security gates define local conformance. Modality-specific claims require reproducible implementation evidence or authoritative primary documentation.

## Related

- 08-multimodal
- input-guardrails
- output-guardrails
