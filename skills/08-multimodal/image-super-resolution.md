---
title: "Image Super-Resolution"
category: 08-multimodal
level: intermediate
stability: experimental
description: "Upscale low-resolution images with model-based super-resolution while bounding hallucinated detail, preserving identity-critical features, and labeling the synthesized output as reconstruction."
added: "2026-10"
version: v1
related: ["image-resizing","image-editing"]
---

# Image Super-Resolution

Category: Multimodal | Level: intermediate | Stability: experimental | Version: v1

## Description

Super-resolution uses a learned model to upscale an image beyond its pixel count. The model invents plausible high-frequency detail; it does not recover what was truly there. This skill covers applying SR appropriately, inspecting the output for hallucinated structure, and keeping the output labeled as a reconstruction — never as recovered evidence.

## When to Use

Use for restoring legacy assets, enlarging crops for human viewing, and cleaning up downscaled media where plausibility is the goal.

Do not use SR output for identification, forensics, medical reading, or any decision where invented detail could be mistaken for captured fact.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `image` | `image` | Yes | Low-resolution source image |
| `scale` | `enum` | No | Target upscale (x2 default; x4 for very low sources) |
| `content_type` | `enum` | No | `photo`, `text`, or `art` to select the model variant |

## Procedure

1. Confirm the use case permits synthesized detail; refuse evidentiary use up front.
2. Select the model variant matching the content type; text and faces need the strictest handling.
3. Run SR at a power-of-two scale; larger factors by chained passes, not one extreme pass.
4. Inspect the output for hallucination signatures: invented text glyphs, warped faces, repeated window or brick patterns.
5. Keep the original untouched alongside the output; never overwrite the source.
6. Record in metadata that the image is model-upscaled, with model and scale named.

## Outputs

| Output | Type | Description |
|---|---|---|
| `upscaled_image` | `image` | The synthesized high-resolution reconstruction |
| `quality_report` | `object` | Sharpness gain, artifact inspection summary |
| `hallucination_flags` | `list` | Regions where invented structure is suspected |

## Runnable Example

```python
def hallucination_risk(tile):
    if tile.get("text") or tile.get("face"):
        return "high"
    return "medium" if tile.get("variance", 0) > 0.5 else "low"

def inspect(tiles):
    counts = {}
    for t in tiles:
        r = hallucination_risk(t)
        counts[r] = counts.get(r, 0) + 1
    return counts

tiles = [{"text": True, "variance": 0.2}, {"variance": 0.3}, {"variance": 0.8}]
print(inspect(tiles))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Invented text or faces | Model fills in what it expects to see | Flag text/face tiles as high risk; human review |
| Identity drift | Upscaled face is a different, plausible person | Refuse identification use; compare against original |
| Over-sharpening artifacts | Halos at strong edges | Use conservative scale; inspect edges |
| Output treated as evidence | Reconstruction believed to be capture | Label outputs and keep the original |
| Noise upscaling | Sensor noise enlarged into texture | Denoise before SR, not after |

## Security and Authority Boundary

Super-resolution output is synthesized imagery. It must be labeled as such, must not feed identification or forensic pipelines, and must not be presented in a way that implies detail the sensor never captured.

## Evidence

This skill is grounded in dated public implementation references:

1. The Real-ESRGAN image restoration project (https://github.com/xinntao/Real-ESRGAN).
2. The realesrgan Python package (https://pypi.org/project/realesrgan/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Image Resizing](image-resizing.md) — the geometric counterpart that moves pixels without inventing detail.
- [Image Editing](image-editing.md) — the broader manipulation layer SR output feeds into.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
