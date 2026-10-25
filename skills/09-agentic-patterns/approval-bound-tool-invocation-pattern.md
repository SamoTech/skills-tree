---
title: "Approval Bound Tool Invocation Pattern"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Bind every human approval to the exact tool invocation it authorizes so the approval cannot be replayed for a different call."
added: "2026-10"
version: v1
related: [model-tool-pre-approval-tiering, approval-gate]
tags: [approval, bound, tool, invocation, pattern]
---
# Approval Bound Tool Invocation Pattern

## Description
Bind every human approval to the exact tool invocation it authorizes so the approval cannot be replayed for a different call. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An operator needs this capability to proceed safely and verifiably.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Compute the invocation fingerprint from tool identity and canonical arguments, present it to the approver, and refuse any tool call whose fingerprint is not covered by a live approval record.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def authorized(call, approvals):
    fp = call["tool"] + "|" + repr(sorted(call["args"].items()))
    return any(a["fingerprint"] == fp and a["live"] for a in approvals)

call = {"tool": "delete_file", "args": {"path": "a.txt"}}
fp = call["tool"] + "|" + repr(sorted(call["args"].items()))
ap = [{"fingerprint": fp, "live": True}]
assert authorized(call, ap) is True
assert authorized({"tool": "delete_file", "args": {"path": "b.txt"}}, ap) is False
```

## Failure Modes
- The approval is recorded for the tool but not its arguments and any argument set reuses it.
- Fingerprints are computed on raw JSON strings and key order changes re-trigger approval loops.
- A used approval stays live and the same call replays without a new gate.
- The approver sees a summarized invocation and approves a fingerprint they never inspected.
- Approval checks are advisory in the code path and a bypass flag ships by default.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Agent Framework .NET 1.24.0 binds MCP approval headers to the approved invocation, codifying the approval-binding requirement (releasebot.io, dated October 7, 2026) ([public signal](https://releasebot.io/updates/microsoft/agent-framework))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Model Tool Pre-approval Tiering](../09-agentic-patterns/model-tool-pre-approval-tiering.md)
- [Approval Gate](../09-agentic-patterns/approval-gates.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
