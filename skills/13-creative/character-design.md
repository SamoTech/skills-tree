---
title: "Character Design"
category: 13-creative
level: basic
stability: experimental
description: "Build fictional characters as explicit profiles — voice, motivation, capability, limits — with mechanically checkable arc beats so characters stay consistent and their growth is deliberate."
added: "2026-10"
version: v1
related: ["avatar-design", "creative-writing"]
---

# Character Design

Category: Creative | Level: basic | Stability: experimental | Version: v1

## Description

A character is a contract with the reader: the way they speak, what they want, what they cannot do. Breaking that contract by convenience is how stories lose trust. This skill defines a character as a structured profile — identity, motivation, capabilities with explicit limits, and voice rules — plus a beat sheet for their arc, so consistency is checkable against a record instead of remembered vibes.

## When to Use

Use when introducing a recurring character into any narrative work — prose, games, scripts — whose behavior must stay consistent across scenes and writers.

Do not use for background figures who appear once; a full profile for a walk-on role is overhead.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `profile` | `map[field -> value]` | Yes | Identity, motivation, capabilities, and limits |
| `arc` | `list[(beat, scene)]` | Yes | Planned arc beats in story order |
| `required_beats` | `list[beat]` | No | Beat types the arc must contain |

## Procedure

1. Write the profile before the character acts: motivation, capability set with explicit limits, and voice rules with examples.
2. State what the character cannot do; limits are what make capability meaningful.
3. Plan the arc as an ordered beat list and check it contains the required beat types before writing.
4. Check every written scene against the profile; out-of-character action requires either a new beat that earns it or a profile revision.
5. Keep the profile versioned with the work so any scene can be traced to the character state it assumed.
6. Give each distinct character a distinguishable voice rule set; interchangeable voices are a design failure.

## Outputs

| Output | Type | Description |
|---|---|---|
| `profile` | `map[field -> value]` | The recorded character profile |
| `missing_beats` | `list[beat]` | Required arc beats not yet planned |

## Runnable Example

```python
def arc_missing(beats, required):
    """Report required beat types absent from the planned arc."""
    present = {beat for beat, _scene in beats}
    return [stage for stage in required if stage not in present]

beats = [("introduction", "the village gate"), ("desire", "joining the guild"),
         ("loss", "the night fire"), ("change", "the road home")]
required = ["introduction", "desire", "loss", "change"]
print("missing beats:", arc_missing(beats, required))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Out-of-character action | Scene convenience overrides the profile | Check scenes against the profile or revise it deliberately |
| Missing arc stages | Key beats skipped in planning | Check required beats before writing the arc |
| Interchangeable voices | All characters speak alike | Write and test a distinct voice rule per character |
| Capability inflation | Limits quietly dropped under plot pressure | Restate limits in the profile and enforce them |
| Stale profiles | Character grows but the record does not | Version the profile with each earned change |

## Security and Authority Boundary

Characters borrowed from real people or cultures carry real obligations. Design with researched respect, avoid caricature, and keep provenance notes so borrowed elements are used with attribution and consent where applicable.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s overview of characterization (https://en.wikipedia.org/wiki/Characterization).
2. Wikipedia’s overview of the character arc (https://en.wikipedia.org/wiki/Character_arc).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Avatar Design](avatar-design.md) — the visual counterpart that must agree with this profile’s identity.
- [Creative Writing](creative-writing.md) — the prose execution that writes scenes against this record.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
