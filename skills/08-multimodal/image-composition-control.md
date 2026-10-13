---
title: "Image Composition Control"
category: 08-multimodal
level: advanced
stability: experimental
description: "Generate images with declared composition constraints such as subject placement, horizon level, and depth cues, verified against the rendered output."
added: "2026-10"
version: v1
related: [image-generation, style-reference-image-generation, chart-generation]
tags: [images, composition, generation]
---

# Image Composition Control

## Description
Generate images with declared composition constraints such as subject placement, horizon level, and depth cues, verified against the rendered output. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an image must follow explicit composition rules rather than loose text prompts.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for image composition control work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the image composition control steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def check(out, rules):
    problems = []
    if "horizon" in rules and out["horizon"] != rules["horizon"]:
        problems.append("horizon")
    for zone, subject in rules.get("placement", {}).items():
        if out["placement"].get(zone) != subject:
            problems.append("placement:" + zone)
    return problems

rules = {"horizon": "upper-third", "placement": {"left": "tree"}}
good = {"horizon": "upper-third", "placement": {"left": "tree"}}
bad = {"horizon": "center", "placement": {"left": "tree"}}
assert check(good, rules) == []
assert check(bad, rules) == ["horizon"]
```

## Failure Modes
- Declaring composition in the prompt but never checking the output.
- Conflicting zone assignments.
- Treating a close render as a pass.
- No iteration loop when checks fail.
- Assuming aspect ratios transfer between models.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Controllable image composition is a recurring 2026 image-generation request in public developer discussion; this is a dated signal, not an adoption metric.

## Related
- image-generation.md
- style-reference-image-generation.md
- chart-generation.md
