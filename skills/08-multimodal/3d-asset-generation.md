---
title: "3D Asset Generation"
category: 08-multimodal
level: intermediate
stability: experimental
description: "Generate 3D assets from specifications or references with topology, scale, and format constraints verified before delivery."
added: "2026-10"
version: v1
related: [3d-scene-understanding, image-generation, svg-generation]
tags: [3d, asset, generation, multimodal]
---

# 3D Asset Generation

## Description
Generate 3D assets from specifications or references with topology, scale, and format constraints verified before delivery. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires 3d asset generation before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for 3d asset generation. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the 3d asset generation procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# 3D Asset Generation: deterministic check
candidates = [{"id": "a", "score": 0.8, "cost": 2}, {"id": "b", "score": 0.95, "cost": 9}]
eligible = [c for c in candidates if c["score"] >= 0.8]
selected = min(eligible, key=lambda c: c["cost"])
assert selected["id"] == "a"
print("selected:", selected["id"])
```

## Failure Modes
- Proceeding with 3d asset generation without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
3D generation is a 2026 creative-tooling trend; asset pipelines for agents are a public request pattern. These are dated public signals, not adoption metrics.

## Related
- 3d-scene-understanding.md
- image-generation.md
- ../13-creative/svg-generation.md
