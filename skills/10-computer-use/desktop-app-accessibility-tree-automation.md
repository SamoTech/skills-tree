---
title: "Desktop App Accessibility Tree Automation"
category: 10-computer-use
level: advanced
stability: experimental
description: "Drive desktop applications through their accessibility tree with stable role and name selectors instead of coordinates."
added: "2026-10"
version: v1
related: [screen-reading, url-dom-inspection, keyboard-input]
tags: [desktop, app, accessibility, tree]
---
# Desktop App Accessibility Tree Automation

## Description
Drive desktop applications through their accessibility tree with stable role and name selectors instead of coordinates. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires desktop app accessibility tree automation before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for desktop app accessibility tree automation. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the desktop app accessibility tree automation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def selector(role, name):
    return {"role": role, "name": name}
def matches(node, sel):
    return node["role"] == sel["role"] and node["name"] == sel["name"]
assert matches({"role": "button", "name": "Open"}, selector("button", "Open")) is True
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Accessibility-tree automation is the recommended stable approach for desktop UI agents in 2026. These are dated public signals, not adoption metrics.

## Related
- screen-reading.md
- url-dom-inspection.md
- keyboard-input.md
