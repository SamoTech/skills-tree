---
title: "Singing Transcription"
category: 08-multimodal
level: advanced
stability: experimental
description: "Transcribe sung audio into note-level pitch, timing, and lyric alignment with syllable checks and confidence gating per note."
added: "2026-10"
version: v1
related: [music-stem-separation, audio-transcription, audio-diarization]
tags: [music, transcription, audio]
---

# Singing Transcription

## Description
Transcribe sung audio into note-level pitch, timing, and lyric alignment with syllable checks and confidence gating per note. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- sung audio must be converted into aligned notes and lyrics.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for singing transcription work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the singing transcription steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def align(notes, syllables):
    if len(notes) != len(syllables):
        return "length-mismatch"
    out = []
    for n, s in zip(notes, syllables):
        if n["conf"] < 0.6:
            return "low-confidence"
        out.append((n["pitch"], s))
    return out

notes = [{"pitch": 69, "conf": 0.9}, {"pitch": 71, "conf": 0.9}]
assert align(notes, ["la", "la"]) == [(69, "la"), (71, "la")]
```

## Failure Modes
- Aligning lyrics to notes without syllable counts.
- Exporting notes below the confidence gate.
- Missing melisma so one note carries many syllables.
- Ignoring vibrato as separate notes.
- No tuning reference so pitches are off by constants.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Singing transcription tooling is a recurring 2026 music-AI request in public coverage; this is a dated signal, not an adoption metric.

## Related
- music-stem-separation.md
- audio-transcription.md
- audio-diarization.md
