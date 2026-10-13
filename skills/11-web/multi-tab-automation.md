---
title: "Multi-Tab Automation"
category: 11-web
level: advanced
stability: experimental
description: "Coordinate automation across multiple browser tabs with per-tab state tracking and explicit tab-targeted actions instead of implicit focus assumptions."
added: "2026-10"
version: v1
related: [browser-session-isolation, browser-navigation, popup-dialog-handling]
tags: [tabs, browser, state]
---

# Multi-Tab Automation

## Description
Coordinate automation across multiple browser tabs with per-tab state tracking and explicit tab-targeted actions instead of implicit focus assumptions. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a flow spans several tabs and actions must hit the intended one.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for multi-tab automation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the multi-tab automation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def target_tab(tabs, handle):
    if handle not in tabs:
        raise ValueError('unknown tab handle')
    return tabs[handle]['url']

tabs = {'t1': {'url': 'a'}, 't2': {'url': 'b'}}
assert target_tab(tabs, 't2') == 'b'
```

## Failure Modes
- Acting on whatever tab happens to have focus.
- Losing the tab handle after a popup opens a new one.
- Assuming tab order stays stable across runs.
- Mixing state between tabs that share a domain.
- Never verifying the target tab before the action.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Multi-tab coordination bugs recur in 2026 browser-agent discussions; this is a dated signal, not an adoption metric.

## Related
- browser-session-isolation.md
- browser-navigation.md
- popup-dialog-handling.md
