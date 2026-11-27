---
title: "Hierarchical Tree"
category: 15-orchestration
level: advanced
stability: stable
version: v2
description: "Coordinate hierarchical agent teams with explicit parent-child roles, delegation boundaries, and result aggregation."
added: "2025-03"
related: [subagent-spawning, result-aggregation]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-hierarchical-tree.json)

# Hierarchical Tree

**Category:** `orchestration`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Coordinate hierarchical agent teams with explicit parent-child roles, delegation boundaries, and result aggregation. The orchestration step is contract-first: validate state and inputs before acting, and verify the resulting state transition instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | decomposition | object | Parent task split into scoped child tasks with return criteria |
| Input | authority | object | Explicit per-child authority and resource bounds |
| Output | child_results | list of object | Per-child results with evidence against their return criteria |
| Output | aggregated | object | The parent's aggregated result with per-child attribution |

### Procedure
1. Decompose the parent task into child tasks with explicit scope and return criteria.
2. Assign each child the minimum authority and resources its scope requires.
3. Forbid hidden escalation: a child exceeding scope returns a failure, not a broader result.
4. Collect child results with evidence checked against each return criterion.
5. Aggregate deterministically at the parent with per-child attribution.
6. Report failed or incomplete children instead of absorbing them into a partial aggregate.

### Example

```python
tasks = [{'id': 'c1', 'scope': 'parse logs', 'done': True, 'evidence': ['parsed.json']},
          {'id': 'c2', 'scope': 'patch code', 'done': False, 'evidence': []}]
authority = {'c1': 'read', 'c2': 'read-write'}
ok = [t for t in tasks if t['done'] and t['evidence']]
failed = [t['id'] for t in tasks if not t['done']]
assert len(ok) == 1 and failed == ['c2'] and authority['c2'] == 'read-write'
print({'aggregated_from': [t['id'] for t in ok], 'failed': failed})
```

### Related Skills

- [Subagent Spawning](subagent-spawning.md) - creating bounded child agents
- [Result Aggregation](result-aggregation.md) - combining child results
- [Least Privilege Scoping](../14-security/least-privilege-scoping.md) - minimum authority per child

## Failure Modes

- Children granted authority beyond their declared scope.
- Aggregating partial or unverified child results as complete.
- Hidden escalation where a child widens its own task.
- Missing return criteria, so child completion cannot be checked.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing framework's documentation; no benchmark claim is made without reproducible evidence.
