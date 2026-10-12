---
name: feedback-delivery
description: Deliver critique so the recipient can act on it — observed behavior, concrete impact, and a specific request, separated from judgment of the person.
metadata:
  source: skills/06-communication/feedback-delivery.md
  category: 06-communication
  version: "v1"
---

# Feedback Delivery

Category: Communication | Level: basic | Stability: experimental | Version: v1

## Description

Feedback fails in two directions: it is so soft the recipient misses the point, or so blunt the recipient defends instead of acting. This skill holds the message to three separable parts — what was observed, what it caused, and what change is requested — and refuses to mix them with verdicts about the person. The test of good feedback is not how it feels in the moment; it is whether the next artifact observably changes.

## When to Use

Use when reviewing work product — code, writing, analysis, performance — in written reviews or in conversation.

Do not use feedback structure to smuggle in verdicts about people, and do not deliver critique when either party is depleted; timing is part of the message.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `observation` | `string` | Yes | The specific behavior or artifact observed |
| `impact` | `string` | Yes | The concrete effect of that behavior |
| `request` | `string` | Yes | The specific, checkable change proposed |

## Procedure

1. Ground in observation: quote the artifact or name the behavior before interpreting it.
2. State impact concretely: what follows from the behavior, for whom, measurably where possible.
3. Make the request specific and checkable — name a change a future reader could verify happened.
4. Keep person and artifact separate: critique the work, never the character or motives of the worker.
5. Check receipt: ask what the recipient heard, and correct drift before it hardens into grievance.
6. Close the loop: record what was agreed, and revisit it after the next instance of the same work.

## Outputs

| Output | Type | Description |
|---|---|---|
| `feedback` | `message` | Observation, impact, and request stated separately |
| `agreement` | `record` | What the recipient heard and committed to |

## Runnable Example

```python
def feedback(artifact, observation, impact, request):
    return {
        "artifact": artifact,
        "observation": observation,
        "impact": impact,
        "request": request,
    }

note = feedback(
    "pull request 512",
    "the test suite is skipped in CI",
    "regressions can reach main undetected",
    "run the suite on every push",
)
for part, text in note.items():
    print(f"{part}: {text}")
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Verdict without evidence | A judgment with no citable observation | Quote the artifact before interpreting |
| Vague requests | A change request nobody could verify | Ask for something a future reader can check |
| Character leakage | Critique slides from the work to the person | Critique the artifact, never the person |
| Sandwich dilution | Praise wrapped around critique disguises the point | Deliver recognition and critique separately |
| Drive-by timing | Delivered when the recipient cannot absorb it | Pick a moment both parties can engage |

## Security and Authority Boundary

Review feedback can surface sensitive detail: findings about security flaws belong in channels scoped to the trust of the recipient, with exploitable specifics kept out of open threads until a fix or a disclosure decision is made.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of feedback (https://en.wikipedia.org/wiki/Feedback).
2. Wikipedia's overview of 360-degree feedback (https://en.wikipedia.org/wiki/360-degree_feedback).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Debate](debate.md) — structured argument when positions must be contested.
- [Argument Construction](argument-construction.md) — building claims that survive challenge.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
