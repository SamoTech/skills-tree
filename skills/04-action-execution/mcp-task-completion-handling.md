---
title: "Mcp Task Completion Handling"
category: 04-action-execution
level: advanced
stability: experimental
description: "Handle asynchronous MCP task states from submission to completion with bounded polling, terminal-state verification, and fail-closed handling of unknown states."
added: "2026-10"
version: v1
related: [mcp-elicitation-request-parsing, mcp-multi-round-trip-request-authoring]
tags: [mcp, tasks, lifecycle]
---
# Mcp Task Completion Handling

## Description
Handle asynchronous MCP task states from submission to completion with bounded polling, terminal-state verification, and fail-closed handling of unknown states. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An MCP server accepts tasks that complete asynchronously and the agent must react to terminal states.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | mcp task completion handling task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the mcp task completion handling steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A task-state handling record with terminal state, poll count, and result-verification verdict. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def next_action(state, polls, max_polls=10):
    if state in ("completed", "failed"):
        return "settle"
    return "wait" if polls < max_polls else "abort"
assert next_action("completed", 3) == "settle"
assert next_action("running", 10) == "abort"
```

## Failure Modes
- Acting outside the declared task boundary.
- Treating an unknown task state as success.
- Polling without a bound and blocking the agent indefinitely.
- Accepting a completed result whose payload does not match the submission.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Task lifecycle handling is part of the Model Context Protocol task model. ([public signal](https://en.wikipedia.org/wiki/Model_Context_Protocol))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Mcp Elicitation Request Parsing](../07-tool-use/mcp-elicitation-request-parsing.md)
- [Mcp Multi Round Trip Request Authoring](../07-tool-use/mcp-multi-round-trip-request-authoring.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
