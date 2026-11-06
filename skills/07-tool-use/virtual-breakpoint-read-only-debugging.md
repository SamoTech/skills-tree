---
title: "Virtual Breakpoint Read-Only Debugging"
category: 07-tool-use
level: advanced
stability: experimental
description: "Debug production agents through read-only virtual breakpoints that pause reasoning for inspection without mutating production state."
added: "2026-11"
version: v1
related: [a2a-remote-agent-tool-invocation, a2a-push-notification-usage]
tags: [tool-use, debugging, observability, safety]
---

# Virtual Breakpoint Read-Only Debugging

## Description
Debug production agents through read-only virtual breakpoints that pause reasoning for inspection without mutating production state. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A production agent must be inspected without risk of mutating live state.
- Breakpoints must be virtual and read-only, not code changes or hot patches.
- Inspection output must be recorded for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The agent's trace stream, the breakpoint definition with trigger conditions, and the read-only output contract. |
| Outputs | An inspection record naming each triggered breakpoint, the captured state, and confirmation that no production mutation occurred. |
| Safety | Fail closed by disabling the debugger when any output path writes to production state. |

## Procedure
1. Define breakpoints with explicit trigger conditions over the trace stream.
2. Attach the debugger in read-only mode and verify its output paths.
3. Capture agent state at each triggered breakpoint without pausing the process.
4. Record the captured state with timestamps and trace positions.
5. Confirm through the output contract that no production state changed.
6. Emit the inspection record with captured states and the no-mutation confirmation.

## Outputs
| Area | Contract |
|---|---|
| Primary | An inspection record naming each triggered breakpoint, the captured state, and confirmation that no production mutation occurred. |
| Verification | Trace positions and output-path audits that reproduce each captured state. |
| Failure | A fail-closed abort naming the write-capable output path and the disabled debugger. |

## Runnable Example
```python
def attach(breakpoints, trace, outputs):
    if any(o.get("writable") for o in outputs):
        return {"attached": False, "reason": "writable_output"}
    hits = []
    for i, step in enumerate(trace):
        for b in breakpoints:
            if b["when"] == step:
                hits.append((b["id"], i, step))
    return {"attached": True, "hits": hits}

trace = ["plan", "tool_call", "tool_call", "done"]
r = attach([{"id": "bp1", "when": "tool_call"}], trace, [{"sink": "log", "writable": False}])
assert r["attached"] and len(r["hits"]) == 2
assert attach([], trace, [{"sink": "db", "writable": True}])["reason"] == "writable_output"
```

## Failure Modes
- The debugger writes checkpoints back to the production store.
- Breakpoints are implemented as code changes deployed to production.
- Captured state omits trace positions, so findings cannot be reproduced.
- All steps are captured instead of breakpoint-triggered ones, flooding storage.
- The no-mutation confirmation is assumed rather than audited.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- HyperProbe introduced virtual breakpoints for read-only production debugging, giving agents observability without mutation risk (mech.app Daily Brief, November 6, 2026) ([public signal](https://www.mech.app/briefs/2026-11-06-daily-brief/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [A2a Remote Agent Tool Invocation](a2a-remote-agent-tool-invocation.md)
- [A2a Push Notification Usage](a2a-push-notification-usage.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

