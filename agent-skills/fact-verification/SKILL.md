---
name: fact-verification
description: Evaluate factual claims against declared evidence sources and classify them as verified, contradicted, unverified, or uncertain. Use explicit provenance, retention boundaries, uncertainty handling, and verification.
---

# Fact Verification

## Description

Evaluate factual claims against declared evidence sources and classify them as verified, contradicted, unverified, or uncertain.

## When to Use

Use when memory state must persist across steps or sessions and its scope and verification rules are explicit.

## Inputs / Outputs

- Inputs: validated memory candidates, task context, provenance, authorization, and retention constraints.
- Outputs: scoped memory state with provenance, uncertainty, and verification status.

## Procedure

1. Define scope, owner, retention, and acceptance criteria.
2. Validate candidates and preserve provenance.
3. Apply freshness, confidence, conflict, and size bounds.
4. Retrieve only task-relevant state.
5. Revalidate memory before treating it as authoritative when material.
6. Record updates and unresolved uncertainty.

## Failure Modes

- Stale or unsupported memory.
- Inference stored as fact.
- Conflicting records silently merged.
- Unauthorized retention.
- Context or storage exhaustion.
- Required revalidation skipped.

## Runnable Example

```python
memory = {"capability": "fact-verification", "validated": True, "budget": 4}
assert memory["validated"] and memory["budget"] > 0
print({"status": "bounded_memory_operation", "capability": memory["capability"]})
```

## Evidence

Canonical repository skill: skills/03-memory/fact-verification.md. Repository schema, validation workflows, Agent Skills contract, and security gates define local conformance. Stored memory is not evidence by itself.

## Related

- 03-memory
- input-guardrails
- output-guardrails
