---
title: "Safety Threshold Runtime Gating"
category: 15-orchestration
level: advanced
stability: experimental
description: "Gate agent actions at runtime against declared safety thresholds, failing closed whenever a threshold is missing, ambiguous, or the action risk class is undefined."
added: "2026-10"
version: v1
related: [model-card-safety-threshold-parsing, autonomy-threshold-reasoning]
tags: [runtime, gating, safety]
---
# Safety Threshold Runtime Gating

## Description
Gate agent actions at runtime against declared safety thresholds, failing closed whenever a threshold is missing, ambiguous, or the action risk class is undefined. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent actions must be gated at runtime against declared safety thresholds.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | safety threshold runtime gating task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the safety threshold runtime gating steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A per-action gate verdict of allow, threshold-deny, or fail-closed no-rule deny. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def gate(action, thresholds):
    rule = thresholds.get(action["risk_class"])
    if rule is None:
        return "deny_no_rule"
    return "allow" if action["score"] <= rule else "deny_threshold"
th = {"high": 0.8}
assert gate({"risk_class": "high", "score": 0.5}, th) == "allow"
assert gate({"risk_class": "high", "score": 0.9}, th) == "deny_threshold"
assert gate({"risk_class": "g3", "score": 0.1}, th) == "deny_no_rule"
```

## Failure Modes
- Acting outside the declared task boundary.
- Allowing an action whose risk class has no rule, on the excuse of urgency.
- Comparing scores to thresholds computed with different units.
- Treating an ambiguous threshold as the looser reading.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Runtime safety gating requirements appear in 2026 model card guidance. ([public signal](https://aitechmodel.com/what-is-new-with-agentic-ai-in-october-2026-latest-model-cards-and))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Model Card Safety Threshold Parsing](../12-data/model-card-safety-threshold-parsing.md)
- [Autonomy Threshold Reasoning](../02-reasoning/autonomy-threshold-reasoning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
