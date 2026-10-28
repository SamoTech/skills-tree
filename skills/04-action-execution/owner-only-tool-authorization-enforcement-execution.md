---
title: "Owner Only Tool Authorization Enforcement Execution"
category: 04-action-execution
level: advanced
stability: experimental
description: "Owner Only Tool Authorization Enforcement Execution contract with bounded inputs, recorded verification, and fail-closed handling."
added: "2026-10"
version: v1
related: [per-task-credential-scoping-actions, human-approval-gate-implementation]
tags: [owner, only, tool, authorization]
---

# Owner Only Tool Authorization Enforcement Execution

## Description
Owner Only Tool Authorization Enforcement Execution contract with bounded inputs, recorded verification, and fail-closed handling. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent must execute tool calls only when they appear on the per-request narrowed authorization list.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the per-request authorized tool list as the only valid authorization source.
2. Resolve the incoming tool call to its registry entry and request context.
3. Check the call against the per-request list, never against the full registry.
4. Route owner-only state-changing tools to their approval path when not pre-authorized.
5. Journal the authorization decision with the list version and the call identifier.
6. Emit an execution or denial record with the exact rule that decided it.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def authorize(call, per_request_list, registry):
    allowed = call["tool"] in per_request_list
    return {"execute": allowed, "basis": "per_request_list" if allowed else "not_in_request_scope",
            "registry_size_ignored": len(registry)}
r = authorize({"tool": "wallet_transfer"}, {"search"}, {"search", "wallet_transfer"})
assert r["execute"] is False and r["registry_size_ignored"] == 2
```

## Failure Modes
- The call is validated against the registry so every installed tool is callable.
- Owner-only tools execute because the caller name matches instead of the request scope.
- The narrowed list is cached across requests so stale authorizations leak in.
- Denials are not journaled so registry fallback bugs are invisible.
- The authorization source is never recorded so the decision cannot be reproduced.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The the October 21 review of the VulnCheck advisory for IntentKit CVE-2026-76066, where the executor validated calls against the full tool registry instead of the per-request narrowed list is the dated public signal for this contract. ([public signal](https://niteagent.com/blog/12-ai-agent-pain-points-and-how-to-fix-them/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Per Task Credential Scoping Actions](../04-action-execution/per-task-credential-scoping-actions.md)
- [Human Approval Gate Implementation](../04-action-execution/human-approval-gate-implementation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
