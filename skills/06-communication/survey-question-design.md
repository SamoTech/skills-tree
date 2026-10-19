---
title: "Survey Question Design"
category: 06-communication
level: advanced
stability: experimental
description: "Design survey questions so that responses measure the declared construct without leading wording, double-barreled items, or unbalanced scales."
added: "2026-10"
version: v1
related: [requirement-elicitation-interviewing, evaluation-dataset-curation]
tags: [surveys, questions, evaluation, design]
---
# Survey Question Design

## Description
Design survey questions so that responses measure the declared construct without leading wording, double-barreled items, or unbalanced scales. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Feedback or evaluation data must be collected with questions that measure what they claim.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Define the construct each question measures, check each item for leading wording, double barrels, and scale balance, and pilot the instrument with a small respondent set before full deployment.
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
def item_ok(item):
    if " or " in item["text"].lower():
        return False
    return len(item["scale"]) % 2 == 1 and "neutral" in item["scale"]
assert item_ok({"text": "How satisfied are you", "scale": ["low", "neutral", "high"]})
assert not item_ok({"text": "Was it fast or friendly", "scale": ["low", "high"]})
```

## Failure Modes
- A double-barreled item is kept because it reads naturally and the responses are uninterpretable..
- Scale labels are unbalanced, steering respondents toward the favorable end..
- The pilot is skipped and a broken item ships to the full population..
- The construct definition is written after the data arrives to fit the answers..
- Demographic items are collected without a purpose and leak identity for no measurement gain..

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 evaluation practice covers instrument design quality as a prerequisite for trustworthy agent feedback data (futransolutions.com, dated October 2026) ([public signal](https://futransolutions.com/blog/ai-agent-observability-in-2026-how-to-trace-evaluate-and-debug-ai-that-takes-action/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Requirement Elicitation Interviewing](../06-communication/requirement-elicitation-interviewing.md)
- [Evaluation Dataset Curation](../12-data/evaluation-dataset-curation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
