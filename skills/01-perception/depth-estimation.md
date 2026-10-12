---
title: "Monocular Depth Estimation"
category: 01-perception
level: intermediate
stability: experimental
description: "Estimate per-pixel depth from a single image or video frame, ranking surfaces by distance with explicit handling of scale ambiguity, occlusion edges, and reflective surfaces."
added: "2026-10"
version: v1
related: ["image-understanding","video-understanding"]
---

# Monocular Depth Estimation

Category: Perception | Level: intermediate | Stability: experimental | Version: v1

## Description

Depth estimation maps every pixel of an image to a distance from the camera. In the monocular setting there is no stereo baseline and no known camera motion, so the raw output is a relative ordering of surfaces — closer versus farther — unless an external reference converts it to metric units. This skill covers running a depth estimator, aligning its relative output to a known scale when one exists, and reporting the ambiguity honestly.

## When to Use

Use when a single image or video feed must support distance-aware decisions: robot navigation, AR object placement, background separation, or defocus-aware editing.

Do not treat monocular depth as surveyed distance. Without a known reference the output is ordering only, and reflective or low-texture surfaces break even the ordering.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `image` | `image` | Yes | Single image or video frame |
| `reference` | `list` | No | Known size-at-distance pairs used to fit a metric scale |
| `mode` | `enum` | No | `relative` (default) or `metric` (requires `reference`) |

## Procedure

1. Normalize the input to the estimator's native resolution while preserving aspect ratio; record the resize factor.
2. Run the estimator and obtain the relative depth map.
3. If a metric scale is required, fit a single scale factor over the reference pairs with a least-squares alignment and report the residual.
4. Post-process with edge-aware smoothing only; hard occlusion boundaries must survive.
5. Produce a confidence channel: flag low-texture regions, mirrors, glass, and thin structures as unreliable.
6. Bound the cost: one estimator pass, no iterative refinement loops on unbounded inputs.

## Outputs

| Output | Type | Description |
|---|---|---|
| `depth_map` | `array` | Per-pixel depth (relative or metric per `mode`) |
| `confidence` | `array` | Per-pixel reliability flags |
| `scale_status` | `object` | Fitted scale, residual, or explicit `relative-only` marker |

## Runnable Example

```python
def fit_scale(reference_pairs):
    """reference_pairs: [(relative_depth, known_distance), ...]"""
    num = sum(r * d for r, d in reference_pairs)
    den = sum(r * r for r, _ in reference_pairs)
    if den == 0:
        return None
    scale = num / den
    residual = sum((scale * r - d) ** 2 for r, d in reference_pairs)
    return {"scale": round(scale, 4), "residual": round(residual, 4)}

print(fit_scale([(0.5, 100.0), (1.0, 200.0), (2.0, 410.0)]))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Relative depth read as meters | No reference was provided or fitted | Always emit `scale_status`; refuse silent metric claims |
| Reflective surfaces | Mirrors and glass return the reflected scene's depth | Flag glossy regions as unreliable |
| Occlusion edges smoothed away | Aggressive post-processing | Use edge-aware smoothing and check boundaries |
| Thin structures missed | Poles, wires, and cables vanish at low resolution | Report sub-pixel structures as low confidence |
| Scale drift across frames | Per-frame independent estimation in video | Use temporal consistency or report per-frame scale |

## Security and Authority Boundary

Depth maps reveal room layout and object placement; treat them as sensitive scene data. Do not route third-party images through estimators that log or retain inputs, and do not use depth output to infer information about identifiable people beyond the task's purpose.

## Evidence

This skill is grounded in dated public implementation references:

1. The MiDaS monocular depth estimation project (https://github.com/isl-org/MiDaS).
2. The Depth Anything V2 monocular depth estimation model repository (https://github.com/DepthAnything/Depth-Anything-V2).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Image Understanding](image-understanding.md) — the visual grounding layer that locates the surfaces being ranked.
- [Video Understanding](video-understanding.md) — the temporal context where per-frame depth must stay consistent.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
