---
name: plot-structure
description: Organize a story into declared structural acts with positioned beats so pacing, reversals, and climaxes land where the chosen form requires and deviations are deliberate.
metadata:
  source: skills/13-creative/plot-structure.md
  category: 13-creative
  version: "v1"
---

# Plot Structure

Category: Creative | Level: basic | Stability: experimental | Version: v1

## Description

Structure is the load-bearing frame a story hangs from: acts, beats, and their positions. Without declared positions, a “slow second act” is a feeling; with them, it is a measurable gap between the inciting event and the midpoint. This skill defines plot structure as a table — beats named, positioned on a 0–100 scale, and assigned to declared acts — so the shape is visible and every deviation is a decision.

## When to Use

Use when planning or diagnosing a story’s shape — novels, screenplays, episodes — before or during drafting, or when a draft feels structurally off.

Do not use to impose structure on completed work by force; if a story resists the chosen form, change forms deliberately rather than mangle the story.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `beats` | `list[(label, position)]` | Yes | Story beats with positions on a 0–100 scale |
| `acts` | `list[(name, start, end)]` | Yes | Declared act boundaries on the same scale |
| `required_beats` | `list[label]` | No | Beats the chosen form mandates |

## Procedure

1. Choose the structural form first and declare its act boundaries on a normalized 0–100 scale.
2. Position each beat on the same scale; relative position is the contract, not chapter count.
3. Check that every beat falls inside exactly one act; boundary orphans indicate scale drift.
4. Check the form’s required beats are present and positioned within their expected ranges.
5. Report structural gaps — long stretches with no beat — as measurable intervals, not impressions.
6. Revise positions on evidence when pacing is off; the table is the plan of record.

## Outputs

| Output | Type | Description |
|---|---|---|
| `assignments` | `list[(label, position, act)]` | Beats mapped to their acts |
| `orphans` | `list[label]` | Beats outside every declared act |
| `gaps` | `list[(start, end)]` | Unusually long beat-free intervals |

## Runnable Example

```python
def assign_acts(beats, acts):
    """Map positioned beats into declared act boundaries."""
    result = []
    for label, position in beats:
        act = next((name for name, start, end in acts if start <= position <= end), None)
        result.append((label, position, act))
    return result

beats = [("inciting event", 12), ("midpoint reversal", 50), ("all-is-lost", 68), ("climax", 88)]
acts = [("act 1", 0, 30), ("act 2", 31, 75), ("act 3", 76, 100)]
for label, position, act in assign_acts(beats, acts):
    print(f"{position:3d}  {act or 'orphan':7s}  {label}")
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Act drift | Beats straddle declared boundaries | Normalize positions to one scale and reassign |
| Missing mandatory beats | The chosen form’s obligations unmet | Check required beats against the declared form |
| Unmeasured pacing | “Slow” sections felt but not located | Report beat-free intervals as numbers |
| Form mismatch | Story forced into an unsuitable structure | Choose the form from the story, not habit |
| Stale plan | Draft diverges from the structural table | Keep the table current or admit it is abandoned |

## Security and Authority Boundary

Structure tools shape creative output but claim no ownership; a structural template is scaffolding, and the finished work inherits only the licenses of its actual sources.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s overview of the three-act structure (https://en.wikipedia.org/wiki/Three-act_structure).
2. Wikipedia’s overview of dramatic structure (https://en.wikipedia.org/wiki/Dramatic_structure).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Creative Writing](creative-writing.md) — the drafting craft that executes against this structural table.
- [Video Script](video-script.md) — a timed medium where positions map to minutes, not chapters.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
