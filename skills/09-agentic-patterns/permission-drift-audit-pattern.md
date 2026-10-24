---
title: "Permission Drift Audit Pattern"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Audit long-lived agents for permission drift by comparing granted scopes against used scopes over a recorded window."
added: "2026-10"
version: v1
related: [agent-observability-tracing, agent-halt-conditions]
tags: [permission, drift, audit, pattern]
---
# Permission Drift Audit Pattern

## Description
Audit long-lived agents for permission drift by comparing granted scopes against used scopes over a recorded window. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A persistent agent has accumulated grants over weeks and the operator must find scopes granted but never used.
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
3. Collect the granted-scope set and the used-scope set over the recorded window, and flag every grant with no recorded use for downgrade review.
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
def audit_drift(granted, used, window):
    unused = sorted(s for s in granted if s not in used and granted[s] <= window["start"])
    recent = sorted(s for s in granted if s not in used and granted[s] > window["start"])
    return {"downgrade_candidates": unused, "watch": recent}

granted = {"messages": "2026-09-01", "full_disk_access": "2026-09-01", "calendar": "2026-10-20"}
used = {"messages"}
out = audit_drift(granted, used, {"start": "2026-10-01"})
assert out["downgrade_candidates"] == ["full_disk_access"] and out["watch"] == ["calendar"]
```

## Failure Modes
- The audit window is too short so old unused grants look recent.
- Failed authorization attempts are counted as use.
- Use is inferred from the grant date instead of the access log.
- Downgrade candidates are listed but never acted on in a later cycle.
- The audit reads the grant store but not cached client-side grants.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Associated Press reporting traces an agent over-access incident to an always-allow grant whose extent was misunderstood, making drift auditing the pattern-level control (apnews.com, dated October 19, 2026) ([public signal](https://apnews.com/article/meta-muse-openai-dot-ai-privacy-449734d41d3750aad7038b761faa49c9))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Observability Tracing](../09-agentic-patterns/agent-observability-tracing.md)
- [Agent Halt Conditions](../09-agentic-patterns/agent-halt-conditions.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
