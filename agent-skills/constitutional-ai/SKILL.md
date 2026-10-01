---
name: constitutional-ai
description: Apply constitutional ai with explicit objectives, evaluation criteria, evidence boundaries, and resource limits.
---

# constitutional ai

## Description
Apply constitutional ai only within explicit agentic workflow constraints and preserve evaluation state.

## Evidence
Canonical source: `skills/09-agentic-patterns/constitutional-ai.md`. Repository schema, Agent Skills validation, security scanning, and CI define structural conformance.

## Usage
Define objective, context, evaluator, resource limits, stopping conditions, and evidence requirements before execution.

## Failure modes
- Goal drift or ambiguous stopping condition.
- Evaluator bias or correlated failure.
- Unsupported output treated as grounded.
- Unbounded search or tool use.
- Completion without evidence or validation.

## Related
- `09-agentic-patterns`
- `input-guardrails`
- `output-guardrails`
