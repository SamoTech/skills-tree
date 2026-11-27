---
name: subagent-spawning
description: Create bounded subagent runs for independent subtasks with explicit scopes, concurrency caps, and verified result collection.
metadata:
  source: skills/15-orchestration/subagent-spawning.md
  category: 15-orchestration
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-subagent-spawning.json)

# Subagent Spawning

**Category:** `orchestration`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Create bounded subagent runs for independent subtasks with explicit scopes, concurrency caps, and verified result collection. The orchestration step is contract-first: validate state and inputs before acting, and verify the resulting state transition instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | task | object | The delegated unit of work with its acceptance criteria |
| Input | spawn_policy | object | Max concurrent subagents, tool scope, and timeout per spawn |
| Output | subagent_result | object | The subagent's output with its execution metadata |
| Output | resource_report | object | Spawn count, duration, and budget consumed |

### Procedure
1. Split work only when subtasks are independent; sequential steps stay with the parent.
2. Declare each subagent's tool scope and timeout before spawning it.
3. Enforce the concurrency cap; queue excess spawns instead of over-parallelizing.
4. Collect each subagent's result with its metadata, never bare output text.
5. Verify results against the task's acceptance criteria before merging them.
6. Release spawned resources and record the spawn report for the parent run.

### Example

```python
policy = {'max_concurrent': 2, 'timeout_s': 60}
tasks = [{'id': 'a', 'independent': True}, {'id': 'b', 'independent': True}, {'id': 'c', 'independent': False, 'after': 'a'}]
spawnable = [t['id'] for t in tasks if t['independent']]
batch = spawnable[:policy['max_concurrent']]
deferred = [t['id'] for t in tasks if not t['independent']]
assert batch == ['a', 'b'] and deferred == ['c'] and len(batch) <= policy['max_concurrent']
print({'spawned': batch, 'deferred_to_parent': deferred})
```

### Related Skills

- [Parallel Execution](parallel-execution.md) - run independent work concurrently
- [Agent Pool Warming](agent-pool-warming.md) - pre-provision capacity for spawns
- [Specialist Agent Routing](specialist-agent-routing.md) - route tasks to capable agents

## Failure Modes

- Spawning subagents for dependent steps that need parent sequencing.
- Uncapped parallelism exhausting tokens, threads, or tool quotas.
- Delegating without a tool scope, letting subagents exceed the parent's authority.
- Merging subagent output without checking it against acceptance criteria.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing framework's documentation; no benchmark claim is made without reproducible evidence.
