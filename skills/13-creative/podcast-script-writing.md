---
title: "Podcast Script Writing"
category: 13-creative
level: basic
stability: experimental
description: "Write podcast scripts and episode outlines with cold opens, segments, host cues, and ad placements, tuned to time targets and speaker-friendly rhythm."
added: "2026-10"
version: v1
related: ["copywriting","dialogue-writing"]
---

# Podcast Script Writing

Category: Creative | Level: basic | Stability: experimental | Version: v1

## Description

A podcast script must sound spoken, not read. The skill covers structuring an episode as a cold open, segments with time boxes, and an outro; writing for the ear with short sentences and explicit host cues; placing transitions and ad reads at natural seams; and marking every line with a time estimate so the episode hits its target duration. Speaker difficulty is checked by reading cadence, not word count alone.

## When to Use

Use when an audio episode needs a script or a tight outline: narrative shows, interview prep, news digests, or branded series with required segments.

Do not deliver a text meant for silent reading. If a sentence cannot be spoken in one breath or loses meaning when heard once, rewrite it.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `episode_brief` | `object` | Yes | Topic, audience, target duration, and required segments |
| `research` | `text` | Yes | Source material and facts the episode must present |
| `duration_target` | `int` | No | Target length in minutes; drives the time budget per segment |

## Procedure

1. Break the brief into a cold open, ordered segments, and an outro with a time budget each.
2. Verify every factual claim in the research material and mark attributed claims.
3. Write spoken-style lines: short sentences, contractions, and explicit host cues.
4. Insert transitions and ad placements at segment seams only, never mid-argument.
5. Estimate speaking time per block at a fixed words-per-minute rate and rebalance the budget.
6. Read-check the script for breath length, tongue twisters, and lines that only work on paper.

## Outputs

| Output | Type | Description |
|---|---|---|
| `script` | `text` | Full spoken script with host cues and timing marks |
| `segment_plan` | `array` | Segments with time budgets and transition types |
| `fact_log` | `list` | Claims with their source status for verification |

## Runnable Example

```python
def budget_segments(total_minutes, segments, wpm=150):
    """segments: [(name, share)] summing to 1.0"""
    out = []
    for name, share in segments:
        words = int(total_minutes * share * wpm)
        out.append({"segment": name, "minutes": round(total_minutes * share, 1), "word_budget": words})
    return out

print(budget_segments(20, [("cold-open", 0.1), ("story", 0.5), ("interview", 0.3), ("outro", 0.1)]))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Reads as written prose | Long sentences and subordination built for the eye | Apply breath-length checks and rewrite |
| Overtime or underfilled | No time budget per segment | Budget words per segment at a fixed rate |
| Ad breaks mid-argument | Placement not at a seam | Allow transitions only at segment boundaries |
| Unsupported claims aired | Research not verified before scripting | Fact-log every claim with source status |
| Flat segment pacing | Uniform rhythm across the whole episode | Vary energy: open high, breathe mid, land the outro |

## Security and Authority Boundary

Podcast scripts carry legal exposure: defamation risk from unverified claims, and licensing risk from quoted material. Attribute contested claims, keep the fact log with the script, and do not read sponsor copy beyond the approved disclosure.

## Evidence

This skill is grounded in dated public implementation references:

1. The Wikipedia article on podcasts as a medium (https://en.wikipedia.org/wiki/Podcast).
2. The Podlove open-source podcast publishing project (https://github.com/podlove/podlove-podcast-publisher).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Copywriting](copywriting.md) — the short-form persuasion craft used in cold opens and sponsor reads.
- [Dialogue Writing](dialogue-writing.md) — the spoken-interaction patterns that keep host lines natural.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
