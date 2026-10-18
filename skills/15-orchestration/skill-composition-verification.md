---
title: "Skill Composition Verification"
category: 15-orchestration
level: advanced
stability: experimental
description: "Verify that a composed set of skills is internally consistent by checking that every cross-skill input has a producing output, contracts match, and boundaries do not conflict."
added: "2026-10"
version: v1
related: [agent-authorization-context-propagation, safety-threshold-runtime-gating]
tags: [composition, verification, skills]
---
# Skill Composition Verification

## Description
Verify that a composed set of skills is internally consistent by checking that every cross-skill input has a producing output, contracts match, and boundaries do not conflict. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Several skills are being composed into one agent and the composition must be checked end to end.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | skill composition verification task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the skill composition verification steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A composition verification record with every cross-skill contract matched or flagged. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def resolve(needs, provides):
    return sorted(n for n in needs if n not in provides)
assert resolve(["index", "ranker"], {"index"}) == ["ranker"]
assert resolve(["index"], {"index"}) == []
```

## Failure Modes
- Acting outside the declared task boundary.
- Composing skills whose cross-consumed outputs have mismatched shapes.
- Leaving a needed input with no declared producer.
- Composing skills whose boundary claims contradict each other.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Skill composition verification needs appear in 2026 context engineering writeups. ([public signal](https://cruxdigits.nl/blog/context-engineering-ai-agents-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Authorization Context Propagation](../15-orchestration/agent-authorization-context-propagation.md)
- [Safety Threshold Runtime Gating](../15-orchestration/safety-threshold-runtime-gating.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
