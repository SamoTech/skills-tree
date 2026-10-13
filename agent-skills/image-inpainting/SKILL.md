---
name: image-inpainting
description: Fill masked image regions with content constrained by a declared mask inventory, edge continuity checks, and provenance records when inpainting is used at all.
metadata:
  source: skills/08-multimodal/image-inpainting.md
  category: 08-multimodal
  version: "v1"
---

# Image Inpainting

## Description
Fill masked image regions with content constrained by a declared mask inventory, edge continuity checks, and provenance records when inpainting is used at all. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- damaged or occluded image regions must be filled while the alteration is recorded and bounded.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for image inpainting work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the image inpainting steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def fill_report(mask_area, edits, allowed):
    flagged = [e for e in edits if e["region"] not in allowed and mask_area[e["region"]] > 0.05]
    return {"edits": edits, "flagged": flagged}

mask = {"face": 0.2, "background": 0.01}
edits = [{"region": "face"}, {"region": "background"}]
rep = fill_report(mask, edits, {"background"})
assert [f["region"] for f in rep["flagged"]] == ["face"]
```

## Failure Modes
- Inpainting regions that carry semantic or legal weight.
- No provenance record that content was synthesized.
- Blurring the mask boundary into surrounding pixels.
- Inpainting without preserving measurement data in the image.
- Using inpainted images as training evidence.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Synthesized image content disclosure is a recurring 2026 media-integrity topic in public coverage; this is a dated signal, not an adoption metric.

## Related
- image-editing.md
- image-generation.md
- image-super-resolution.md
