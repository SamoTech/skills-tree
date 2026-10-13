---
name: subject-consistency-image-generation
description: Generate a consistent subject across multiple images using reference conditioning, feature distance checks, and rejection of inconsistent renders.
metadata:
  source: skills/08-multimodal/subject-consistency-image-generation.md
  category: 08-multimodal
  version: "v1"
---

# Subject Consistency Image Generation

## Description
Generate a consistent subject across multiple images using reference conditioning, feature distance checks, and rejection of inconsistent renders. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- one character or product must look the same across a set of generated images.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for subject consistency image generation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the subject consistency image generation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def accept(reference, candidates, max_dist):
    kept = []
    for c in candidates:
        d = abs(c["embedding"] - reference)
        if d <= max_dist:
            kept.append(c["id"])
    return kept

ref = 0.50
cands = [{"id": 1, "embedding": 0.52}, {"id": 2, "embedding": 0.9}]
assert accept(ref, cands, 0.05) == [1]
```

## Failure Modes
- Accepting renders that drift because regenerating is slow.
- No numeric consistency check, only eyeballing.
- Changing style parameters between shots.
- Reference set of one, so checks overfit.
- Mixing seeds without recording which produced the subject.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Character consistency across generated images is a dominant 2026 image-model request in public discussion; this is a dated signal, not an adoption metric.

## Related
- style-reference-image-generation.md
- image-generation.md
- perceptual-image-hashing.md
