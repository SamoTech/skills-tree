---
title: "Multi Agent Desktop Team Operation"
category: 10-computer-use
level: advanced
stability: experimental
description: "Operate a desktop agent team where a commander decomposes the goal into tasks and coordinates specialist agents plus external agents."
added: "2026-11"
version: v1
related: [desktop-foreground-focus-automation, host-permission-piping-integration]
tags: [computer, agents, teams, coordination]
---

# Multi Agent Desktop Team Operation

## Description
Operate a desktop agent team where a commander decomposes the goal into tasks and coordinates specialist agents plus external agents. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A goal on the user desktop needs multiple specialist agents coordinated by a single command layer.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the goal, the specialist roster, and the task decomposition and coordination contract. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Declare the goal, the specialist roster including any external agents, and the task decomposition contract.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Have the commander decompose the goal into tasks and assign each to a named specialist.
4. Compare completed tasks against the goal contract and record deviations.
5. On a specialist failure or conflict, reassign within the roster, and never let two agents mutate the same surface unsynchronized.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def coordinate(goal, specialists):
    tasks = goal.split()
    assigned = {t: specialists[i % len(specialists)] for i, t in enumerate(tasks)}
    return {"tasks": len(assigned), "specialists_used": len(set(assigned.values()))}
r = coordinate("clean scan report", ["coder", "reviewer"])
assert r["tasks"] == 3 and r["specialists_used"] == 2
```

## Failure Modes
- Two specialists mutate the same file or surface without synchronization.
- The decomposition is kept in memory only so a restart loses the task map.
- An external agent is invoked without inheriting the task boundary.
- Specialist failures are retried indefinitely instead of reassigned.
- The commander does work itself instead of coordinating, collapsing the team pattern.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Orkas, an open-source team of AI agents on the desktop, where a Commander turns your goal into tasks and coordinates 16 built-in specialist agents plus Claude Code, Codex, OpenCode, OpenClaw, and Hermes (Munder Difflin agent-tools daily brief, dated November 1, 2026) ([public signal](https://munderdiffl.in/blog/agent-tools-today-2026-11-01/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Desktop Foreground Focus Automation](desktop-foreground-focus-automation.md)
- [Host Permission Piping Integration](host-permission-piping-integration.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
