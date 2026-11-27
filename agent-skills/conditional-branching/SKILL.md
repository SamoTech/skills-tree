---
name: conditional-branching
description: Route workflow execution using explicit conditions, predicates, and mutually understood branch outcomes.
metadata:
  source: skills/15-orchestration/conditional-branching.md
  category: 15-orchestration
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-conditional-branching.json)

# Conditional Branching

**Category:** `orchestration`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Route workflow execution using explicit conditions, predicates, and mutually understood branch outcomes. The orchestration step is contract-first: validate state and inputs before acting, and verify the resulting state transition instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | state | object | The validated workflow state the predicate reads |
| Input | branches | list of object | Declared predicates with mutually exclusive outcomes plus a default |
| Output | branch | string | The selected branch id and the predicate that fired |
| Output | evidence | object | The state values that satisfied the predicate |

### Procedure
1. Declare every branch predicate and its outcome before execution, including a default/error branch.
2. Validate the state the predicate reads; never branch on stale or partial state.
3. Evaluate predicates in a declared order so overlapping predicates resolve deterministically.
4. Record which predicate fired and the state values that satisfied it.
5. Route only to declared outcomes; an unmatched case goes to the default branch, never improvised.
6. Verify the selected branch's preconditions before handing over control.

### Example

```python
state = {'validated': True, 'risk': 'high'}
branches = [{'id': 'escalate', 'when': lambda s: s['validated'] and s['risk'] == 'high'},
            {'id': 'auto', 'when': lambda s: s['validated'] and s['risk'] != 'high'},
            {'id': 'error', 'when': lambda s: not s['validated']}]
fired = next(b for b in branches if b['when'](state))
assert fired['id'] == 'escalate'
print({'branch': fired['id'], 'evidence': {'risk': state['risk'], 'validated': state['validated']}})
```

### Related Skills

- [Sequential Workflow](sequential-workflow.md) - ordered stages between branches
- [State Machine](state-machine.md) - explicit transition graphs
- [Human Approval Gates](human-approval-gates.md) - the escalation branch

## Failure Modes

- Branching on stale, partial, or unvalidated state.
- Overlapping predicates resolved by accidental evaluation order.
- Missing default/error branch, so unmatched cases fail silently or improvise.
- Routing to an outcome that was never declared.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing framework's documentation; no benchmark claim is made without reproducible evidence.
