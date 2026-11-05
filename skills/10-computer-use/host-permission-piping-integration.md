---
title: "Host Permission Piping Integration"
category: 10-computer-use
level: advanced
stability: experimental
description: "Integrate an agent harness into a host application that answers permission prompts through a piped channel with declared authority."
added: "2026-11"
version: v1
related: [desktop-foreground-focus-automation, multi-agent-desktop-team-operation]
tags: [computer, permissions, integration, hosts]
---

# Host Permission Piping Integration

## Description
Integrate an agent harness into a host application that answers permission prompts through a piped channel with declared authority. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A host application embeds an agent harness and must answer its permission prompts programmatically.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the harness, the host integration, the permission event types, and the host authority policy. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Declare the permission event types the host will answer and the authority policy behind each answer.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Enable the piped permission channel and bind each event type to an explicit host decision rule.
4. Compare the observed prompt behavior against the declared rules and record deviations.
5. On an unbound event type, deny and surface it, and never answer prompts with an open-ended allow.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def answer_prompt(kind, policy):
    rule = policy.get(kind)
    return {"answer": rule if rule else "deny", "bound": rule is not None}
r = answer_prompt("write_file", {"write_file": "allow_scope"})
assert r["answer"] == "allow_scope" and r["bound"] is True
```

## Failure Modes
- The host answers every prompt with allow because binding rules were never written.
- An unbound prompt type is answered by default instead of denied.
- The authority policy is implicit in host code so it cannot be audited.
- Prompt answers are not logged so approvals cannot be reviewed later.
- The piped channel is enabled without verifying the harness version that supports it.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Crush 0.99.0 letting an app that hosts Crush theme it, tell it which files are open, and answer its permission prompts with CRUSH_PERMISSIONS_PIPED=1 (Munder Difflin agent-tools daily brief, dated November 1, 2026) ([public signal](https://munderdiffl.in/blog/agent-tools-today-2026-11-01/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Desktop Foreground Focus Automation](desktop-foreground-focus-automation.md)
- [Multi Agent Desktop Team Operation](multi-agent-desktop-team-operation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
