---
title: "Image Resizing"
category: 08-multimodal
level: basic
stability: experimental
description: "Compute contain and cover resize boxes with integer arithmetic, explicit rounding, and declared upscale policy so scaled pixel targets are deterministic across runtimes."
added: "2026-10"
version: v1
related: ["image-editing", "chart-generation"]
---

# Image Resizing

Category: Multimodal | Level: basic | Stability: experimental | Version: v1

## Description

“Scale to fit” hides two different contracts: contain fits the whole image inside a box with letterboxing, cover fills the box and crops the overflow. This skill computes both as pure integer math with declared rounding and upscale rules, so every runtime derives the same target box from the same inputs. Resampling filters and color management are out of scope; this is the geometry contract that runs before them.

## When to Use

Use when a fixed display box must receive images of arbitrary aspect ratio and the output box — letterboxed, cropped, or bounded — must be computed exactly.

Do not use for art-directed aspect changes; creative crop choices belong to image editing, not to mechanical geometry.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `width` | `integer` | Yes | Source image width in pixels |
| `height` | `integer` | Yes | Source image height in pixels |
| `box` | `(width, height)` | Yes | Target bounding box |
| `strategy` | `"contain" | "cover"` | Yes | Fit inside the box, or fill it and crop |

## Procedure

1. Reject non-positive dimensions or box before computing.
2. Compute contain as the minimum scale that fits both sides, never exceeding the box on either axis.
3. Compute cover as the maximum scale that fills both sides, at least as large as the box on either axis.
4. Floor results to integer pixels with one documented rounding rule applied to both axes.
5. Apply the upscale policy: contain never exceeds the source size unless enlargement is declared; cover enlarges only as required to fill.
6. Return the box with the effective scale and the crop offsets for cover, so the caller can apply them mechanically.

## Outputs

| Output | Type | Description |
|---|---|---|
| `target` | `(width, height)` | The resized output dimensions |
| `scale` | `number` | Effective scale factor applied |
| `crop` | `(x, y)` | Cover-strategy center-crop offsets |

## Runnable Example

```python
def contain_box(width, height, box_w, box_h):
    scale = min(box_w / width, box_h / height, 1.0)
    return (max(1, int(width * scale)), max(1, int(height * scale))), round(scale, 4)

def cover_box(width, height, box_w, box_h):
    scale = max(box_w / width, box_h / height)
    w, h = int(width * scale), int(height * scale)
    crop = (max(0, (w - box_w) // 2), max(0, (h - box_h) // 2))
    return (max(box_w, w), max(box_h, h)), crop

print("contain:", contain_box(1920, 1080, 400, 400))
print("cover:", cover_box(1920, 1080, 400, 400))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Strategy confusion | Cover applied where contain was intended | Require the strategy argument and document the difference |
| Aspect drift | Independent per-axis rounding | Scale from one factor and floor both axes once |
| Unexpected upscale | Small sources enlarged by contain math | Cap scale at 1.0 unless enlargement is declared |
| Crop misalignment | Center offsets computed on the box, not the scaled size | Derive offsets from scaled dimensions minus the box |
| Zero-dimension output | Flooring small boxes to zero | Clamp outputs to at least one pixel |

## Security and Authority Boundary

Resizing grants no authority over source media and removes no protection: an access-controlled image stays access-controlled at every derived size, and metadata stripping is a separate decision that must be made explicitly.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s overview of image scaling algorithms (https://en.wikipedia.org/wiki/Image_scaling).
2. Pillow’s documentation for resize and thumbnail geometry (https://pillow.readthedocs.io/en/stable/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Image Editing](image-editing.md) — executes the resample and crop once this contract fixes the geometry.
- [Chart Generation](chart-generation.md) — consumes consistent resize geometry when composing figures into pages.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
