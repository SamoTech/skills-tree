---
title: "Agent Insider Threat Detection Operations"
category: 14-security
level: advanced
stability: experimental
description: "Operate insider threat detection for agent fleets so anomalous agent behavior is contained on recorded evidence."
added: "2026-10"
version: v1
related: [agentic-attack-surface-mapping, agent-payment-fraud-pattern-detection]
tags: [insider-threat, detection, agents, operations]
---
# Agent Insider Threat Detection Operations

## Description
Operate insider threat detection for agent fleets so anomalous agent behavior is contained on recorded evidence. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Autonomous agents hold insider-level access and anomalous behavior must trigger a declared containment runbook.
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
3. Correlate agent action telemetry against the declared behavioral baselines, classify deviations, and execute the containment runbook only on the recorded evidence chain.
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
def contain_agent(baseline, observed):
    if observed["actions_per_hour"] > baseline["max_actions_per_hour"]:
        return {"contain": True, "evidence": "action-rate-breach"}
    if observed["scope"] - baseline["scope"]:
        return {"contain": True, "evidence": "scope-creep"}
    return {"contain": False, "evidence": ""}
b = {"max_actions_per_hour": 100, "scope": {"read"}}
assert contain_agent(b, {"actions_per_hour": 220, "scope": {"read", "write"}})["contain"] is True
```

## Failure Modes
- Baselines are set from vendor defaults and every fleet alerts or none does.
- Containment fires without an evidence chain and harmless agents are disabled in production.
- Scope creep is not a detection signal and quiet permission growth goes unnoticed.
- The containment runbook is not rehearsed and the first real detection stalls.
- Detection telemetry is retained without privacy review and the watch becomes surveillance.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Microsoft Security argues that AI agents are the newest insiders and that security controls must move at agent speed (microsoft.com, dated October 19, 2026) ([public signal](https://www.microsoft.com/en-us/security/blog/2026/10/19/agents-are-your-newest-insiders-security-must-move-at-their-speed/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agentic Attack Surface Mapping](../14-security/agentic-attack-surface-mapping.md)
- [Agent Payment Fraud Pattern Detection](../14-security/agent-payment-fraud-pattern-detection.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
