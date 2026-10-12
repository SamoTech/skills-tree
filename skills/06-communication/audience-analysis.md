---
title: "Audience Analysis"
category: 06-communication
level: basic
stability: experimental
description: "Profile who will receive a message — their prior knowledge, stakes, and constraints — before deciding what to say and in what form to say it."
added: "2026-10"
version: v1
related: ["persona-adoption", "tone-adjustment"]
---

# Audience Analysis

Category: Communication | Level: basic | Stability: experimental | Version: v1

## Description

Most failed communication was written before anyone asked who would read it. This skill front-loads that question: name the audience precisely, establish what they already know and what is at stake for them, and let those facts decide depth, order, and channel. The profile constrains the wording, not the truth — it changes how something is said, never whether the substance gets stated.

## When to Use

Use before sending anything consequential to a group you cannot see — documentation, announcements, incident notices, decision requests.

Do not use the profile to stereotype individuals or to substitute imagined preferences for the purpose of the message; a profile guides wording, it does not license telling people only what they want to hear.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `message_purpose` | `string` | Yes | What the audience should know or do afterward |
| `audience` | `map` | Yes | Roles, prior knowledge, stakes, and constraints of the readers |
| `channels` | `list` | No | Where the message will arrive, with format constraints |

## Procedure

1. Name the audience precisely: "all users" is not an audience, while "first-time administrators configuring single sign-on" is.
2. Establish the baseline: what the reader already knows, so the message starts where they are rather than where the author wishes they were.
3. Establish the stakes: what changes for the reader if they act, and what changes if they do not.
4. Decide depth per segment — background, working detail, or decision summary — because one message cannot be all three at once.
5. Choose the channel and format each segment actually reads, and record constraints such as length limits or review requirements.
6. Revisit the profile when feedback arrives, because audiences drift and a stale profile misroutes everything built on it.

## Outputs

| Output | Type | Description |
|---|---|---|
| `profile` | `map` | Segments with baseline knowledge, stakes, and constraints |
| `message_plan` | `map` | Per-segment decisions on depth, order, and channel |

## Runnable Example

```python
def plan_for(segment):
    if not segment.get("knows"):
        return "start from zero context and define every term"
    if segment.get("stakes") == "decision":
        return "lead with the recommendation, then the reasoning"
    return "keep the shared vocabulary and keep the detail"

segments = [
    {"knows": [], "stakes": "daily use"},
    {"knows": ["rate limits"], "stakes": "decision"},
]
for segment in segments:
    print(plan_for(segment))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Assumed knowledge | Readers lack context the author took for granted | Start from the actual baseline of the audience |
| Self-reference | Message organized around the author instead of the reader | Reorder sections around reader stakes |
| Averaged audience | One compromise message serves no segment | Split by segment and depth |
| Stale profiles | The audience changed since the last analysis | Revalidate against observed feedback |
| Missing stakes | Readers cannot tell why it matters to them | State consequences for the reader early |

## Security and Authority Boundary

Audience analysis is a distribution decision, and distribution is a boundary: the segments a message will reach must feed directly into what it may contain, and no segment broader than the intended trust level of the content may be added as a recipient.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of audience analysis (https://en.wikipedia.org/wiki/Audience_analysis).
2. The PlainLanguage.gov guidelines on writing for the audience (https://www.plainlanguage.gov/guidelines/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Persona Adoption](persona-adoption.md) — simulating a specific reader to test a message.
- [Tone Adjustment](tone-adjustment.md) — matching register once the audience is known.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
