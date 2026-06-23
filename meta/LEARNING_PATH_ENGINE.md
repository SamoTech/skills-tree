# Learning Path Engine
**Initiative:** INITIATIVE-012C  
**Version:** 1.0.0

## Algorithm: Weighted Layer Sort

| Priority | Category | Layer |
|----------|----------|-------|
| 1 | `01-perception` | Foundation |
| 2 | `03-memory` | Retention |
| 3 | `02-reasoning` | Cognition |
| 4 | `04-action-execution` | Execution |
| 5+ | All others | Advanced |

```javascript
function buildLearningPath(skills) {
  return [...skills].sort((a, b) =>
    (LEVEL_WEIGHT[catClass(a)] || 5) - (LEVEL_WEIGHT[catClass(b)] || 5)
  );
}
```

## Guarantees
- Deterministic: same goal → same path
- No infinite loops (pure array sort)
- All input skills preserved

## Known Gaps (v1)
| Gap | Impact | Planned |
|-----|--------|-------|
| Edge-based REQUIRES traversal | Path may miss granular deps | v2 |
| Cross-category prerequisite ordering | Skills within same category use insertion order | v2 |

## v2 Enhancement
Full Kahn's algorithm traversal from SKILLS_GRAPH.json edges for precise dependency ordering.
