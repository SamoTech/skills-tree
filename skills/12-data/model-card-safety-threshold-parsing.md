---
title: "Model Card Safety Threshold Parsing"
category: 12-data
level: advanced
stability: experimental
description: "Parse model card safety thresholds into a typed record with units and applicability conditions, flagging missing or contradictory thresholds before any runtime gate consumes them."
added: "2026-10"
version: v1
related: [safety-threshold-runtime-gating, safety-threshold-disclosure-writing]
tags: [model-cards, parsing, thresholds]
---
# Model Card Safety Threshold Parsing

## Description
Parse model card safety thresholds into a typed record with units and applicability conditions, flagging missing or contradictory thresholds before any runtime gate consumes them. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Runtime gating will consume a model card declared safety thresholds.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | model card safety threshold parsing task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the model card safety threshold parsing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A typed threshold record with missing and contradictory thresholds flagged. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def parse_card(card, required):
    missing = sorted(k for k in required if card.get(k) is None)
    return {"usable": not missing, "missing": missing}
c = parse_card({"refusal_rate_max": 0.02}, ["refusal_rate_max", "autonomy_level"])
assert c["usable"] is False and c["missing"] == ["autonomy_level"]
```

## Failure Modes
- Acting outside the declared task boundary.
- Consuming a card whose required threshold is missing.
- Reading a threshold without its unit and applying it to the wrong scale.
- Treating contradictory thresholds as valid by taking the looser one.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Model card threshold parsing needs appear in 2026 model card guidance. ([public signal](https://aitechmodel.com/what-is-new-with-agentic-ai-in-october-2026-latest-model-cards-and))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Safety Threshold Runtime Gating](../15-orchestration/safety-threshold-runtime-gating.md)
- [Safety Threshold Disclosure Writing](../06-communication/safety-threshold-disclosure-writing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
