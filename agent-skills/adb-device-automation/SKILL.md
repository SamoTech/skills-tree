---
name: adb-device-automation
description: Drive Android devices through adb commands with explicit device targeting, state checks, and output parsing rather than blind command firing.
metadata:
  source: skills/10-computer-use/adb-device-automation.md
  category: 10-computer-use
  version: "v1"
---

# ADB Device Automation

## Description
Drive Android devices through adb commands with explicit device targeting, state checks, and output parsing rather than blind command firing. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Android device tasks must target a specific verified device through adb.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for adb device automation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the adb device automation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def parse_devices(output):
    devices = []
    for line in output.strip().splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == 'device':
            devices.append(parts[0])
    return devices

out = 'List of devices\nemulator-5554\tdevice\nserial-9\tunauthorized'
assert parse_devices(out) == ['emulator-5554']
```

## Failure Modes
- Firing adb commands at whatever device happens to be attached.
- Ignoring unauthorized or offline device states.
- Parsing adb output with brittle line assumptions.
- Treating a successful command exit as proof the device state changed.
- Leaving debug settings enabled after the run.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Android device automation through adb appears repeatedly in 2026 agent tooling requests; this is a dated signal, not an adoption metric.

## Related
- terminal-interaction.md
- app-launch.md
- peripheral-device-detection.md
