---
title: "Shared Memory"
category: 15-orchestration
level: advanced
stability: stable
description: "Coordinate shared workflow state across agents using explicit schemas, ownership, synchronization, and provenance."
added: "2025-03"
related: ["15-orchestration", "input-guardrails", "output-guardrails"]
---

**Category:** Orchestration
**Skill Level:** `advanced`
**Stability:** stable

## Description
Coordinate shared workflow state across agents using explicit schemas, ownership, synchronization, and provenance.

## When to Use
Use when multiple agents need a common state store or shared context.

## Inputs / Outputs / Failure Modes
| Area | Contract |
|---|---|
| Inputs | Workflow state, roles, task constraints, dependencies, authorization, and acceptance criteria. |
| Outputs | Explicit orchestration state/result with ownership, evidence, and recovery information. |
| Failure modes | Stale state, ambiguous transitions, duplicate work, missing authority, or unverifiable completion. |

## Procedure
1. Establish state, ownership, dependencies, and acceptance criteria.
2. Validate preconditions before changing workflow state.
3. Execute the declared orchestration operation within bounded authority.
4. Record state changes, evidence, and unresolved conditions.
5. Apply explicit retry, recovery, escalation, or terminal behavior when required.

## Runnable Example
```python
task = {"capability": "shared-memory", "validated": True}
assert task["validated"]
result = {"status": "orchestration_step", "capability": task["capability"]}
print(result)
```

## Failure Modes
- Missing or ambiguous workflow state.
- Invalid transition or unmet dependency.
- Duplicate or concurrent execution.
- Capability or authority exceeds declared scope.
- Completion cannot be verified.

## Orchestration Boundary
Concurrent writes can corrupt state; define ownership, versioning, and conflict handling.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Orchestration state must remain explicit, bounded, and traceable.

## Related
- 15-orchestration
- input-guardrails
- output-guardrails
