---
name: performance-profiling
description: Measure software performance with representative workloads, identify bottlenecks, and validate changes against explicit performance requirements.
metadata:
  source: skills/05-code/performance-profiling.md
  category: 05-code
---

## Description
Measure software performance with representative workloads, identify bottlenecks, and validate changes against explicit performance requirements. Prefer measurement over intuition and preserve correctness while optimizing.

## When to Use
Use when latency, throughput, memory, CPU, startup, or resource consumption must be investigated or improved.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | Performance requirement, representative workload, profiling tools, and baseline measurements. |
| Outputs | Bottleneck evidence, targeted change, and before/after verification. |
| Failure modes | Unrepresentative workload, noisy measurements, premature optimization, or correctness regressions. |

## Runnable Example

```python
import time

start = time.perf_counter()
sum(range(10000))
elapsed = time.perf_counter() - start
print('elapsed:', elapsed)
```

## Failure modes
- Optimizing without a baseline.
- Using an unrealistic workload.
- Mistaking measurement noise for improvement.
- Skipping functional regression tests.

## Related
- 05-code
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.
