---
title: "Local LLM Virtual Desktop Control Operations"
category: 10-computer-use
level: advanced
stability: experimental
description: "Operate virtual desktops controlled by locally hosted LLMs by scoping the control surface, action budget, and offline verification of every step."
added: "2026-11"
version: v1
related: [coordinate-based-desktop-tool-driving, desktop-control-session-checkpoint-memory]
tags: [local-llm, desktop, operations]
---

# Local LLM Virtual Desktop Control Operations

## Description
Operate virtual desktops controlled by locally hosted LLMs by scoping the control surface, action budget, and offline verification of every step. Operations are bounded by the declared control surface and offline-verifiable logs rather than cloud-dependent control.

## When to Use
- A locally hosted LLM must drive a virtual desktop environment.
- All control decisions must remain verifiable offline.
- The control surface must be scoped per session.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The virtual desktop session, the declared control surface, and the action policy. |
| Outputs | Executed desktop actions with per-step offline-verifiable logs. |
| Safety | Fail closed by refusing actions outside the declared control surface. |

## Procedure
1. Boot the virtual desktop session and record its baseline state.
2. Declare the control surface: permitted applications and input types.
3. Execute desktop actions only within the declared surface.
4. Log every action with input, target window, and resulting state digest.
5. Verify each logged step offline against the state digest chain.
6. Emit the session record with the verified action log.

## Outputs
| Area | Contract |
|---|---|
| Primary | A session record with verified per-step action logs. |
| Verification | The digest chain that reproduces the session offline. |
| Failure | A refusal record for actions outside the declared surface. |

## Runnable Example
```python
def act(action, surface, log):
    if action["app"] not in surface["apps"] or action["input"] not in surface["inputs"]:
        log.append({"action": action, "result": "refused"})
        return {"ok": False, "refuse": "outside_surface"}
    entry = {"action": action, "result": "executed", "digest": f"d{len(log)}-{action['app']}"}
    log.append(entry)
    return {"ok": True, **entry}

surface = {"apps": ["editor", "terminal"], "inputs": ["mouse", "keyboard"]}
log = []
assert act({"app": "editor", "input": "mouse"}, surface, log)["ok"] is True
assert act({"app": "browser", "input": "mouse"}, surface, log)["refuse"] == "outside_surface"
assert len(log) == 2 and log[0]["digest"] == "d0-editor"
```

## Failure Modes
- The control surface is left open to all desktop applications.
- Action logs require cloud access to verify.
- Steps are logged without state digests, breaking offline verification.
- Refused actions are retried with a widened surface.
- The baseline state is not recorded, so drift is undetectable.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Open WebUI 0.13.0 enables local LLMs to control virtual desktop environments via mouse coordinate manipulation (LLM Daily, November 7, 2026) ([public signal](https://buttondown.com/agent-k/archive/llm-daily-november-07-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Coordinate Based Desktop Tool Driving](coordinate-based-desktop-tool-driving.md)
- [Desktop Control Session Checkpoint Memory](desktop-control-session-checkpoint-memory.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
