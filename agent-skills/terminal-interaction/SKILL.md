---
name: terminal-interaction
description: Perform terminal interaction as a verified computer-use capability with explicit target and postcondition checks.
---

# terminal interaction

## Description
Perform terminal interaction only against a verified UI or session target and expected state.

## Evidence
Canonical source: `skills/10-computer-use/terminal-interaction.md`. Repository schema, Agent Skills validation, security scanning, and CI define structural conformance.

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
