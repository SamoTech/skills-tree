---
name: sequential-workflow
description: Apply sequential workflow with explicit workflow state, ownership, validation, and bounded authority.
---

# sequential workflow

## Description
Apply sequential workflow only within explicit orchestration boundaries and preserve workflow state and ownership.

## Evidence
Canonical source: `skills/15-orchestration/sequential-workflow.md`. Repository schema, Agent Skills validation, security scanning, and CI define structural conformance.

## Usage
Validate workflow state, ownership, authority, and preconditions before execution; preserve postconditions and recovery state.

## Failure modes
- Ambiguous ownership or stale state.
- Invalid transition or unmet dependency.
- Duplicate or concurrent execution.
- Excess authority or resource scope.
- Unverifiable completion.

## Related
- `15-orchestration`
- `input-guardrails`
- `output-guardrails`
