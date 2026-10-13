---
title: "Mobile App Automation"
category: 10-computer-use
level: advanced
stability: experimental
description: "Automate mobile application flows across orientations and devices with device-state verification before and after each step."
added: "2026-10"
version: v1
related: [app-readiness-probing, screenshot-capture, ui-element-waiting]
tags: [mobile, testing, ui-automation]
---

# Mobile App Automation

## Description
Automate mobile application flows across orientations and devices with device-state verification before and after each step. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a mobile flow must be verified on real device states and both orientations.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for mobile app automation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the mobile app automation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def check_orientation(steps, orientation):
    if orientation not in ('portrait', 'landscape'):
        raise ValueError('unknown orientation')
    return [s for s in steps if s['orientation'] == orientation]

steps = [{'name': 'login', 'orientation': 'portrait'}, {'name': 'chart', 'orientation': 'landscape'}]
assert len(check_orientation(steps, 'portrait')) == 1
```

## Failure Modes
- Testing only one device or one orientation.
- Continuing after an unexpected orientation change mid-flow.
- Selecting elements by fragile index instead of stable identifiers.
- Skipping post-step state verification on the device.
- Assuming emulator behavior matches physical devices.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Mobile flow automation across devices and orientations is a recurring 2026 QA request; this is a dated signal, not an adoption metric.

## Related
- app-readiness-probing.md
- screenshot-capture.md
- ui-element-waiting.md
