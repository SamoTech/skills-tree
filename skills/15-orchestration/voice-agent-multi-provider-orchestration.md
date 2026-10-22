---
title: "Voice Agent Multi Provider Orchestration"
category: 15-orchestration
level: advanced
stability: experimental
description: "Orchestrate realtime voice agents across interchangeable providers with protocol-level failover and recorded provider selections."
added: "2026-10"
version: v1
related: [payment-protocol-failover-orchestration, specialist-agent-routing]
tags: [voice, realtime, failover, orchestration]
---

# Voice Agent Multi Provider Orchestration

## Description
Orchestrate realtime voice agents across interchangeable providers with protocol-level failover and recorded provider selections. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A voice platform must serve conversations across multiple realtime providers and switch providers per session without rewiring clients.
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
3. Model each provider as an endpoint plus protocol dialect, select per session on latency and cost budgets, and emit session records naming the provider, dialect, and failover reason.
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
def pick_provider(session, providers):
    eligible = [p for p in providers if p["dialect"] == session["dialect"] and p["p99_ms"] <= session["latency_budget_ms"]]
    chosen = min(eligible, key=lambda p: p["cost_per_min"])
    return {"session": session["id"], "provider": chosen["id"], "dialect": chosen["dialect"], "reason": "latency_and_cost"}
```

## Failure Modes
- Provider dialects are assumed identical and event mismatches corrupt live sessions mid-conversation.
- Failover mid-session drops context because session state is not portable across providers.
- Latency budgets are never re-measured and the selection stays pinned to a provider that regressed.
- Provider selection is not recorded per session, so cost attribution and incident replay fail.
- Failover fires on a single dropped frame and flaps sessions between providers repeatedly.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The Eleven Realtime launch speaking the OpenAI realtime protocol so voice agents switch by endpoint and model name documents the interchange this skill orchestrates (i-scoop.eu, dated 22 October 2026) ([public signal](https://www.i-scoop.eu/eleven-realtime-elevenlabs/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Payment Protocol Failover Orchestration](../15-orchestration/payment-protocol-failover-orchestration.md)
- [Specialist Agent Routing](../15-orchestration/specialist-agent-routing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
