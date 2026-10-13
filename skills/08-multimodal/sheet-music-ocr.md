---
title: "Sheet Music OCR"
category: 08-multimodal
level: advanced
stability: experimental
description: "Recognize printed sheet music into structured notation with symbol validation, key-signature checks, and pitch-range verification before export to symbolic formats."
added: "2026-10"
version: v1
related: [document-layout-analysis, image-captioning, audio-transcription]
tags: [music, ocr, documents]
---

# Sheet Music OCR

## Description
Recognize printed sheet music into structured notation with symbol validation, key-signature checks, and pitch-range verification before export to symbolic formats. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- printed sheet music must be converted into a machine-readable symbolic score.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for sheet music ocr work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the sheet music ocr steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def validate_bars(bars, expected):
    problems = []
    for i, b in enumerate(bars):
        if b["duration"] != expected:
            problems.append(f"bar-{i}-duration")
        for n in b["notes"]:
            if not 21 <= n <= 108:
                problems.append(f"bar-{i}-pitch")
    return problems

bars = [{"duration": 4.0, "notes": [60]}, {"duration": 3.0, "notes": [60]}]
assert validate_bars(bars, 4.0) == ["bar-1-duration"]
```

## Failure Modes
- Exporting without bar-duration validation.
- Ignoring the key signature and producing wrong accidentals.
- No staff-assignment check so clefs are swapped.
- Treating unrecognized symbols as silence.
- No confidence review of low-quality scans.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Symbolic music extraction is a recurring 2026 document-AI request in public coverage; this is a dated signal, not an adoption metric.

## Related
- document-layout-analysis.md
- image-captioning.md
- audio-transcription.md
