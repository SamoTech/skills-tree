---
title: "Persistent Workspace Confirmation Ux Writing"
category: 06-communication
level: advanced
stability: experimental
description: "Write the confirmation and undo copy for a persistent agent workspace, stating what the agent may do, what needs confirmation, and how work is reviewed or undone."
added: "2026-11"
version: v1
related: [report-writing, accessibility-statement-writing]
tags: [communication, ux, confirmations]
---

# Persistent Workspace Confirmation Ux Writing

## Description
Write the confirmation and undo copy for a persistent agent workspace, stating what the agent may do, what needs confirmation, and how work is reviewed or undone. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A workspace ships agent actions with irreversible effects.
- Users need clear confirm and undo affordances.
- A copy review must match risk tiers to wording.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The workspace action inventory, the risk tiers, and the undo capabilities. |
| Outputs | A copy deck naming per-action confirmation text, undo wording, and review entry points. |
| Safety | Fail closed by shipping no action whose consequence text is missing or unbounded. |

## Procedure
1. Inventory every agent action exposed in the workspace.
2. Tier the actions by reversibility and blast radius.
3. Write confirmation copy that states scope, data touched, and reversibility.
4. Write undo copy that names what is restored and what is not.
5. Write review entry points that show history with author and time.
6. Emit the copy deck with the tier rationale.

## Outputs
| Area | Contract |
|---|---|
| Primary | A copy deck naming per-action confirmation text, undo wording, and review entry points. |
| Verification | The recorded inputs and intermediate values that reproduce the primary output from the runnable example. |
| Failure | A fail-closed hold naming the unmet precondition and the withheld primary output. |

## Runnable Example
```python
def write_copy(actions, tiers):
    deck = []
    for a in actions:
        tier = tiers[a["reversible"]]
        deck.append({"action": a["name"], "needs_confirmation": tier == "high", "undo": a["reversible"]})
    return deck

acts = [{"name": "post-draft", "reversible": True}, {"name": "send-payment", "reversible": False}]
deck = write_copy(acts, {True: "low", False: "high"})
assert deck[0]["needs_confirmation"] is False and deck[1]["needs_confirmation"] is True
```

## Failure Modes
- Confirmation copy omits scope or data touched..
- Undo wording implies full restore where none exists..
- High-tier actions ship with the same copy as low-tier ones..
- Review entry points are mentioned but not linked..
- Risk tiers are assigned without a rationale..

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Meta Spaces guidance says builders should define what a Muse agent may retain, what actions require confirmation, and how a user can review or undo its work (AI Agent News Today, November 8, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/daily/2026-11-08))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Report Writing](report-writing.md)
- [Accessibility Statement Writing](accessibility-statement-writing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
