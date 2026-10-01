---
name: blog-writing
description: Produce a structured blog article that matches the requested audience, purpose, length, voice, and factual boundaries. Preserve originality, source permissions, factual boundaries, and the requested creative contract.
---

# Blog Writing

## Description

Produce a structured blog article that matches the requested audience, purpose, length, voice, and factual boundaries.

## When to Use

Use when the creative brief, audience, deliverable, and acceptance criteria are explicit.

## Inputs / Outputs

- Inputs: creative brief, source material permissions, audience, and format constraints.
- Outputs: creative artifact with constraint checks, provenance notes, and unresolved assumptions.

## Procedure

1. Parse brief, audience, purpose, and protected constraints.
2. Establish originality and source-use boundaries.
3. Generate within explicit format and length limits.
4. Check structure, consistency, and factual claims.
5. Preserve source attribution and distinguish invention from source material.
6. Validate the deliverable against the brief.

## Failure Modes

- Underspecified brief.
- Invented factual or product claims.
- Structure or audience mismatch.
- Unauthorized reproduction or imitation.
- Unauthorized likeness or source asset use.
- Unverified completion.

## Runnable Example

```python
task = {"capability": "blog-writing", "brief_validated": True, "budget": 4}
assert task["brief_validated"] and task["budget"] > 0
print({"status": "creative_contract_checked", "capability": task["capability"]})
```

## Evidence

Canonical repository skill: skills/13-creative/blog-writing.md. Repository schema, validation workflows, Agent Skills contract, and security gates define local conformance. Creative output is an artifact, not evidence of factual claims.

## Related

- 13-creative
- input-guardrails
- output-guardrails
