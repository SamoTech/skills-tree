---
name: keyboard-type
description: Perform keyboard type as a verified computer-use capability with explicit target and postcondition checks.
---

# keyboard type

## Description
Perform keyboard type only against a verified UI target and expected application state.

## Evidence
Canonical source: `skills/10-computer-use/keyboard-type.md`. Repository schema, Agent Skills validation, security scanning, and CI define structural conformance.

## Usage
Verify target identity, focus, authorization, and expected postcondition before and after the action.

## Failure modes
- Stale or ambiguous UI target.
- Unexpected application state.
- Coordinate drift or focus loss.
- Destructive side effect without explicit authorization.
- Postcondition cannot be verified.

## Related
- `10-computer-use`
- `input-guardrails`
- `output-guardrails`
