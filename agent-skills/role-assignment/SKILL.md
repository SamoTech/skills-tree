---
name: role-assignment
description: Assign explicit responsibilities to agents or workflow stages using capability, authority, inputs, outputs, and escalation boundaries.
metadata:
  source: skills/15-orchestration/role-assignment.md
  category: 15-orchestration
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-role-assignment.json)

# Role Assignment

**Category:** `orchestration`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Assign explicit responsibilities to agents or workflow stages using capability, authority, inputs, outputs, and escalation boundaries. The orchestration step is contract-first: validate state and inputs before acting, and verify the resulting state transition instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | responsibilities | list of object | Task scopes with required capability and authority bounds |
| Input | candidates | list of object | Available agents with verified capabilities |
| Output | assignments | list of object | Agent-task pairs with declared authority and escalation path |
| Output | unassigned | list of string | Responsibilities no candidate can hold within scope |

### Procedure
1. Declare each responsibility's scope, required capability, and authority bound.
2. Match candidates by verified capability, never by assumed identity or seniority.
3. Assign minimum authority; an assignment never exceeds the task's declared scope.
4. Declare the escalation path and the conditions that trigger it for each assignment.
5. Record the assignments with their scope so later steps can verify authority.
6. Leave unmatched responsibilities explicitly unassigned rather than force-fitting a candidate.

### Example

```python
resp = [{'task': 'audit', 'cap': 'security', 'auth': 'read'}]
cands = [{'agent': 'a', 'caps': ['code']}, {'agent': 'b', 'caps': ['security']}]
assignments = [{'task': r['task'], 'agent': c['agent'], 'auth': r['auth']}
               for r in resp for c in cands if r['cap'] in c['caps']]
unassigned = [r['task'] for r in resp if r['task'] not in [a['task'] for a in assignments]]
assert assignments == [{'task': 'audit', 'agent': 'b', 'auth': 'read'}] and unassigned == []
print({'assignments': assignments, 'unassigned': unassigned})
```

### Related Skills

- [Hierarchical Tree](hierarchical-tree.md) - parent-child delegation structure
- [Specialist Agent Routing](specialist-agent-routing.md) - route tasks to specialists
- [Least Privilege Scoping](../14-security/least-privilege-scoping.md) - authority bounds per role

## Failure Modes

- Assignments granting capability or authority beyond the declared task scope.
- Matching by assumed identity instead of verified capability.
- Force-fitting a candidate and hiding the mismatch.
- Missing escalation path, so scope violations have no route back.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing framework's documentation; no benchmark claim is made without reproducible evidence.
