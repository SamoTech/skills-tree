---
title: "On Screen Agent Annotation Overlay"
category: 10-computer-use
level: advanced
stability: experimental
description: "Render agent attention as on-screen annotations such as arrows, boxes, and labels so a human can see which region an agent is acting on."
added: "2026-10"
version: v1
related: [voice-hold-to-talk-agent-control]
tags: [overlays, annotation, computer-use, visibility]
---
# On Screen Agent Annotation Overlay

## Description
Render agent attention as on-screen annotations such as arrows, boxes, and labels so a human can see which region an agent is acting on. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent acts on regions of a shared screen and its target must be visible to the human operator during the action.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Compute the target region from the agent’s action, render a bounded overlay identifying it, and record the overlay with the action so later review can reconstruct what the agent pointed at.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def overlay(action, region):
    return {"label": action, "region": region, "dismissable": True}
o = overlay("clicking-submit", [10, 20, 30, 40])
assert o["region"] == [10, 20, 30, 40] and o["dismissable"]
```

## Failure Modes
- The overlay is shown but never recorded with the action it annotated.
- Regions go stale after scrolling and point at the wrong place.
- The overlay blocks interaction with the element it marks.
- Multiple agents annotate the same screen without labels distinguishing them.
- There is no dismissal path for a stuck overlay.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Big Arrow on the Screen tool letting AI agents draw large arrows, boxes, and text directly on top of the screen (useaitools.me late October 2026 roundup, dated October 31, 2026) ([public signal](https://useaitools.me/blog/new-ai-tools-late-october-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Voice Hold To Talk Agent Control](voice-hold-to-talk-agent-control.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
