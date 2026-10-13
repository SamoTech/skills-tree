---
name: hotkey-conflict-resolution
description: Detect conflicting application and global hotkeys before registering new ones and apply an explicit resolution order that never silently shadows user shortcuts.
metadata:
  source: skills/10-computer-use/hotkey-conflict-resolution.md
  category: 10-computer-use
  version: "v1"
---

# Hotkey Conflict Resolution

## Description
Detect conflicting application and global hotkeys before registering new ones and apply an explicit resolution order that never silently shadows user shortcuts. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- new keyboard shortcuts must be registered without breaking existing ones.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for hotkey conflict resolution work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the hotkey conflict resolution steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def resolve(existing, wanted):
    conflicts = [k for k in wanted if k in existing]
    return {**existing, **{k: v for k, v in wanted.items() if k not in conflicts}}, conflicts

safe, conflicts = resolve({'ctrl+s': 'app-a'}, {'ctrl+shift+p': 'app-b', 'ctrl+s': 'app-b'})
assert conflicts == ['ctrl+s'] and 'ctrl+shift+p' in safe
```

## Failure Modes
- Registering a hotkey that silently shadows an existing one.
- Ignoring global OS shortcuts that trump app bindings.
- Resolving conflicts by overwriting without recording the loser.
- Shipping shortcuts that differ across keyboard layouts untested.
- Never re-checking conflicts after other apps install shortcuts.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Hotkey collision handling is a recurring 2026 automation tooling request; this is a dated signal, not an adoption metric.

## Related
- keyboard-shortcut.md
- macro-recording.md
- system-settings-configuration.md
