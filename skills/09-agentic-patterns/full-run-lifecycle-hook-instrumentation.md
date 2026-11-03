---
title: "Full Run Lifecycle Hook Instrumentation"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Instrument an agent run with hooks that observe the whole lifecycle, including sessions, turns, and permission events, into a structured event log."
added: "2026-11"
version: v1
related: [piped-permission-prompt-delegation, tool-selection-competing-interest-disclosure]
tags: [hooks, instrumentation, lifecycle, agentic-patterns]
---
# Full Run Lifecycle Hook Instrumentation

## Description
Instrument an agent run with hooks that observe the whole lifecycle, including sessions, turns, and permission events, into a structured event log. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent host must see every phase of a run and partial hook coverage has already left permission decisions unobserved.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the agent run lifecycle definition, the hook event schema, and the event log sink. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Declare the lifecycle event types to observe, including session, turn, and permission events.
2. Register a hook for each declared event type and verify registration at run start.
3. Emit a structured event per lifecycle occurrence with type, time, and run identifier.
4. Verify at run end that every declared event type occurred or record its absence.
5. On a missing event type, fail closed and report the gap instead of a green log.
6. Emit a structured result with the event log, coverage check, and run identifier.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def instrument_run(events, declared):
    seen = {e["type"] for e in events}
    missing = [d for d in declared if d not in seen]
    return {"complete": not missing, "missing": missing, "log": events}
declared = ["session_start", "turn", "permission", "session_end"]
ev = [{"type": "session_start"}, {"type": "turn"}, {"type": "permission"}, {"type": "session_end"}]
assert instrument_run(ev, declared)["complete"] is True
assert instrument_run(ev[:-1], declared)["missing"] == ["session_end"]
```

## Failure Modes
- Hooks fire only on turns, so permission events pass unobserved.
- Event payloads omit the run identifier and logs from parallel runs interleave.
- Registration is declared but never verified, so a missing hook looks like a quiet run.
- A missing event type is treated as a normal short run rather than a coverage gap.
- The event log is written to a sink nobody reads and coverage is never re-checked.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Crush 0.99.0 adding hooks that follow the whole run across sessions, turns, permissions, and more (Munder Difflin agent-tools daily, dated November 1, 2026) ([public signal](https://munderdiffl.in/blog/agent-tools-today-2026-11-01/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Piped Permission Prompt Delegation](piped-permission-prompt-delegation.md)
- [Tool Selection Competing Interest Disclosure](tool-selection-competing-interest-disclosure.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
