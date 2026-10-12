---
name: audio-mixing
description: Blend multiple PCM audio tracks under explicit gain envelopes with sample-accurate summation, hard clipping bounds, and a measured output peak so a mix is reproducible and cannot silently exceed the output range.
metadata:
  source: skills/08-multimodal/audio-mixing.md
  category: 08-multimodal
  version: "v1"
---

# Audio Mixing

Category: Multimodal | Level: intermediate | Stability: experimental | Version: v1

## Description

Mixing becomes destructive the moment gain is improvised: summed samples clip, quiet tracks get buried, and the result varies run to run. This skill treats a mix as an explicit contract — per-track gains, optional timed envelopes, a declared clip limit, and a measured peak — so the output is byte-reproducible from its inputs. It operates on in-memory PCM sample lists; codec-level or streaming mixdowns are out of scope.

## When to Use

Use when combining two or more recorded or synthesized mono PCM tracks into one output track where loudness behavior and clipping must be decided by policy rather than by accident.

Do not use for real-time streaming mixdowns or codec-domain processing; apply this contract after decoding, on sample data.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `tracks` | `list[PCM samples]` | Yes | Two or more mono sample lists at identical length basis |
| `gains` | `list[number]` | Yes | One fixed gain multiplier per track, declared before summation |
| `clip_limit` | `integer` | Yes | Hard output bound, e.g. 32767 for 16-bit audio |
| `envelope` | `list[(time, gain)]` | No | Timed gain points applied per track before summation |

## Procedure

1. Declare every track gain and the clip limit before the first sample is summed; mixing with undeclared gains is rejected.
2. Verify all tracks share a sample rate and channel layout; resample or reject before mixing, never inside it.
3. Apply each track’s gain (and optional timed envelope) sample by sample, in a fixed track order.
4. Sum tracks sample-accurately in integer domain so the result is identical across runs and platforms.
5. Clip each summed sample to the declared limit and count clipped samples as a quality signal.
6. Measure the output peak after mixing; an unmeasured mix cannot be compared or improved.
7. Record the gain set, envelope, clip count, and peak alongside the output so the mix is reproducible.
8. Re-mix rather than normalize after the fact when the clip count is nonzero; clipping already destroyed information.

## Outputs

| Output | Type | Description |
|---|---|---|
| `mixed` | `list[samples]` | The clipped, summed output track |
| `peak` | `integer` | Largest absolute sample value in the output |
| `clipped_samples` | `integer` | Number of samples bounded by the clip limit |

## Runnable Example

```python
def mix_tracks(tracks, gains, clip_limit):
    """Mix PCM tracks with fixed per-track gains and hard clipping."""
    length = max(len(t) for t in tracks)
    mixed = [0] * length
    for track, gain in zip(tracks, gains):
        for i, sample in enumerate(track):
            mixed[i] += int(sample * gain)
    clipped = 0
    for i, total in enumerate(mixed):
        if total > clip_limit:
            mixed[i] = clip_limit
            clipped += 1
        elif total < -clip_limit:
            mixed[i] = -clip_limit
            clipped += 1
    peak = max(abs(s) for s in mixed)
    return mixed, peak, clipped

tracks = [[10000, -4000, 6000], [24000, 0, -9000]]
gains = [0.5, 0.75]
mixed, peak, clipped = mix_tracks(tracks, gains, clip_limit=16000)
print(mixed)
print("peak:", peak, "clipped:", clipped)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Clipping distortion | Summed samples exceed the output range | Declare a clip limit up front and count clipped samples |
| Buried quiet tracks | Gains improvised per mix | Fix the gain set before summation and record it with the output |
| Rate mismatch | Tracks mixed at different sample rates | Verify a shared rate before mixing; resample or reject |
| Non-reproducible mix | Float ordering and undeclared gains vary | Sum in a fixed track order with declared gains |
| Unmeasured output | Peak level never computed | Measure and record peak and clip count with every mix |

## Security and Authority Boundary

Mixing grants no authority over source recordings. Source material keeps its license and consent state; a mix does not launder restricted audio into usable output. Output loudness is a technical measurement, not a safety claim.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s overview of audio mixing practice (https://en.wikipedia.org/wiki/Audio_mixing_(recorded_music)).
2. Python’s wave module documentation for reading and writing PCM files (https://docs.python.org/3/library/wave.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Audio Classification](audio-classification.md) — labels tracks before mixing so per-track policy can be applied.
- [Text to Speech](text-to-speech.md) — a common synthesized source track that follows this mixing contract downstream.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
