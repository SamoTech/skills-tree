---
title: "Mobile Remote Agent Stop Execution"
category: 04-action-execution
level: advanced
stability: experimental
description: "Execute a supervised remote stop of a running agent from a mobile operator device with recorded authorization and confirmed termination."
added: "2026-11"
version: v1
related: [action-journaling, action-cost-estimation]
tags: [execution, supervision, safety, auditing]
---

# Mobile Remote Agent Stop Execution

## Description
Execute a supervised remote stop of a running agent from a mobile operator device with recorded authorization and confirmed termination. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A running agent must be stopped remotely from a mobile supervision app.
- The stop must be authorized, executed, and confirmed, not just requested.
- Termination must leave an auditable stop record.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The stop request with the operator identity, the agent registry, and the termination confirmation channel. |
| Outputs | A stop record naming the operator, the stopped agent, the termination confirmation, and the audit verdict. |
| Safety | Fail closed by requiring confirmed termination before the stop is reported complete. |

## Procedure
1. Authenticate the operator and locate the target agent in the registry.
2. Verify the operator's stop authorization for that agent class.
3. Issue the stop command through the supervision channel and record its receipt.
4. Wait for the termination confirmation from the agent runtime.
5. Re-check the registry to confirm the agent is no longer running.
6. Emit the stop record with operator, confirmation, and audit verdict.

## Outputs
| Area | Contract |
|---|---|
| Primary | A stop record naming the operator, the stopped agent, the termination confirmation, and the audit verdict. |
| Verification | Command receipts and termination confirmations that reproduce the stop record. |
| Failure | A fail-closed report naming the unconfirmed termination and the escalated operator alert. |

## Runnable Example
```python
def remote_stop(request, registry, authz):
    agent = registry.get(request["agent"])
    if agent is None or not agent["running"]:
        return {"ok": False, "reason": "agent_not_running"}
    if request["operator"] not in authz.get(agent["class"], []):
        return {"ok": False, "reason": "unauthorized_operator"}
    agent["running"] = False
    return {"ok": True, "stopped": request["agent"], "operator": request["operator"]}

reg = {"bot-1": {"class": "prod", "running": True}}
authz = {"prod": ["dana"]}
assert remote_stop({"agent": "bot-1", "operator": "dana"}, reg, authz)["ok"] is True
assert reg["bot-1"]["running"] is False
assert remote_stop({"agent": "bot-1", "operator": "eve"}, reg, authz)["reason"] == "agent_not_running"
```

## Failure Modes
- The stop is reported complete without a termination confirmation.
- Operator authorization is checked after the stop command is issued.
- The stop record omits who triggered it and under which policy.
- Termination is assumed from a quiet heartbeat instead of a runtime confirmation.
- Stops issued during network loss are never re-confirmed.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- DigitalOcean's Cuttlefish app lets operators stop a running agent remotely from an iPhone on the Managed Agents platform, which remains in public preview (AI Agent News Today, November 6, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/daily/2026-11-06))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Action Journaling](action-journaling.md)
- [Action Cost Estimation](action-cost-estimation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

