---
name: parallel-execution
description: Run independent workflow branches concurrently while defining isolation, synchronization, failure aggregation, and join semantics.
metadata:
  source: skills/15-orchestration/parallel-execution.md
  category: 15-orchestration
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-parallel-execution.json)

# Parallel Execution

**Category:** `orchestration`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Run independent workflow branches concurrently while defining isolation, synchronization, failure aggregation, and join semantics. The orchestration step is contract-first: validate state and inputs before acting, and verify the resulting state transition instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | branches | list of object | Demonstrably independent tasks with their inputs |
| Input | join_policy | object | Declared join semantics (all, quorum, first) and failure aggregation |
| Output | results | list of object | Per-branch outcomes with evidence, in stable order |
| Output | join | object | The joined result and any failed branches with reasons |

### Procedure
1. Prove independence before parallelizing: no shared mutable state between branches.
2. Declare the join policy (all, quorum, first-success) and failure aggregation up front.
3. Execute branches concurrently with isolated inputs and per-branch evidence.
4. Collect results in a stable order; never let completion order define result order.
5. Apply the join policy exactly as declared, including the failure path.
6. Report failed branches with reasons instead of silently re-running them sequentially.

### Example

```python
branches = [{'id': 'lint', 'ok': True}, {'id': 'test', 'ok': True}, {'id': 'scan', 'ok': False}]
policy = {'join': 'all', 'on_fail': 'aggregate'}
results = [{'id': b['id'], 'ok': b['ok']} for b in branches]  # stable order
failed = [r['id'] for r in results if not r['ok']]
joined = all(r['ok'] for r in results) if policy['join'] == 'all' else any(r['ok'] for r in results)
assert failed == ['scan'] and joined is False
print({'joined': joined, 'failed': failed, 'order': [r['id'] for r in results]})
```

### Related Skills

- [Sequential Workflow](sequential-workflow.md) - the ordered alternative
- [Speculative Execution](speculative-execution.md) - parallel alternatives with late selection
- [Circuit Breaking](circuit-breaking.md) - stop cascading parallel failures

## Failure Modes

- Shared mutable state creating races between branches.
- Join semantics improvised after the branches finished.
- Completion order leaking into result order, making output nondeterministic.
- Failed branches silently retried or absorbed into a partial join.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing framework's documentation; no benchmark claim is made without reproducible evidence.
