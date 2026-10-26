---
title: "Image Model Release Capability Comparison"
category: 08-multimodal
level: advanced
stability: experimental
description: "Compare newly released image models on declared capability criteria with recorded evidence instead of gallery impressions."
added: "2026-10"
version: v1
related: [image-generation, model-selection-reasoning]
tags: [image, models, release, comparison]
---
# Image Model Release Capability Comparison

## Description
Compare newly released image models on declared capability criteria with recorded evidence instead of gallery impressions. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A multimodal agent must decide whether a new image model replaces the incumbent on declared criteria.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. For each declared capability criterion, record the verdict with evidence from the model card or a controlled test, and name the criteria the rejected model failed.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def compare_image(new, incumbent, criteria):
    verdicts = {c: bool(new[c]) for c in criteria}
    return {"switch": all(verdicts.values()) and not all(bool(incumbent[c]) for c in criteria), "verdicts": verdicts}
r = compare_image({"text_render": True, "consistency": True}, {"text_render": False, "consistency": True}, ["text_render", "consistency"])
assert r["switch"] and r["verdicts"]["text_render"]
```

## Failure Modes
- Gallery samples are treated as capability proof and cherry-picked outputs drive the switch.
- Model card claims are recorded without test conditions and capabilities are overstated.
- The incumbent is not compared and the new model wins by novelty.
- Rejected criteria are not named and later reviews cannot see why the switch happened.
- The switch is all-at-once and a regression strands every image pipeline.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The October 2026 model and tool release tracker covering new image models is the dated release stream this comparison evaluates. ([public signal](https://gadgetsfocus.com/october-2026-ai-models-tools-release-tracker-mistral-large-4-beam-gemini-agent/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Image Generation](../08-multimodal/image-generation.md)
- [Model Selection Reasoning](../02-reasoning/model-selection-reasoning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
