---
name: dialogue-writing
description: Write character dialogue with explicit speaker turns, subtext layers, and mechanical exchange checks so conversations stay consistent, purposeful, and attributable line by line.
metadata:
  source: skills/13-creative/dialogue-writing.md
  category: 13-creative
  version: "v1"
---

# Dialogue Writing

Category: Creative | Level: basic | Stability: experimental | Version: v1

## Description

Dialogue has mechanics and meaning: every line belongs to a speaker, turns should not blur into monologue by accident, and what a character says should rarely be exactly what they mean. This skill treats dialogue as structured data — (speaker, text) turns with optional subtext — plus checks for alternation, tagging, and emptiness, so the craft decisions sit on a verifiable exchange structure.

## When to Use

Use when writing scenes of two or more voices where speaker attribution and turn structure must stay clean — prose, scripts, or interactive fiction.

Do not use for interior monologue; unattributed thought is not dialogue and follows different rules.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `lines` | `list[(speaker, text)]` | Yes | Dialogue turns in order with explicit speakers |
| `subtext` | `map[line -> meaning]` | No | Intended unstated meaning per line |
| `voices` | `map[speaker -> rules]` | No | Per-speaker voice constraints |

## Procedure

1. Write every line as an explicit (speaker, text) turn; unattributed lines are a structural defect, not a style.
2. Run the exchange checks before polishing prose: same-speaker runs must be intentional, empty lines removed.
3. Give each line a purpose — information, pressure, or relationship change — and cut lines with none.
4. Set the subtext deliberately; when text equals meaning, that sameness should be the decision, not the default.
5. Read voices against their speaker rules; a line that fits no voice is a draft error.
6. Keep the exchange table with the draft so revisions do not silently drop speakers or turns.

## Outputs

| Output | Type | Description |
|---|---|---|
| `scene` | `list[(speaker, text)]` | The checked, ordered exchange |
| `issues` | `list[(line_index, kind)]` | Structural problems found by the checks |

## Runnable Example

```python
def check_exchange(lines):
    """Report accidental same-speaker runs and empty turns."""
    issues = []
    previous = None
    for i, (speaker, text) in enumerate(lines, 1):
        if not text.strip():
            issues.append((i, "empty line"))
        if speaker == previous:
            issues.append((i, "same speaker twice in a row"))
        previous = speaker
    return issues

scene = [("mara", "You came back."), ("joss", "I never left."),
         ("joss", "You knew that."), ("mara", "I hoped.")]
for issue in check_exchange(scene):
    print(issue)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Speaker blur | Turns run together without clear attribution | Tag every line and run the alternation check |
| Talking heads | Exchange carries no scene purpose | Give each line information, pressure, or change |
| Flat text | Characters say exactly what they mean | Set subtext deliberately per line |
| Voice bleed | All characters speak with one voice | Write per-speaker voice rules and check against them |
| Unversioned drafts | Revisions drop turns silently | Keep the exchange table with the draft |

## Security and Authority Boundary

Dialogue written in real people’s voices — impressions of living individuals — carries defamation and dignity risks. Fictional voices should stay fictional, and borrowed real-world dialect deserves researched respect.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s overview of dialogue in narrative (https://en.wikipedia.org/wiki/Dialogue).
2. Wikipedia’s overview of fiction as a narrative form (https://en.wikipedia.org/wiki/Fiction).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Creative Writing](creative-writing.md) — the prose craft that surrounds these structured exchanges.
- [Social Media Post](social-media-post.md) — short-form voice writing governed by the same consistency discipline.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
