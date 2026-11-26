---
title: "Performance Profiling"
category: 05-code
level: advanced
stability: stable
version: v2
description: "Measure software performance with representative workloads, identify bottlenecks, and validate changes against explicit performance requirements."
added: "2026-09"
related: [debugging, refactoring]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-performance-profiling.json)

# Performance Profiling

**Category:** `code`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Measure software performance with representative workloads, identify bottlenecks, and validate changes against explicit performance requirements. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | requirement | object | The latency, throughput, memory, or CPU target and how it is measured |
| Input | workload | object | A representative, bounded workload with a labeled environment |
| Output | measurements | object | Baseline and post-change results under identical conditions |
| Output | bottlenecks | list of object | Cost attributed to specific code paths with profiler evidence |

### Procedure
1. Write down the performance requirement and its measurement method before profiling.
2. Build a representative, bounded workload; label synthetic micro-benchmarks as such.
3. Measure a baseline with the profiling tool and record the environment.
4. Attribute cost to specific code paths with the profiler, not intuition.
5. Change one hot path at a time and re-measure under identical conditions.
6. Run the functional test suite; an optimization that breaks correctness is a defect.

### Example

```python
import time

start = time.perf_counter()
total = sum(range(10000))
elapsed = time.perf_counter() - start
assert total == 49995000
print('baseline recorded:', round(elapsed, 6), 'seconds')
```

### Related Skills

- [Debugging](debugging.md) - same evidence-first isolation discipline
- [Refactoring](refactoring.md) - restructure hot paths after measuring them

## Failure Modes

- Optimizing without a baseline.
- Using an unrepresentative or unbounded workload.
- Mistaking measurement noise for improvement.
- Skipping functional regression tests after optimization.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic baseline example, an execution procedure, and corpus-verified related links.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
