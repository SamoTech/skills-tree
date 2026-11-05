---
title: "Codex CLI Voice Task Steering Execution"
category: 04-action-execution
level: advanced
stability: experimental
description: "Execute voice-initiated task start and mid-task steering in a coding CLI without losing the running task state."
added: "2026-11"
version: v1
related: [voice-command-action-binding, human-takeover-mid-action-handoff]
tags: [execution, voice, cli, steering]
---
# Codex CLI Voice Task Steering Execution

## Description
Execute voice-initiated task start and mid-task steering in a coding CLI without losing the running task state. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A developer starts or steers a CLI coding task by voice.
- The voice instruction must bind to a named running task.
- Mid-task steering must preserve the current action state.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The transcribed voice instruction, the running task registry, and the current task state. |
| Outputs | An executed voice instruction naming its intent, bound task, and state transition. |
| Safety | Fail closed by ignoring steering instructions that cannot be bound to a running task. |

## Procedure
1. Transcribe the voice input and strip non-instruction artifacts.
2. Parse the instruction into start, steer, status, or cancel intents.
3. Resolve the instruction against the named running task.
4. For steering, capture the current action state before applying the change.
5. Apply the change and record the pre-change and post-change states.
6. Emit the bound instruction with the preserved state transition.

## Outputs
| Area | Contract |
|---|---|
| Primary | An executed voice instruction naming its intent, bound task, and state transition. |
| Verification | Recorded pre-change and post-change states that reproduce the steering. |
| Failure | A fail-closed report naming the unbindable instruction and the untouched task. |

## Runnable Example
```python
def steer(tasks, name, new_goal):
    if name not in tasks:
        return {"applied": False, "reason": "no-such-task"}
    before = tasks[name]["goal"]
    tasks[name]["goal"] = new_goal
    return {"applied": True, "before": before, "after": new_goal}
t = {"build": {"goal": "run tests"}}
r = steer(t, "build", "run lint then tests")
assert r["applied"] and r["before"] == "run tests"
assert steer(t, "deploy", "x")["applied"] is False
```

## Failure Modes
- A transcription artifact is executed as a steering command.
- Steering applies to the most recent task instead of the named one.
- The pre-change state is overwritten before the change is recorded.
- Cancel and steer intents are conflated, cancelling live work.
- Unbindable instructions are queued and applied later.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI DevDay 2026 let the Codex CLI start and steer tasks by voice, alongside improved prompt editing, session resume, and worktrees (OpenAI DevDay 2026 Recap, dated November 5, 2026) ([public signal](https://openai.com/index/devday-2026-recap/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Voice Command Action Binding](voice-command-action-binding.md)
- [Human Takeover Mid Action Handoff](human-takeover-mid-action-handoff.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
