---
title: "Banking Agent Credential Delegation Review"
category: 14-security
level: advanced
stability: experimental
description: "Banking Agent Credential Delegation Review contract with bounded inputs, recorded verification, and fail-closed handling."
added: "2026-10"
version: v1
related: [agent-wallet-key-custody-review, least-privilege-scoping]
tags: [banking, agent, credential, delegation]
---

# Banking Agent Credential Delegation Review

## Description
Banking Agent Credential Delegation Review contract with bounded inputs, recorded verification, and fail-closed handling. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent must review any design that delegates banking credentials to an agent against the explicit prohibition and liability transfer.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Inventory every path where banking credentials could reach agent-controlled storage or input.
2. Compare each path against the advisory prohibition and the liability statement.
3. Identify the human-in-the-loop boundary and verify credentials stop there.
4. Check transaction-level approval for any financial action the agent can reach.
5. Record residual paths that remain after the boundary fixes.
6. Emit the review verdict with the prohibited paths found and the required design changes.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def review(paths):
    prohibited = [p["name"] for p in paths if p["credential_reaches_agent"]]
    return {"verdict": "reject" if prohibited else "pass", "prohibited_paths": prohibited}
r = review([{"name": "oauth_flow", "credential_reaches_agent": False}, {"name": "password_store", "credential_reaches_agent": True}])
assert r == {"verdict": "reject", "prohibited_paths": ["password_store"]}
```

## Failure Modes
- The review treats the advisory as a user preference rather than a prohibition.
- Credential storage is assessed for encryption instead of absence.
- The liability statement is not surfaced to the design decision.
- Transaction-level approval is assumed from read-access scoping.
- Residual paths are not recorded so the review looks clean.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The the October 28 Bank of America advisory that customers must not entrust banking credentials to AI assistants and carry complete financial liability for autonomous agent actions is the dated public signal for this contract. ([public signal](https://blog.luandnh.com/en/ai-daily/2026-10-28/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Wallet Key Custody Review](../14-security/agent-wallet-key-custody-review.md)
- [Least Privilege Scoping](../14-security/least-privilege-scoping.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
