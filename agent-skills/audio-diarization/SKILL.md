---
name: audio-diarization
description: Segment an audio stream into who-spoke-when turns from frame-level acoustic evidence with deterministic boundary rules so speaker attribution yields explicit, testable segments.
metadata:
  source: skills/08-multimodal/audio-diarization.md
  category: 08-multimodal
  version: "v1"
---

# Audio Diarization

Category: Multimodal | Level: advanced | Stability: experimental | Version: v1

## Description

Speaker attribution is only as trustworthy as its segment boundaries. This skill builds diarization as a rule-bound pipeline: acoustic frames carry a speaker label, consecutive same-label frames merge into turns, and every turn records its speaker, start, and end. The merge rules are deterministic so the same frame sequence always produces the same turn list. Acoustic labeling itself is delegated to a classifier; this skill governs the segmentation contract.

## When to Use

Use when a transcript or analysis needs per-speaker attribution — meeting minutes, call analytics, or speaker-indexed search — and the output must be a reviewable turn list rather than a black-box label.

Do not use for raw transcription without speakers; apply the audio transcription skill instead, and diarize its alignment if per-speaker turns are needed.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `frames` | `list[(speaker, start, end)]` | Yes | Acoustic frames with inferred speaker labels, time-ordered |
| `min_turn` | `number` | No | Shortest turn duration kept; shorter turns are dropped |
| `unknown_label` | `string` | No | Label treated as no-speaker; frames with it are not merged |

## Procedure

1. Require frames to be sorted by start time before merging; unsorted input is rejected.
2. Merge a frame into the previous turn only when speaker labels match and boundaries are contiguous.
3. Start a new turn on any label change, gap, or boundary discontinuity; never merge across gaps.
4. Apply the minimum-turn rule after merging, dropping turns shorter than the declared floor.
5. Record each turn as (speaker, start, end) with an identifier stable across runs.
6. Expose a coverage metric: total speech time minus turn gaps, so silent regions are visible.
7. Treat classifier labels as evidence, not truth: keep the label confidence alongside each turn when available.

## Outputs

| Output | Type | Description |
|---|---|---|
| `turns` | `list[(speaker, start, end)]` | Ordered, non-overlapping speaker turns |
| `coverage` | `number` | Fraction of the stream covered by turns |
| `dropped` | `list[turn]` | Turns removed by the minimum-turn rule |

## Runnable Example

```python
def segment_turns(frames):
    """Merge contiguous same-speaker frames into (speaker, start, end) turns."""
    turns = []
    for speaker, start, end in frames:
        if turns and turns[-1][0] == speaker and turns[-1][2] == start:
            turns[-1] = (speaker, turns[-1][1], end)
        else:
            turns.append((speaker, start, end))
    return turns

frames = [("A", 0.0, 1.2), ("A", 1.2, 2.4), ("B", 2.4, 3.0), ("A", 3.0, 4.5)]
for turn in segment_turns(frames):
    print(turn)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Over-merge | Gap ignored between same-speaker frames | Merge only on contiguous boundaries |
| Under-merge | Rounding splits contiguous frames | Compare with tolerance and normalize timestamps first |
| Unstable labels | Classifier flickers between speakers | Smooth labels before merging and record confidence |
| Unsorted input | Frames arrive out of order | Validate sort order up front and reject violations |
| Silent regions hidden | Gaps never reported | Compute and expose coverage alongside turns |

## Security and Authority Boundary

Diarization output identifies who spoke when; treat it as personal data. It grants no authority to act on speakers and must respect the retention and consent rules of the source audio in every downstream store.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s survey of speaker diarisation (https://en.wikipedia.org/wiki/Speaker_diarisation).
2. Python’s wave module documentation for reading PCM audio fragments (https://docs.python.org/3/library/wave.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Audio Transcription](audio-transcription.md) — produces the word-level content this skill assigns to speakers.
- [Audio Classification](audio-classification.md) — supplies the frame labels the merge rules operate on.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
