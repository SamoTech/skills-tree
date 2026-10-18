---
title: "Agent Authorization Context Propagation"
category: 15-orchestration
level: advanced
stability: experimental
description: "Propagate authorization context through orchestration hops so downstream executors receive scoped, unmodified grants with per-hop provenance and a tamper check."
added: "2026-10"
version: v1
related: [agentic-iam-policy-review, agent-team-termination-planning]
tags: [authorization, propagation, provenance]
---
# Agent Authorization Context Propagation

## Description
Propagate authorization context through orchestration hops so downstream executors receive scoped, unmodified grants with per-hop provenance and a tamper check. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An orchestration hop must carry the caller authorization context to the next executor unchanged.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | agent authorization context propagation task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent authorization context propagation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A propagated grant with per-hop provenance and an unchanged scope set. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def propagate(grant, hop):
    carried = dict(grant)
    carried["provenance"] = carried.get("provenance", []) + [hop]
    return carried
g = propagate({"scopes": ["task:run"]}, "orchestrator")
assert g["provenance"] == ["orchestrator"] and g["scopes"] == ["task:run"]
```

## Failure Modes
- Acting outside the declared task boundary.
- Widening a grant mid-chain to make a hop succeed.
- Dropping provenance so a downstream executor cannot name the original grant.
- Propagating a grant after its expiry was reached at an earlier hop.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Authorization context propagation is part of current agentic identity guidance. ([public signal](https://twilio.com/en-us/blog/insights/agentic-identity))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agentic Iam Policy Review](../14-security/agentic-iam-policy-review.md)
- [Agent Team Termination Planning](../09-agentic-patterns/agent-team-termination-planning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
