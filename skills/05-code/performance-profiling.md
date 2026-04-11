# Performance Profiling

**Category:** `code`  
**Skill Level:** `advanced`  
**Stability:** `stable`

### Description

Measure and analyze code execution time, memory usage, and bottlenecks to guide optimization.

### Example

```python
import cProfile
import pstats

with cProfile.Profile() as pr:
    run_agent_task()

stats = pstats.Stats(pr)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 slowest functions
```

### Related Skills

- [Algorithm Design](algorithm-design.md)
- [Debugging](debugging.md)
