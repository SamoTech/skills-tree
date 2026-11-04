---
name: provider-auth-guided-setup
description: Run a guided provider setup for a coding agent that reuses an existing login instead of storing new credentials, and verify the connection before real work.
metadata:
  source: skills/05-code/provider-auth-guided-setup.md
  category: 05-code
  version: "v1"
---

# Provider Auth Guided Setup

## Description
Run a guided provider setup for a coding agent that reuses an existing login instead of storing new credentials, and verify the connection before real work. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A coding agent must use an existing provider subscription login and a misconfigured auth path would surface only mid-task.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the provider login state, the agent provider configuration, and the connection verification command. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Check that the referenced provider CLI is installed and its login state is active.
2. Write the agent provider configuration to reuse that login rather than a new credential store.
3. Run the documented connection verification command and require an explicit success signal.
4. On verification failure, block task dispatch and report the failed verification step.
5. Record which provider identity the agent will use so attribution is unambiguous.
6. Emit a structured result with the verification output and the bound provider identity.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def setup_provider(installed, logged_in, verify):
    if not installed:
        return {"ready": False, "reason": "provider cli missing"}
    if not logged_in:
        return {"ready": False, "reason": "no active login"}
    if verify() != "ok":
        return {"ready": False, "reason": "connection verification failed"}
    return {"ready": True}
assert setup_provider(True, True, lambda: "ok")["ready"] is True
assert setup_provider(True, True, lambda: "error")["reason"] == "connection verification failed"
assert setup_provider(False, True, lambda: "ok")["reason"] == "provider cli missing"
```

## Failure Modes
- The agent is declared ready without running the verification command.
- The provider login is copied into a new credential store instead of being reused.
- Verification failure is retried with a different provider and the config silently drifts.
- The provider identity is not recorded, so audit cannot tell which account acted.
- Subscription terms for the reused login are never checked against agent use.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenCode 2.2.4 adding a guided setup for the Claude Agent provider that uses the Claude Code login and models, with a documented connection verification step (Munder Difflin agent-tools daily, dated November 1, 2026) ([public signal](https://munderdiffl.in/blog/agent-tools-today-2026-11-01/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Harness Remote Engine Deployment](harness-remote-engine-deployment.md)
- [Coding Harness Resource Budgeting](coding-harness-resource-budgeting.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
