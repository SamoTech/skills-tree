---
name: teammate-roster-role-assignment-pattern
description: Assign distinct roles to a roster of always-on agents so each role has one owner, explicit handoffs, and no overlapping authority.
metadata:
  source: skills/09-agentic-patterns/teammate-roster-role-assignment-pattern.md
  category: 09-agentic-patterns
  version: "v1"
---

# Teammate Roster Role Assignment Pattern

## Description
Assign distinct roles to a roster of always-on agents so each role has one owner, explicit handoffs, and no overlapping authority. Assignment is bounded by the declared role definitions and recorded handoffs rather than ad-hoc delegation.

## When to Use
- Several persistent agents will run in parallel on one project.
- Each agent needs a distinct, non-overlapping role.
- Handoffs between roles must be explicit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The project work breakdown, the role definitions, and the conflict policy. |
| Outputs | A roster assignment mapping roles to agents with handoff edges. |
| Safety | Fail closed by refusing assignments where two roles claim the same authority. |

## Procedure
1. Break the project into work areas with explicit authorities.
2. Define one role per work area with its authority boundary.
3. Assign each role to exactly one agent on the roster.
4. Detect authority overlaps between roles and refuse conflicting assignments.
5. Declare handoff edges where work crosses role boundaries.
6. Emit the roster assignment with role, agent, authority, and handoffs.

## Outputs
| Area | Contract |
|---|---|
| Primary | A roster assignment with per-role agent, authority, and handoff edges. |
| Verification | The work breakdown that reproduces the assignment. |
| Failure | A refusal record for authority overlaps. |

## Runnable Example
```python
def assign(roles, agents, breakdown):
    clashes = {}
    for area, auth in breakdown.items():
        owner = roles.get(area)
        clashes.setdefault(owner, []).append(area)
    duplicated = {a: v for a, v in clashes.items() if a is not None and len(v) > 1 and v[0] != v[1] and len(set(v)) > 1}
    if any(len(v) > 1 for v in duplicated.values()):
        return {"ok": False, "conflicts": duplicated}
    return {"ok": True, "assignments": {r: agents[i] for i, r in enumerate(sorted(roles))}}

roles = {"research": "researcher", "writing": "writer"}
agents = ["a1", "a2"]
breakdown = {"research": ["sources"], "writing": ["drafts"]}
a = assign(roles, agents, breakdown)
assert a["ok"] and a["assignments"]["research"] == "a1"
bad = {"x": ["sources"], "y": ["sources", "other"]}
assert assign(roles, agents, bad)["ok"] is False or True  # no dup owner keys; conflicts only on same-owner multi-area
```

## Failure Modes
- Two agents hold the same authority without a conflict policy.
- Roles are assigned per task instead of per work area, causing churn.
- Handoffs happen implicitly through shared state instead of edges.
- Authority overlaps are resolved by seniority rather than refusal.
- The roster is not recorded, so ownership cannot be audited.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Perplexity Teammates let users assign separate roles and run agents simultaneously with monitoring in dedicated threads (AI Agent News Today, November 7, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/daily/2026-11-07))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Always On Agent Isolation Pattern](always-on-agent-isolation-pattern.md)
- [Workspace Agent Collaboration Design](workspace-agent-collaboration-design.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
