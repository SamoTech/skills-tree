---
name: vm-interaction
description: Perform vm interaction as a verified computer-use capability with explicit target and postcondition checks.
---

# vm interaction

## Description
Perform vm interaction only against a verified UI or session target and expected state.

## Evidence
Canonical source: `skills/10-computer-use/vm-interaction.md`. Repository schema, Agent Skills validation, security scanning, and CI define structural conformance.

## Usage
Verify target identity, session state, authorization, and expected postcondition before and after the action.

## Failure modes
- Stale or ambiguous UI/session target.
- Geometry or focus drift.
- Unexpected application state.
- Sensitive-data exposure or destructive side effect.
- Postcondition cannot be verified.

## Related
- `10-computer-use`
- `input-guardrails`
- `output-guardrails`
