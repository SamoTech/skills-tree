---
name: question-answering
description: Answer questions using the declared evidence boundary and distinguish retrieved facts, supplied context, inference, and unknowns. Preserve evidence boundaries, uncertainty, and requested output constraints.
---

# Question Answering

## Description

Answer questions using the declared evidence boundary and distinguish retrieved facts, supplied context, inference, and unknowns.

## When to Use

Use when the communication objective, audience, and acceptance criteria are explicit.

## Inputs / Outputs

- Inputs: task intent, audience, constraints, evidence boundary, and source material where applicable.
- Outputs: structured communication result with assumptions, provenance, and unresolved uncertainty where material.

## Procedure

1. Parse purpose, audience, constraints, and evidence boundary.
2. Resolve precedence among explicit requirements.
3. Produce the requested communication.
4. Check facts, format, terminology, tone, and omissions.
5. Verify the result against the declared criteria.
6. Clarify material ambiguity rather than guessing.

## Failure Modes

- Ambiguous or conflicting requirements.
- Unsupported claims or fabricated sources.
- Constraint or format mismatch.
- Tone/persona overriding factual accuracy or safety.
- Source meaning changed during transformation.
- Unverified completion.

## Runnable Example

```python
task = {"capability": "question-answering", "validated": True, "budget": 4}
assert task["validated"] and task["budget"] > 0
print({"status": "contract_checked", "capability": task["capability"]})
```

## Evidence

Canonical repository skill: skills/06-communication/question-answering.md. Repository schema, validation workflows, Agent Skills contract, and security gates define local conformance. Generated prose is not evidence by itself.

## Related

- 06-communication
- input-guardrails
- output-guardrails
