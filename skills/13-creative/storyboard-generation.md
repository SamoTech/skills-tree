---
title: "Storyboard Generation"
category: 13-creative
level: basic
stability: experimental
description: "Produce shot-by-shot storyboards from scripts or scene descriptions, specifying framing, camera movement, transitions, and visual continuity for production review."
added: "2026-10"
version: v1
related: ["video-script","plot-structure"]
---

# Storyboard Generation

Category: Creative | Level: basic | Stability: experimental | Version: v1

## Description

A storyboard is the contract between a script and a shoot. The skill covers decomposing a script into shots, choosing framing and camera movement per shot, writing panel descriptions that a reviewer can verify against the script, and maintaining continuity of position, time, and screen direction across panels. Output is a numbered panel sequence with explicit per-panel specs, not prose.

## When to Use

Use when a script, scene, or campaign concept must be visualized as a shot sequence for review before expensive production or animation begins.

Do not generate decorative single images and call them a storyboard. A storyboard is a numbered sequence whose continuity and screen direction can be checked panel by panel.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `script` | `text` | Yes | Scene text or shot list to visualize |
| `style` | `object` | No | Visual style guide for panel rendering |
| `detail` | `enum` | No | `shot-level` (default) or `beat-level` granularity |

## Procedure

1. Break the script into shots; each shot gets one panel with a unique number.
2. For each panel, specify framing, camera movement, subject blocking, and screen direction.
3. Write a one-to-two sentence panel description that a reviewer can verify against the script.
4. Check continuity across panels: position, time of day, costume, and screen direction.
5. Mark transitions between panels: cut, dissolve, or move, stated explicitly.
6. Assemble the sequence with dialogue or action captions and export for review.

## Outputs

| Output | Type | Description |
|---|---|---|
| `panels` | `array` | Numbered panel specs with framing, movement, and description |
| `continuity_notes` | `list` | Cross-panel continuity checks and any flagged breaks |
| `transition_map` | `list` | Transitions between consecutive panels |

## Runnable Example

```python
def check_screen_direction(panels):
    """panels: [(number, subject_x)] left-to-right positions"""
    issues = []
    for i in range(1, len(panels)):
        prev, cur = panels[i - 1], panels[i]
        if cur[1] < prev[1] and abs(cur[1] - prev[1]) > 50:
            issues.append({"between": [prev[0], cur[0]], "rule": "180-degree line crossed"})
    return {"panels": len(panels), "issues": issues}

print(check_screen_direction([(1, 120), (2, 200), (3, 40)]))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Continuity breaks | Position or costume changes between adjacent panels | Run continuity checks before review |
| Screen direction flips | 180-degree line crossed mid-scene | Fix blocking or insert a neutral panel |
| Decorative drift | Panels look good but match no script line | Require a verifiable script reference per panel |
| Shot overload | Every line becomes a new shot | Consolidate to shot-level unless beats are requested |
| Unspecified transitions | Panel joins left ambiguous | State cut, dissolve, or move explicitly |

## Security and Authority Boundary

Storyboards can embed real people, brands, or locations from the source material. Do not render identifiable individuals without permission, keep campaign material confidential until approved, and check generated panels for content that leaks unreleased plot or product details.

## Evidence

This skill is grounded in dated public implementation references:

1. The Storyboarder open-source storyboarding tool (https://github.com/wonderunit/storyboarder).
2. The Wikipedia article on storyboards (https://en.wikipedia.org/wiki/Storyboard).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Video Script](video-script.md) — the upstream script that defines the shots being boarded.
- [Plot Structure](plot-structure.md) — the narrative skeleton that shot ordering must serve.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
