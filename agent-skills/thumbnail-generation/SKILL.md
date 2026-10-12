---
name: thumbnail-generation
description: Derive bounded thumbnail dimensions from source width and height using integer-only aspect-ratio arithmetic so preview sizes are exact, reproducible, and free of rounding drift.
metadata:
  source: skills/08-multimodal/thumbnail-generation.md
  category: 08-multimodal
  version: "v1"
---

# Thumbnail Generation

Category: Multimodal | Level: basic | Stability: experimental | Version: v1

## Description

A thumbnail pipeline needs one deterministic answer per input: given a source size and a bound, what target box does every runtime agree on? This skill defines that answer with integer math — scale by the limiting side, floor to whole pixels, never upscale past the bound — so galleries and indexes render identical sizes everywhere. Pixel resampling quality is out of scope; this is the sizing contract.

## When to Use

Use when generating preview images for galleries, feeds, or search results where the target box must be computed, not guessed, and must match across implementations.

Do not use for art-directed crops; creative sizing belongs to image editing, not to this mechanical contract.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `width` | `integer` | Yes | Source image width in pixels |
| `height` | `integer` | Yes | Source image height in pixels |
| `max_side` | `integer` | Yes | Largest permitted thumbnail dimension |
| `allow_upscale` | `boolean` | No | Whether already-small sources may be enlarged; default false |

## Procedure

1. Reject non-positive width, height, or max_side before any math runs.
2. Compute the scale as the minimum of max_side/width, max_side/height, and 1 when upscaling is disabled.
3. Apply the scale to both dimensions and floor to whole pixels, flooring identically in every implementation.
4. Clamp each result to at least one pixel so degenerate inputs never yield an empty box.
5. Return the box together with the computed scale so callers can verify the bound was respected.
6. Keep the operation pure: same inputs, same box, no environment state.

## Outputs

| Output | Type | Description |
|---|---|---|
| `box` | `(width, height)` | The integer thumbnail dimensions |
| `scale` | `number` | The limiting scale factor applied |

## Runnable Example

```python
def thumbnail_size(width, height, max_side, allow_upscale=False):
    """Fit (width, height) inside max_side preserving aspect ratio."""
    scale = min(max_side / width, max_side / height)
    if not allow_upscale:
        scale = min(scale, 1.0)
    new_w = max(1, int(width * scale))
    new_h = max(1, int(height * scale))
    return (new_w, new_h), round(scale, 4)

for source in [(1920, 1080), (1080, 1920), (256, 256)]:
    print(source, "->", thumbnail_size(*source, max_side=128))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Aspect distortion | One dimension rounded independently of the ratio | Scale both dimensions by the same limiting factor |
| Upscaled previews | Small sources enlarged and blurred | Cap the scale at 1.0 unless upscaling is explicitly enabled |
| Zero-size box | Degenerate source or flooring to zero | Clamp each dimension to at least one pixel |
| Cross-runtime drift | Float rounding differs by platform | Floor with integer truncation in a fixed order |
| Unbounded thumbnails | max_side not validated | Reject non-positive bounds before computing |

## Security and Authority Boundary

Thumbnails inherit the access state of their source image. Generating a preview grants no new viewing rights; protected media must keep its protection at every derived size.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s overview of thumbnails and their uses (https://en.wikipedia.org/wiki/Thumbnail).
2. Pillow’s documentation for image geometry operations (https://pillow.readthedocs.io/en/stable/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Video Frame Extraction](video-frame-extraction.md) — supplies representative frames that this skill sizes into previews.
- [Image Editing](image-editing.md) — performs the crop and resample steps once the target box is fixed.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
