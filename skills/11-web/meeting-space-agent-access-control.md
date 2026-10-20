---
title: "Meeting Space Agent Access Control"
category: 11-web
level: advanced
stability: experimental
description: "Control agent access to meeting spaces so joining, recording, and speaking rights follow a declared per-meeting policy."
added: "2026-10"
version: v1
related: [cors-policy-review, browser-session-isolation]
tags: [meetings, access-control, spaces, agents]
---
# Meeting Space Agent Access Control

## Description
Control agent access to meeting spaces so joining, recording, and speaking rights follow a declared per-meeting policy. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- AI agents request access to shared meeting spaces and their rights must be evaluated against each declared meeting policy.
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
3. Resolve the agent requested rights against the meeting access policy, deny undeclared rights with a recorded reason, and log the granted right set into the meeting record.
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
def resolve(requested, policy):
    granted = sorted(set(requested) & set(policy))
    denied = sorted(set(requested) - set(policy))
    return {"granted": granted, "denied": denied}
pol = ["join", "listen"]
assert resolve(["join", "record"], pol) == {"granted": ["join"], "denied": ["record"]}
```

## Failure Modes
- Agents are granted standing meeting access that outlives the meeting series.
- Recording rights default on and captured media escapes the retention policy.
- Denials are not logged so access audits cannot be reconstructed.
- Policy is evaluated at join only and rights are never re-checked mid-meeting.
- Permissive meeting policy templates are copied across the organization.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 agentic meeting frameworks ship in 2026 meeting platforms as a named weekly product signal (aiagentstore.ai, dated October 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [CORS Policy Review](../11-web/cors-policy-review.md)
- [Browser Session Isolation](../11-web/browser-session-isolation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
