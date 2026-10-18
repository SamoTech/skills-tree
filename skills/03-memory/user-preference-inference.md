---
title: "User Preference Inference"
category: 03-memory
level: advanced
stability: experimental
description: "Infer durable user preferences from observed corrections and explicit statements, storing them with provenance and confidence instead of overwriting conflicting facts."
added: "2026-10"
version: v1
related: [user-profile-memory, preference-drift-detection]
tags: [memory, personalization, provenance]
---
# User Preference Inference

## Description
Infer durable user preferences from observed corrections and explicit statements, storing them with provenance and confidence instead of overwriting conflicting facts. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent must record an inferred user preference with evidence rather than asserting it silently.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | user preference inference task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the user preference inference steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A preference entry with source evidence, confidence, and the observed behavior it was inferred from. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def store(inferred, has_evidence):
    return inferred and has_evidence
assert store(True, True) is True
assert store(True, False) is False
```

## Failure Modes
- Acting outside the declared task boundary.
- Storing a single correction as a durable preference without recurrence evidence.
- Overwriting an existing preference instead of recording the conflict.
- Hiding low-confidence preferences from later review.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Context engineering guides store durable user preferences with provenance. ([public signal](https://mem0.ai/blog/context-engineering-ai-agents-guide))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [User Profile Memory](../03-memory/user-profile-memory.md)
- [Preference Drift Detection](../03-memory/preference-drift-detection.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
