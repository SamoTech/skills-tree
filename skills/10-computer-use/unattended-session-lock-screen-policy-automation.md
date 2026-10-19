---
title: "Unattended Session Lock Screen Policy Automation"
category: 10-computer-use
level: advanced
stability: experimental
description: "Enforce lock-screen policy on unattended computer-use sessions with idle-threshold triggers, verified lock state, and escalation when locking is blocked."
added: "2026-10"
version: v1
related: [idle-detection, session-keepalive-automation]
tags: [session-security, automation, policy]
---
# Unattended Session Lock Screen Policy Automation

## Description
Enforce lock-screen policy on unattended computer-use sessions with idle-threshold triggers, verified lock state, and escalation when locking is blocked. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A computer-use session runs unattended and must lock its screen under a stated idle policy.
- The outcome would change if the lock were assumed without verification.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Watch the session idle signal against the policy threshold, trigger the declared lock action, and verify the lock state from the screen rather than the return code alone.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Out
puts
| Area | Contract |
|---|---|
| Primary | A policy-execution record with idle measurements, lock actions, and verified lock states. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def enforce(idle_ms, policy_ms, lock, verify):
    if idle_ms >= policy_ms:
        lock()
        if not verify():
            raise RuntimeError("lock not verified")
        return "locked"
    return "active"
assert enforce(600000, 300000, lambda: None, lambda: True) == "locked"
```

## Failure Modes
- Assuming the screen locked from a zero exit code without screen verification.
- Locking a session that still has an in-flight user-visible action running.
- Extending the idle threshold without a policy change record.
- Silently continuing when the lock action fails instead of escalating.
- Locking the wrong display or session in multi-session environments.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 agent-security guidance recommends explicit boundary controls for always-on agents handling sensitive streams ([public signal](https://genai.owasp.org/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Idle Detection](../10-computer-use/idle-detection.md)
- [Session Keepalive Automation](../10-computer-use/session-keepalive-automation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
