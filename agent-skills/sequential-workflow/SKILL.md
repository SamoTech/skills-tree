---
name: sequential-workflow
description: Execute workflow stages in a declared order with explicit dependencies, checkpoints, and completion criteria.
metadata:
  source: skills/15-orchestration/sequential-workflow.md
  category: 15-orchestration
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-sequential-workflow.json)

# Sequential Workflow

**Category:** `orchestration`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Execute workflow stages in a declared order with explicit dependencies, checkpoints, and completion criteria. The orchestration step is contract-first: validate state and inputs before acting, and verify the resulting state transition instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | stages | list of object | Ordered stages with dependencies and completion criteria |
| Input | checkpoints | list of string | Stage boundaries where state is persisted |
| Output | stage_state | list of object | Per-stage completion status with evidence |
| Output | resume_point | string | The checkpoint the workflow can resume from |

### Procedure
1. Declare the stage order, dependencies, and per-stage completion criteria before execution.
2. Validate each stage's preconditions against the previous stage's verified outputs.
3. Execute one stage at a time; never advance on unverified or partial outputs.
4. Persist state at the declared checkpoints with the stage evidence.
5. On failure, stop at the failed stage and record the resume point.
6. Report final state as per-stage completion with evidence, not as a single aggregate.

### Example

```python
stages = [{'id': 's1', 'deps': [], 'done': True, 'evidence': ['out1']},
          {'id': 's2', 'deps': ['s1'], 'done': True, 'evidence': ['out2']},
          {'id': 's3', 'deps': ['s2'], 'done': False, 'evidence': []}]
def ready(s): return all(d in {x['id'] for x in stages if x['done']} for d in s['deps'])
s3 = stages[2]
assert not s3['done'] and ready(s3) is True  # deps met, stage itself pending
resume = next(s['id'] for s in stages if not s['done'])
assert resume == 's3'
print({'completed': [s['id'] for s in stages if s['done']], 'resume_point': resume})
```

### Related Skills

- [Parallel Execution](parallel-execution.md) - when stages are independent
- [State Machine](state-machine.md) - explicit transition graphs between stages
- [Thread-Based Resume](thread-based-resume.md) - resuming from checkpointed state

## Failure Modes

- Advancing on unverified or partial stage outputs.
- A dependency violation treated as a soft warning instead of a stop.
- Missing checkpoints, so failure forces a full restart.
- Reporting a single aggregate completion that hides the failed stage.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing framework's documentation; no benchmark claim is made without reproducible evidence.
