---
title: "App Foreground Action Requirements"
category: 10-computer-use
level: advanced
stability: experimental
description: "Detect which desktop actions require their target application to be in the foreground and schedule them so the user keeps working without silent failures."
added: "2026-11"
version: v1
related: [local-desktop-agent-team-execution, app-foreground-action-requirements]
tags: [foreground, scheduling, desktop-automation, computer-use]
---
# App Foreground Action Requirements

## Description
Detect which desktop actions require their target application to be in the foreground and schedule them so the user keeps working without silent failures. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent operates desktop apps in the background and some actions quietly fail or misfire because the app was never brought forward.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the action inventory, the per-app foreground requirement flags, and the user's active-work check. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Tag every desktop action with whether its app must be foreground for it to succeed.
2. Batch the background-safe actions and execute them without touching focus.
3. Queue foreground-required actions and check whether the user is actively working.
4. Ask or schedule before bringing an app forward, and never steal focus mid-action.
5. On a foreground action that still failed, fail closed with the app state preserved.
6. Emit a structured result with the action log, foreground decisions, and outcomes.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def schedule(actions, user_busy):
    bg = [a for a in actions if not a["needs_foreground"]]
    fg = [a for a in actions if a["needs_foreground"]]
    plan = {"run_now": bg, "queued": fg, "ask": bool(fg) and user_busy}
    return plan
acts = [{"n": "read_doc", "needs_foreground": False}, {"n": "click_menu", "needs_foreground": True}]
p = schedule(acts, True)
assert p["run_now"] == [{"n": "read_doc", "needs_foreground": False}] and p["ask"] is True
assert schedule(acts, False)["ask"] is False
```

## Failure Modes
- Foreground-required actions run in the background and fail without an error surfaced.
- Focus is stolen mid-action and the user's keystrokes land in the automated app.
- Foreground flags are guessed per app and never verified against real runs.
- Queued foreground actions run in a burst when the user returns, flooding the apps.
- A failed foreground action is retried without checking why it failed.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Orca 1.4.245 letting agents work in Chrome, Blender, and other apps on a Mac while the user keeps using the mouse and keyboard, though some actions still need the app brought forward (Munder Difflin agent-tools daily, dated November 1, 2026) ([public signal](https://munderdiffl.in/blog/agent-tools-today-2026-11-01/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Local Desktop Agent Team Execution](local-desktop-agent-team-execution.md)
- [App Foreground Action Requirements](app-foreground-action-requirements.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
