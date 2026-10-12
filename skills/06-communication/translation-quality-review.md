---
title: "Translation Quality Review"
category: 06-communication
level: intermediate
stability: experimental
description: "Review translations for fidelity, terminology consistency, and locale correctness against the source, with a defect list and severity per issue."
added: "2026-10"
version: v1
related: [translation, multilingual-output, citation-attribution]
tags: [translation, quality, review, communication]
---

# Translation Quality Review

## Description
Review translations for fidelity, terminology consistency, and locale correctness against the source, with a defect list and severity per issue. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires translation quality review before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for translation quality review. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the translation quality review procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Translation Quality Review: deterministic check
options = [{"name": "x", "gain": 5, "cost": 1}, {"name": "y", "gain": 4, "cost": 1}]
ranked = sorted(options, key=lambda o: (o["cost"], -o["gain"]))
assert ranked[0]["name"] == "x"
print("best:", ranked[0]["name"])
```

## Failure Modes
- Proceeding with translation quality review without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Localization quality assurance automation is a 2026 request pattern; translation quality review differs from raw translation. These are dated public signals, not adoption metrics.

## Related
- translation.md
- multilingual-output.md
- citation-attribution.md
