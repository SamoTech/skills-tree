---
title: "Fact Verification Memory"
category: 03-memory
level: advanced
stability: stable
description: "Maintain a versioned cache of verified, contradicted, and unresolved claims with provenance and freshness metadata."
added: "2025-03"
related: ["03-memory", "input-guardrails", "output-guardrails"]
---

## Description

Maintain a versioned cache of verified, contradicted, and unresolved claims with provenance and freshness metadata.

## When to Use

Use when memory state must persist across steps or sessions and the workflow can define ownership, provenance, retention, and verification rules.

## Inputs / Outputs / Failure Modes

| Area | Contract |
|---|---|
| Inputs | claim, evidence references, verdict, verification time, freshness policy, and scope. |
| Outputs | memory record with verdict, provenance, freshness, and revalidation requirement. |
| Failure modes | Stale memory, unsupported inference, conflicting records, unauthorized retention, context growth, or acceptance without revalidation. |

## Procedure

1. Define the memory scope, owner, retention rule, and acceptance criteria.
2. Validate incoming memory candidates and preserve their provenance.
3. Apply explicit freshness, confidence, conflict, and size bounds.
4. Retrieve only the memory relevant to the current task.
5. Revalidate memory before treating it as authoritative when material.
6. Record updates, conflicts, and unresolved uncertainty.

## Runnable Example

```python
memory = {"capability": "fact-verification-memory", "validated": True, "budget": 4}
assert memory["validated"] and memory["budget"] > 0
print({"status": "bounded_memory_operation", "capability": memory["capability"]})
```

## Failure Modes

- Memory is stale or its provenance cannot be established.
- A model-generated inference is stored as an explicit user fact.
- Conflicting records are silently merged.
- Retention exceeds the declared scope or authorization.
- Memory growth exhausts context or storage budgets.
- A stored procedure or fact is used without required revalidation.

## Safety Boundary

Treat memory as state, not truth. Preserve provenance and scope. Do not store sensitive or personal information unless explicitly authorized by the governing application policy, and honor correction or deletion requirements.

## Evidence

Canonical repository skill: this file. Structural conformance is governed by the repository schema, validation workflows, Agent Skills contract, and security gates. Memory-specific claims require reproducible implementation evidence or authoritative repository evidence; stored memory is not evidence by itself.

## Related

- 03-memory
- input-guardrails
- output-guardrails
