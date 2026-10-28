---
title: "Bank Credential Quarantine Memory"
category: 03-memory
level: advanced
stability: experimental
description: "Bank Credential Quarantine Memory contract with bounded inputs, recorded verification, and fail-closed handling."
added: "2026-10"
version: v1
related: [agent-credential-exposure-quarantine-memory, pii-memory-minimization]
tags: [bank, credential, quarantine, memory]
---

# Bank Credential Quarantine Memory

## Description
Bank Credential Quarantine Memory contract with bounded inputs, recorded verification, and fail-closed handling. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent must keep banking and payment credentials out of agent memory and quarantine them when they appear.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the credential classes that must never persist and the quarantine rule for accidental capture.
2. Scan memory writes for credential patterns and intercept them before storage.
3. Route intercepted credentials to a quarantine store with no agent read access.
4. Record the quarantine event with time and source without storing the credential itself.
5. Purge any credential that already reached memory and record the purge.
6. Emit a quarantine report with event counts and the residual exposure assessment.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def quarantine(write):
    if any(k in write for k in ("password", "pin", "bank_token")):
        return {"action": "quarantine", "stored": False}
    return {"action": "store", "stored": True}
assert quarantine({"text": "hello"})["stored"] is True
assert quarantine({"text": "my password is x"})["action"] == "quarantine"
```

## Failure Modes
- Credentials are stored because the memory backend is internal and assumed safe.
- The quarantine store is readable by the agent so the quarantine is cosmetic.
- Quarantine events are logged with the credential value included.
- Historical memory is never purged after the rule is introduced.
- The advisory boundary is treated as a user preference rather than a hard rule.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The the October 28 Bank of America advisory forbidding customers from entrusting banking credentials to AI assistants and warning of full financial liability for autonomous agent actions is the dated public signal for this contract. ([public signal](https://blog.luandnh.com/en/ai-daily/2026-10-28/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Credential Exposure Quarantine Memory](../03-memory/agent-credential-exposure-quarantine-memory.md)
- [Pii Memory Minimization](../03-memory/pii-memory-minimization.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
