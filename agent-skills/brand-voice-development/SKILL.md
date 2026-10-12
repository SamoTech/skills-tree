---
name: brand-voice-development
description: Define a reusable brand voice from values and audience, specifying tone dimensions, vocabulary rules, and example rewrites so all writers sound like one consistent speaker.
metadata:
  source: skills/13-creative/brand-voice-development.md
  category: 13-creative
  version: "v1"
---

# Brand Voice Development

Category: Creative | Level: intermediate | Stability: experimental | Version: v1

## Description

A brand voice is a small set of decisions applied consistently, not a mood board. The skill covers extracting voice traits from brand values, defining each trait as a position on a tone axis with do-and-never examples, writing vocabulary and punctuation rules, and validating drafts by rewriting the same sample in the defined voice. A voice is done when an unfamiliar writer can apply the spec and pass a blind consistency check.

## When to Use

Use when an organization needs its writing to sound consistent across channels, writers, and formats, from support replies to marketing copy.

Do not describe the voice only with adjectives such as friendly and bold. Without axis positions, vocabulary rules, and contrast examples, every writer interpolates differently.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `brand_brief` | `object` | Yes | Brand values, positioning, and audience definition |
| `samples` | `text` | No | Existing writing the voice should preserve or correct |
| `channels` | `list` | No | Channel-specific tone adjustments, keyed by channel |

## Procedure

1. Extract candidate voice traits from brand values and the audience relationship.
2. Reduce the traits to three to five axes and pick a position on each, with rationale.
3. Write do-and-never examples per trait so contrast is explicit, not implied.
4. Define vocabulary rules: preferred terms, banned terms, and grammar choices.
5. Rewrite one canonical sample passage in the new voice and annotate every change.
6. Run a blind consistency check with an unfamiliar writer before publishing the spec.

## Outputs

| Output | Type | Description |
|---|---|---|
| `voice_spec` | `object` | Trait axes, positions, and rules, machine-referenced per piece |
| `example_set` | `array` | Before-and-after pairs demonstrating each trait |
| `channel_overrides` | `object` | Per-channel tone adjustments that preserve the traits |

## Runnable Example

```python
def voice_consistency_scores(drafts, spec):
    """drafts: {writer: {trait: position}}; spec: {trait: position}"""
    scores = {}
    for writer, traits in drafts.items():
        deltas = [abs(traits[t] - spec[t]) for t in spec if t in traits]
        scores[writer] = round(1 - sum(deltas) / (len(deltas) * 4), 2) if deltas else None
    return scores

print(voice_consistency_scores(
    {"writer-a": {"formality": -2, "playfulness": 1}, "writer-b": {"formality": 1, "playfulness": 3}},
    {"formality": -2, "playfulness": 2},
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Trait soup | Too many traits for writers to hold in mind | Cut to three to five axes |
| Inconsistent across channels | One static tone applied everywhere | Define channel overrides that preserve traits |
| Drift over time | No validation loop after the spec ships | Re-run consistency checks on live copy periodically |
| Adjectives only | No axis positions or contrast examples | Require do-and-never pairs per trait |
| Voice copies a competitor | Samples over-weighted toward external material | Anchor in the brand brief, not imitation |

## Security and Authority Boundary

A voice spec encodes how an organization speaks and is a reputational asset. Keep positioning and unreleased campaign strategy confidential, and ensure the voice never overrides accuracy or legal disclosure requirements in regulated content.

## Evidence

This skill is grounded in dated public implementation references:

1. The Microsoft Writing Style Guide as a public voice and style reference (https://learn.microsoft.com/en-us/style-guide/).
2. The Google developer documentation style guide (https://developers.google.com/style).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Copywriting](copywriting.md) — the short-form craft where voice rules are most visible.
- [Tone Adjustment](../06-communication/tone-adjustment.md) — the per-message modulation that keeps one voice across situations.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
