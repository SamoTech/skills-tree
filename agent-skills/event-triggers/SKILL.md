---
name: event-triggers
description: Apply event triggers with explicit workflow state, ownership, validation, and failure handling.
---

# event triggers

## Description
Apply event triggers only within explicit orchestration boundaries and preserve workflow state and ownership.

## Evidence
Canonical source: `skills/15-orchestration/event-triggers.md`. Repository schema, Agent Skills validation, security scanning, and CI define structural conformance.

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
