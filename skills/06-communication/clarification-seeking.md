---
title: "Clarification Seeking"
category: 06-communication
level: intermediate
stability: stable
description: "Identify material ambiguity or missing constraints and ask the smallest set of questions needed to proceed safely."
added: "2025-03"
related: ["06-communication", "input-guardrails", "output-guardrails"]
---

## Description

Identify material ambiguity or missing constraints and ask the smallest set of questions needed to proceed safely.

## When to Use

Use when the communication objective, audience, evidence boundary, and acceptance criteria are explicit.

## Inputs / Outputs / Failure Modes

| Area | Contract |
|---|---|
| Inputs | user request, known constraints, and decision-impact threshold. |
| Outputs | focused clarification questions or a justified decision to proceed. |
| Failure modes | Ambiguous intent, unsupported claims, constraint conflicts, tone mismatch, omitted uncertainty, or output accepted without checking the requested contract. |

## Procedure

1. Parse the requested purpose, audience, constraints, and evidence boundary.
2. Resolve precedence between explicit requirements and defaults.
3. Draft or construct the response while preserving source meaning and provenance.
4. Check factual claims, required format, terminology, tone, and omissions.
5. Verify the result against the declared acceptance criteria.
6. Ask a focused clarification question when unresolved ambiguity could materially change the result.

## Runnable Example

```python
task = {"capability": "clarification-seeking", "validated": True, "budget": 4}
assert task["validated"] and task["budget"] > 0
print({"status": "contract_checked", "capability": task["capability"]})
```

## Failure Modes

- User intent is ambiguous or materially underspecified.
- Claims are presented without supporting evidence.
- Constraints conflict and precedence is unclear.
- Style or persona instructions override factual accuracy or safety boundaries.
- Translation or paraphrase changes the source meaning.
- Completion is reported without checking the requested format or postcondition.

## Safety Boundary

Communication style does not create authority or factual evidence. Preserve uncertainty, do not fabricate citations or sources, and keep sensitive information within the declared authorization boundary.

## Evidence

Canonical repository skill: this file. Structural conformance is governed by the repository schema, validation workflows, Agent Skills contract, and security gates. Communication-specific claims require reproducible implementation evidence or authoritative primary documentation; generated prose is not evidence by itself.

## Related

- 06-communication
- input-guardrails
- output-guardrails
