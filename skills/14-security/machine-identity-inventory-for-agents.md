---
title: "Machine Identity Inventory For Agents"
category: 14-security
level: advanced
stability: experimental
description: "Maintain an inventory of machine identities used by agents, mapping each identity to its owner, granted scopes, and last-seen activity, and flagging unmapped identities."
added: "2026-10"
version: v1
related: [agentic-traffic-gateway-configuration, agent-identity-assertion-parsing]
tags: [inventory, identity, audit]
---
# Machine Identity Inventory For Agents

## Description
Maintain an inventory of machine identities used by agents, mapping each identity to its owner, granted scopes, and last-seen activity, and flagging unmapped identities. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Agents act under machine identities and every identity in use must be attributable to an owner.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | machine identity inventory for agents task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the machine identity inventory for agents steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | An inventory audit with unmapped identities and stale grants flagged. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def audit(identities, registered):
    return sorted(i for i in identities if i not in registered)
assert audit(["ci-bot", "agent-x", "ghost"], {"ci-bot", "agent-x"}) == ["ghost"]
```

## Failure Modes
- Acting outside the declared task boundary.
- Treating an unmapped identity as benign and leaving it in use.
- Recording scopes that no longer match the identity live grants.
- Letting the inventory go stale because no last-seen refresh exists.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Machine identity inventory needs for agents appear in 2026 agent security checklists. ([public signal](https://iternal.ai/ai-agent-security-checklist))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agentic Traffic Gateway Configuration](../14-security/agentic-traffic-gateway-configuration.md)
- [Agent Identity Assertion Parsing](../12-data/agent-identity-assertion-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
