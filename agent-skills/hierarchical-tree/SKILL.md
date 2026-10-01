---
name: hierarchical-tree
description: Apply hierarchical tree with explicit workflow state, ownership, validation, and failure handling.
---

# hierarchical tree

## Description
Apply hierarchical tree only within explicit orchestration boundaries and preserve workflow state and ownership.

## Evidence
Canonical source: `skills/15-orchestration/hierarchical-tree.md`. Repository schema, Agent Skills validation, security scanning, and CI define structural conformance.

## Usage
Validate workflow state and ownership before execution; preserve material evidence and postconditions.

## Failure modes
- Ambiguous ownership or stale state.
- Duplicate or concurrent execution.
- Missing authorization or recovery path.
- Unverifiable completion.

## Related
- `15-orchestration`
- `input-guardrails`
- `output-guardrails`
