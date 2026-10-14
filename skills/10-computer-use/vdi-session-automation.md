---
title: "Vdi Session Automation"
category: 10-computer-use
level: advanced
stability: experimental
description: "Automate virtual desktop sessions with connection setup, resolution pinning, and session teardown checks."
added: "2026-10"
version: v1
related: [screen-reading, keyboard-input, screenshot-capture]
tags: [vdi, session, automation]
---
# Vdi Session Automation

## Description
Automate virtual desktop sessions with connection setup, resolution pinning, and session teardown checks. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires vdi session automation before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for vdi session automation. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the vdi session automation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def teardown_plan(sessions, save):
    return [("save" if s in save else "discard", s) for s in sessions]
assert teardown_plan(["s1", "s2"], {"s2"}) == [("discard", "s1"), ("save", "s2")]
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
Virtual desktop automation is requested for running GUI agents in isolated hosted environments. These are dated public signals, not adoption metrics.

## Related
- screen-reading.md
- keyboard-input.md
- screenshot-capture.md
