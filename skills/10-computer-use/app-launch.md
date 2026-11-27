---
title: "App Launch"
category: 10-computer-use
level: advanced
stability: stable
version: v2
description: "Launch a specified desktop application using an explicit application identifier or verified path."
added: "2025-03"
related: [app-readiness-probing, window-management]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-app-launch.json)

# App Launch

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Launch a specified desktop application using an explicit application identifier or verified path. The launch is contract-first: resolve and verify the application identity before invoking it, and confirm the observable readiness state afterwards rather than trusting the launch acknowledgement.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | app | object | Application identifier or verified executable path, plus intended profile/workspace |
| Input | readiness | object | The observable postcondition that means "launched" (window title, process present, ready probe) |
| Output | session | object | The launched process or window handle observed on the desktop |
| Output | check | object | Readiness verification result or an explicit failure reason |

### Procedure
1. Resolve the application identifier to an installed, verified path or registered app id.
2. Confirm the launch profile/workspace and any arguments before invoking.
3. Invoke the launch and wait for the declared readiness signal instead of a fixed delay.
4. Verify the observable postcondition (window visible, process running) before continuing.
5. Stop and report the failure reason (not installed, launch timeout, wrong profile) instead of retrying blind.

### Example

```python
launch = {
    "app": {"strategy": "verified_path", "path": "/usr/bin/calculator"},
    "readiness": {"window_title_contains": "Calculator", "timeout_s": 10},
}
import os
assert os.path.exists(launch["app"]["path"]), "app path must be verified before launch"
session = {"pid": 4128, "window_title": "Calculator"}
ready = any(launch["readiness"]["window_title_contains"].lower() in session["window_title"].lower()
            for _ in [0])
assert ready, "readiness postcondition not met"
print({"launched": True, "pid": session["pid"], "readiness": "verified"})
```

### Related Skills

- [App Readiness Probing](app-readiness-probing.md) - verify the launched app is actually ready
- [Window Management](window-management.md) - position or focus the launched window
- [Tool Guardrails](../07-tool-use/tool-guardrails.md) - bound what the launch step may do

## Failure Modes

- The application is not installed or the path/identifier no longer resolves.
- The launch returns before the window reaches a ready state; readiness is never verified.
- A different profile or workspace launches than the one declared.
- A stale app identifier after an application update launches the wrong binary.
- The readiness postcondition cannot be verified within the timeout.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
