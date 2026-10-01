---
title: "Bootstrapping"
category: 09-agentic-patterns
level: advanced
stability: stable
description: "Initialize an agent workflow from explicit capabilities, initial state, tools, constraints, and stopping conditions."
added: "2025-03"
related: ["09-agentic-patterns", "input-guardrails", "output-guardrails"]
---

**Category:** Agentic Patterns
**Skill Level:** `advanced`
**Stability:** stable

## Description
Initialize an agent workflow from explicit capabilities, initial state, tools, constraints, and stopping conditions.

## When to Use
Use when an agent run needs deterministic initialization before execution.

## Inputs / Outputs / Failure Modes
| Area | Contract |
|---|---|
| Inputs | Agent state, task objective, constraints, evidence/context, tools or evaluators, and stopping criteria. |
| Outputs | Structured agent result with provenance, uncertainty, and validation state. |
| Failure modes | Goal drift, evaluator bias, unsupported inference, unbounded search, or incomplete grounding. |

## Procedure
1. Establish the objective, state, constraints, evaluation criteria, and stopping conditions.
2. Validate the available context and tool authority before execution.
3. Apply the declared agentic pattern within explicit resource bounds.
4. Evaluate outputs against evidence and acceptance criteria.
5. Preserve uncertainty and stop or escalate when the evidence is insufficient.

## Runnable Example
```python
task = {"pattern": "bootstrapping", "validated": True}
assert task["validated"]
result = {"status": "evaluation_required", "pattern": task["pattern"]}
print(result)
```

## Failure Modes
- Ambiguous objective or stopping condition.
- Evaluator or critic shares the same failure mode as the generator.
- Unsupported claims treated as grounded output.
- Resource use grows without an explicit bound.
- Completion reported without evidence or validation.

## Pattern Boundary
Initialization must not grant tools or authority beyond the declared configuration.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Agentic-pattern outputs require explicit evaluation and evidence boundaries.

## Related
- 09-agentic-patterns
- input-guardrails
- output-guardrails
