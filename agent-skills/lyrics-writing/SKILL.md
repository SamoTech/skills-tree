---
name: lyrics-writing
description: Write original song lyrics with declared structure, meter, rhyme, theme, and genre constraints while avoiding unauthorized reproduction of existing lyrics. Preserve originality, source permissions, factual boundaries, and the requested creative contract.
---

# Lyrics Writing

## Description

Write original song lyrics with declared structure, meter, rhyme, theme, and genre constraints while avoiding unauthorized reproduction of existing lyrics.

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
task = {"capability": "lyrics-writing", "brief_validated": True, "budget": 4}
assert task["brief_validated"] and task["budget"] > 0
print({"status": "creative_contract_checked", "capability": task["capability"]})
```

## Evidence

Canonical repository skill: skills/13-creative/lyrics-writing.md. Repository schema, validation workflows, Agent Skills contract, and security gates define local conformance. Creative output is an artifact, not evidence of factual claims.

## Related

- 13-creative
- input-guardrails
- output-guardrails
