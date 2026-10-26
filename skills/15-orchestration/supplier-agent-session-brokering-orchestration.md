---
title: "Supplier Agent Session Brokering Orchestration"
category: 15-orchestration
level: advanced
stability: experimental
description: "Orchestrate brokered sessions between supplier-side agents and internal systems through a declared exchange with scoped credentials and journaled handoffs."
added: "2026-10"
version: v1
related: [per-task-credential-scoping-actions, agent-gateway-quota-enforcement]
tags: [supplier, agent, session, brokering, orchestration]
---
# Supplier Agent Session Brokering Orchestration

## Description
Orchestrate brokered sessions between supplier-side agents and internal systems through a declared exchange with scoped credentials and journaled handoffs. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

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
3. Broker each supplier-agent session through a declared exchange with scoped credentials, journal the handoffs, and close the session at task completion.
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
def broker_session(requests, exchange):
    results = []
    for r in requests:
        allowed = set(exchange["supplier_scopes"].get(r["supplier"], []))
        granted = set(r["scopes"]) & allowed
        denied = set(r["scopes"]) - allowed
        results.append({"supplier": r["supplier"], "granted": sorted(granted),
                        "denied": sorted(denied),
                        "journal": exchange["journal_id"]})
    return results

exchange = {"supplier_scopes": {"parts-co": ["read:orders"]}, "journal_id": "j-1"}
reqs = [{"supplier":"parts-co","scopes":["read:orders","write:ledger"]}]
out = broker_session(reqs, exchange)
assert out[0]["granted"] == ["read:orders"] and out[0]["denied"] == ["write:ledger"]
```

## Failure Modes
- Supplier sessions bypass the exchange and reach internal systems with ambient credentials.
- Handoffs are journaled after completion and a mid-session breach leaves no journal evidence.
- Sessions are left open after task completion and become standing supplier access paths.
- Two suppliers share one broker scope and a breach in one reaches the other's data.
- Denied scopes are not recorded so suppliers cannot see why a brokering request failed.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The Norforge campaign confirmed at least one intrusion through a third-party supplier, making brokered supplier sessions a recorded control surface (agenticexpo.ai, dated October 23, 2026) ([public signal](https://www.agenticexpo.ai/news/weekly-roundup-23-october-2026))
- The roundup states organizations securing their own agents while granting third-party agents unexamined access build defences around the wrong perimeter (agenticexpo.ai, dated October 23, 2026) ([public signal](https://www.agenticexpo.ai/news/weekly-roundup-23-october-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Per Task Credential Scoping Actions](../04-action-execution/per-task-credential-scoping-actions.md)
- [Agent Gateway Quota Enforcement](../17-infrastructure/agent-gateway-quota-enforcement.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |