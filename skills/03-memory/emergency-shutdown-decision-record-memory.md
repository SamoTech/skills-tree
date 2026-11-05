---
title: "Emergency Shutdown Decision Record Memory"
category: 03-memory
level: advanced
stability: experimental
description: "Keep the decision record for an emergency agent shutdown so every termination is attributable and reviewable."
added: "2026-11"
version: v1
related: [shutdown-authorization-request-communication, kill-switch-audit-trail-dataset-modeling]
tags: [memory, audit, shutdown, records]
---
# Emergency Shutdown Decision Record Memory

## Description
Keep the decision record for an emergency agent shutdown so every termination is attributable and reviewable. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A kill switch was invoked and the decision must be reconstructible.
- An audit needs who decided, on what evidence, and with what authority.
- Post-incident review requires the full decision context.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The shutdown event, the decision inputs, the actor identity, and the authority level. |
| Outputs | An immutable decision record naming actor, evidence, authority, and outcome. |
| Safety | Fail closed by refusing shutdown execution without a recorded decision entry. |

## Procedure
1. Open a decision record before the shutdown command executes.
2. Attach the alert evidence, anomaly signals, and policy citation.
3. Record the authorizing actor and their authority level.
4. Link the executed action outcome and timestamps to the record.
5. Seal the record and make it available for post-incident review.

## Outputs
| Area | Contract |
|---|---|
| Primary | An immutable decision record naming actor, evidence, authority, and outcome. |
| Verification | Stored evidence links and timestamps that reconstruct the decision chain. |
| Failure | A fail-closed report naming the shutdown attempted without a decision record. |

## Runnable Example
```python
def record(actor, authority, evidence, action):
    if authority < 2:
        return {"sealed": False, "reason": "insufficient authority"}
    return {"sealed": True, "actor": actor, "evidence": evidence, "action": action}
r = record("soc-lead", 3, ["anomaly-17"], "terminate")
assert r["sealed"] and r["action"] == "terminate"
assert record("intern", 1, [], "terminate")["sealed"] is False
```

## Failure Modes
- The shutdown executes before the decision record is opened.
- Evidence is summarized but not linked, so the chain cannot be audited.
- Authority levels are not stated, leaving the actor anonymous.
- Records are editable after the fact.
- The record is stored where the terminated agent could delete it.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- An authorized administrator triggers the kill switch action and every action is recorded in the audit trail (CrowdStrike press release, dated November 3, 2026) ([public signal](https://www.crowdstrike.com/en-us/press-releases/crowdstrike-introduces-ai-kill-switch-for-ai-safety/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Shutdown Authorization Request Communication](../06-communication/shutdown-authorization-request-communication.md)
- [Kill Switch Audit Trail Dataset Modeling](../12-data/kill-switch-audit-trail-dataset-modeling.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
