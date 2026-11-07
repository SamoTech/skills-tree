---
title: "Mobile Checkpoint Supervision Pattern"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Apply the pattern of routing every external agent action through a human checkpoint surfaced on a mobile supervision device."
added: "2026-11"
version: v1
related: [agent-checkpoint-restore-patterns, agent-as-tool]
tags: [patterns, supervision, checkpoints, approval]
---

# Mobile Checkpoint Supervision Pattern

## Description
Apply the pattern of routing every external agent action through a human checkpoint surfaced on a mobile supervision device. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent's external actions must pass a human checkpoint before executing.
- The checkpoint must be reachable from a mobile device, not only a desktop console.
- Approver availability and response times must be measured, not assumed.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The action classification policy, the checkpoint routing rules, and the approver availability register. |
| Outputs | A supervision configuration naming which action classes require checkpoints, their routing targets, and the measured approval paths. |
| Safety | Fail closed by queueing actions indefinitely rather than executing without an answered checkpoint. |

## Procedure
1. Classify every external action class by its checkpoint requirement.
2. Route required actions to the approver register per the routing rules.
3. Surface each pending checkpoint on the mobile supervision surface.
4. Measure approval response time and approver availability per action class.
5. Verify no checkpoint-required action executed without an answered approval.
6. Emit the supervision configuration with measured approval paths.

## Outputs
| Area | Contract |
|---|---|
| Primary | A supervision configuration naming which action classes require checkpoints, their routing targets, and the measured approval paths. |
| Verification | Queue and approval logs that reproduce the measured response paths. |
| Failure | A fail-closed configuration note naming the unroutable action class and its queued behavior. |

## Runnable Example
```python
def route(action, policy, approvers):
    rule = policy.get(action["class"], "checkpoint")
    if rule == "checkpoint":
        available = [a for a in approvers if a["on_duty"]]
        if not available:
            return {"queued": True, "executed": False}
        return {"queued": False, "executed": False, "pending_approval": available[0]["id"]}
    return {"queued": False, "executed": True}

policy = {"read_doc": "auto", "send_email": "checkpoint"}
apprs = [{"id": "dana", "on_duty": True}]
assert route({"class": "read_doc"}, policy, apprs)["executed"] is True
r = route({"class": "send_email"}, policy, apprs)
assert r["executed"] is False and r["pending_approval"] == "dana"
assert route({"class": "send_email"}, policy, [])["queued"] is True
```

## Failure Modes
- Checkpoint-required actions execute while approval is still pending.
- Approver unavailability silently downgrades actions to auto-execute.
- The mobile surface shows approvals but not the action's full payload.
- Response times are never measured, so SLA claims are unverified.
- Action classes are added to the policy without checkpoint classification.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- DigitalOcean's Cuttlefish lets enterprise teams test low-risk workflows with approval gates for every external action, measuring response time and audit quality, including when the approver is unavailable (AI Agent News Today, November 6, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/daily/2026-11-06))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Checkpoint Restore Patterns](agent-checkpoint-restore-patterns.md)
- [Agent As Tool](agent-as-tool.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

