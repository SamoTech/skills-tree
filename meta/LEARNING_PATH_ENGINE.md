# LEARNING PATH ENGINE
> Initiative: INITIATIVE-012C | Phase 4

## Overview

The Learning Path Engine converts a flat skill list into an ordered
sequence of learning phases using topological sorting on the prerequisite graph.

## Algorithm: Kahn's BFS Topological Sort

```python
def topological_sort(skills, edges):
    in_degree = {s: 0 for s in skills}
    adj = {s: [] for s in skills}
    
    for edge in edges:
        if edge.from in in_degree and edge.to in in_degree:
            adj[edge.from].append(edge.to)
            in_degree[edge.to] += 1
    
    queue = [s for s in skills if in_degree[s] == 0]
    phases = []
    visited = set()
    
    while queue:
        phase = sorted(queue)
        phases.append(phase)
        visited.update(phase)
        next_queue = []
        for node in phase:
            for neighbor in adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0 and neighbor not in visited:
                    next_queue.append(neighbor)
        queue = next_queue
    
    return phases
```

## Cycle Detection

1. Track visited nodes during BFS
2. If a node is encountered again before being fully processed → cycle
3. Log warning: `CYCLE_DETECTED: skill_id → skill_id`
4. Remove offending edge and continue
5. Document in `meta/STATE_DIVERGENCE_REPORT.md` if cycles found

## Current Graph Status

- `requires_count` in SKILLS_GRAPH.json meta: **1**  
- Most edges are in `prerequisites[]` arrays on nodes
- Cycle risk: LOW (manual authoring, small graph)

## Gaps Identified

| Gap | Severity | Mitigation |
|-----|----------|------------|
| Most nodes have empty `prerequisites[]` | Medium | Use category ordering as proxy |
| `requires_count=1` suggests sparse REQUIRES edges | Low | Fall back to category-layer ordering |
| No explicit learning_time per skill | Low | Estimate: basic=0.5w, intermediate=1w, advanced=2w |

## Fallback Ordering

When a skill has no prerequisites, order by layer:
```
perception → reasoning → memory → action → code → tool-use → agentic
```

Mapped to category prefixes: `01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11`
