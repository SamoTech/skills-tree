---
title: "Agents API Computer Use Integration Coding"
category: 05-code
level: advanced
stability: experimental
description: "Implement a computer-use agent against the Agents API, wiring hosted desktop control, screenshots, and step-level verification into a bounded task loop."
added: "2026-11"
version: v1
related: [screenshot-capture, action-result-verification]
tags: [code, agents-api, computer-use, integration]
---
# Agents API Computer Use Integration Coding

## Description
Implement a computer-use agent against the Agents API, wiring hosted desktop control, screenshots, and step-level verification into a bounded task loop. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A product must drive a remote computer from an agent using the Agents API rather than bespoke browser drivers.
- The outcome would change if clicks or keystrokes were asserted without verifying the resulting screen state.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The Agents API client, the task definition, and the desktop session contract. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Implement the task loop that sends the next action only after parsing the latest screenshot state.
4. Verify each step's postcondition against the captured screen state and stop on the first unverified result.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | An integration implementation with a step-verified task loop and recorded screen-state evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def step_loop(api, task, max_steps):
    state = api.screenshot()
    for i in range(max_steps):
        action = api.decide(task, state)
        new_state = api.act(action)
        if not api.verify(task, new_state):
            return {"status": "unverified", "step": i, "action": action}
        if api.done(task, new_state):
            return {"status": "done", "steps": i + 1}
        state = new_state
    return {"status": "max_steps"}
class Fake:
    def __init__(s): s.n = 0
    def screenshot(s): return {"screen": "home"}
    def decide(s, t, st): s.n += 1; return {"click": "open"}
    def act(s, a): return {"screen": "open"}
    def verify(s, t, st): return True
    def done(s, t, st): return s.n >= 2
r = step_loop(Fake(), "open app", 5)
assert r["status"] == "done" and r["steps"] == 2
```

## Failure Modes
- Actions are dispatched without parsing the screenshot state between steps.
- The loop continues after an unverified step instead of failing closed.
- Screenshots are captured but never stored as step evidence.
- Keystrokes are sent to stale window handles after a window switch.
- The loop relies on max_steps instead of a task-completion check as its exit condition.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI DevDay 2026 brought computer use to the Agents API, letting agents use a computer in ChatGPT with screenshots and inputs under developer control (OpenAI DevDay recap, dated November 4, 2026) ([public signal](https://openai.com/index/devday-2026-recap/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Screenshot Capture](../10-computer-use/screenshot-capture.md)
- [Action Result Verification](../04-action-execution/action-result-verification.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
