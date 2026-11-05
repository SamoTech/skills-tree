---
title: "AI Kill Switch Policy Design"
category: 14-security
level: advanced
stability: experimental
description: "Design an AI kill switch policy defining who may terminate agents, in what scope, with what evidence, and what gets recorded."
added: "2026-11"
version: v1
related: [unusual-but-permitted-agent-behavior-detection, agent-restart-blocklist-execution]
tags: [security, policy, kill-switch, governance]
---
# AI Kill Switch Policy Design

## Description
Design an AI kill switch policy defining who may terminate agents, in what scope, with what evidence, and what gets recorded. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An organization needs a written kill switch policy.
- Termination authority and scope must be explicit.
- The policy must define evidence and audit requirements.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The threat model, the authority matrix, and the audit requirement set. |
| Outputs | A policy document naming trigger conditions, authority levels, scope, and audit obligations. |
| Safety | Fail closed by blocking termination paths not defined in the policy. |

## Procedure
1. Define trigger conditions from the threat model.
2. Define authority levels and who holds each level.
3. Define the scope each authority level may terminate within.
4. Define the evidence and audit trail obligations per termination.
5. Emit the policy and attach the failure paths it blocks.

## Outputs
| Area | Contract |
|---|---|
| Primary | A policy document naming trigger conditions, authority levels, scope, and audit obligations. |
| Verification | Authority matrix and trigger tests that verify each policy clause. |
| Failure | A fail-closed report naming undefined termination paths. |

## Runnable Example
```python
def policy(trigger, actor_level, scope):
    if actor_level < 2:
        return {"allowed": False}
    return {"allowed": True, "trigger": trigger, "scope": scope}
assert policy("rogue-agent", 3, "dept")["allowed"]
assert policy("rogue-agent", 1, "org")["allowed"] is False
```

## Failure Modes
- The policy grants termination without an authority matrix.
- Triggers are defined so loosely that any anomaly justifies shutdown.
- Audit obligations are defined but not linked to the decision record.
- Scope is defined per team without covering shared environments.
- The policy is written after the first emergency, backwards from what was done.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The AI Kill Switch requires an authorized administrator with a person making the final call (CrowdStrike press release, dated November 3, 2026) ([public signal](https://www.crowdstrike.com/en-us/press-releases/crowdstrike-introduces-ai-kill-switch-for-ai-safety/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Unusual But Permitted Agent Behavior Detection](../14-security/unusual-but-permitted-agent-behavior-detection.md)
- [Agent Restart Blocklist Execution](../undefined/agent-restart-blocklist-execution.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
