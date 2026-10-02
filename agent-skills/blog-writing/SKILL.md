---
name: blog-writing
description: Produce a structured blog article that matches the requested audience, purpose, length, voice, and factual boundaries.
metadata:
  source: skills/13-creative/blog-writing.md
  category: 13-creative
---

## Description

Produce a structured blog article that matches the requested audience, purpose, length, voice, and factual boundaries.

## When to Use

Use when the creative brief, audience, deliverable, and acceptance criteria are explicit.

## Inputs / Outputs / Failure Modes

| Area | Contract |
|---|---|
| Inputs | topic, audience, outline, source material, length, and style constraints. |
| Outputs | structured article with headings, source boundaries, and unresolved factual placeholders. |
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
task = {"capability": "blog-writing", "brief_validated": True, "budget": 4}
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
