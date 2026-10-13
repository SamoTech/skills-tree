---
name: system-tray-interaction
description: Automate interaction with operating-system tray icons and their menus using stable element identification and menu-state verification.
metadata:
  source: skills/10-computer-use/system-tray-interaction.md
  category: 10-computer-use
  version: "v1"
---

# System Tray Interaction

## Description
Automate interaction with operating-system tray icons and their menus using stable element identification and menu-state verification. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a needed control or status is only reachable through a tray icon menu.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for system tray interaction work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the system tray interaction steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def find_tray_item(items, target):
    for item in items:
        if item['name'] == target and item['visible']:
            return item
    return None

items = [{'name': 'net', 'visible': False}, {'name': 'audio', 'visible': True}]
assert find_tray_item(items, 'audio')['name'] == 'audio'
assert find_tray_item(items, 'net') is None
```

## Failure Modes
- Clicking tray coordinates without identifying the icon.
- Assuming a menu opened without verifying its state.
- Using tray icons that move or hide on notification.
- Missing a tray action because the menu closed on focus loss.
- Reporting success without verifying the toggled setting.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Tray-icon automation requests appear in 2026 desktop-automation discussions; this is a dated signal, not an adoption metric.

## Related
- desktop-notification-triage.md
- window-management.md
- mouse-click.md
