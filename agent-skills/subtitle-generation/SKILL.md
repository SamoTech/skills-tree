---
name: subtitle-generation
description: Build well-formed WebVTT subtitle cues from timestamped transcript segments with monotonic ordering, overlap detection, and exact timestamp formatting so captions render correctly and validate mechanically.
metadata:
  source: skills/08-multimodal/subtitle-generation.md
  category: 08-multimodal
  version: "v1"
---

# Subtitle Generation

Category: Multimodal | Level: intermediate | Stability: experimental | Version: v1

## Description

A caption file is a format contract: cue timestamps must be ordered, non-overlapping, and formatted to the millisecond, or players drop or smear cues. This skill turns timestamped segments into a validated WebVTT payload — exact formatting, overlap detection, and a deterministic builder that never emits an invalid cue. Content quality of the translation itself is out of scope; this is the timing-and-format contract.

## When to Use

Use when transcript segments with start and end times must become a caption track that players and validators accept as-is.

Do not use to align audio to text from scratch; alignment belongs to transcription tooling, and this skill consumes its timestamped output.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `segments` | `list[(start, end, text)]` | Yes | Timestamped transcript segments in seconds |
| `max_cue_duration` | `number` | No | Longest single cue allowed before splitting |
| `max_chars` | `integer` | No | Per-cue character cap applied by re-segmentation |

## Procedure

1. Format every timestamp as HH:MM:SS.mmm computed from seconds with integer millisecond rounding.
2. Reject any segment whose end precedes or equals its start; malformed timing never reaches the output.
3. Detect overlaps between consecutive cues and fail closed instead of silently emitting both.
4. Split cues exceeding the duration or character caps before formatting, in reading order.
5. Emit cues in a fixed order: header once, then timing line, text, blank separator per cue.
6. Round-trip the payload: re-parse the emitted cues and assert the turn count and ordering match the input.
7. Keep the builder deterministic — identical segments produce byte-identical output.

## Outputs

| Output | Type | Description |
|---|---|---|
| `vtt` | `string` | The complete WebVTT payload with header and cues |
| `cue_count` | `integer` | Number of cues emitted |
| `violations` | `list[string]` | Input segments rejected for timing or overlap reasons |

## Runnable Example

```python
def format_timestamp(seconds):
    millis = int(round(seconds * 1000))
    h, rem = divmod(millis, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

def build_vtt(segments):
    cues = ["WEBVTT", ""]
    for start, end, text in segments:
        if end <= start:
            raise ValueError(f"invalid cue timing: {start}..{end}")
        cues.append(f"{format_timestamp(start)} --> {format_timestamp(end)}")
        cues.append(text)
        cues.append("")
    return "\n".join(cues).rstrip() + "\n"

segments = [(1.5, 3.0, "hello"), (3.2, 4.75, "world")]
print(build_vtt(segments))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Overlapping cues | Segments overlap after alignment | Detect overlaps and fail closed or split on evidence |
| Smearing timestamps | Floating-point drift in formatting | Round to integer milliseconds from seconds |
| Zero-length cue | End time not after start | Reject malformed segments before emission |
| Player rejection | Missing blank line between cues | Emit the separator line after every cue |
| Silent split drift | Long cues exceed player caps | Apply duration and character caps deterministically |

## Security and Authority Boundary

Caption generation processes potentially private spoken content. The payload inherits the source recording’s disclosure state; rendering or publishing captions grants no new authority over the underlying media.

## Evidence

This skill is grounded in dated public implementation references:

1. The W3C WebVTT specification defining cue timing and structure (https://www.w3.org/TR/webvtt1/).
2. Python’s datetime module documentation for time components (https://docs.python.org/3/library/datetime.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Video Description](video-description.md) — pairs visual narration with spoken captions for accessible playback.
- [Audio Transcription](audio-transcription.md) — produces the timestamped segments this skill formats into cues.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
