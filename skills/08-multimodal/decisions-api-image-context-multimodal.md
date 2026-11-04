---
title: "Decisions API Image Context Multimodal"
category: 08-multimodal
level: advanced
stability: experimental
description: "Combine image inputs with a bounded decision question so classification over visual context returns one of a finite answer set with recorded evidence."
added: "2026-11"
version: v1
related: [screenshot-capture]
tags: [multimodal, decisions, images, classification]
---
# Decisions API Image Context Multimodal

## Description
Combine image inputs with a bounded decision question so classification over visual context returns one of a finite answer set with recorded evidence. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A visual input (screenshot, scan, photo) must drive a routing decision among known answers.
- The outcome would change if the visual answer were free-form and downstream automation could not consume it.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The image payload reference, the bounded decision question, and the finite answer set. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Attach the image context to the decision request and parse the answer against the finite set.
4. Record the image reference, answer, and residual-case fallback when the image is out of distribution.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A visual-decision record with image reference, chosen answer, and residual disposition. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def decide_visual(decide, image_ref, answers):
    a = decide(image_ref)
    if a not in answers:
        return {"answer": "residual", "fallback": "human_review"}
    return {"answer": a, "image": image_ref}
r = decide_visual(lambda i: "damaged", "img/1", ["damaged", "intact"])
assert r["answer"] == "damaged" and r["image"] == "img/1"
assert decide_visual(lambda i: "maybe", "img/2", ["damaged", "intact"])["answer"] == "residual"
```

## Failure Modes
- The decision runs without keeping the image reference, breaking evidence traceability.
- Out-of-distribution images are forced into the nearest answer instead of the residual path.
- The image is sent to the decision endpoint without checking payload limits.
- Answers are accepted that are not members of the declared finite set.
- The visual decision is cached and reused for a changed image.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI DevDay 2026 announced the Decisions API for real-time classification and routing with finite pre-defined answers, available alongside multimodal model context (OpenAI DevDay recap, dated November 4, 2026) ([public signal](https://openai.com/index/devday-2026-recap/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Screenshot Capture](../10-computer-use/screenshot-capture.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
