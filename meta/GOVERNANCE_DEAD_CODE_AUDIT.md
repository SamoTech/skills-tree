# GOVERNANCE_DEAD_CODE_AUDIT.md

**Initiative:** INITIATIVE-007R — Governance Reality Check  
**Date:** 2026-06-23  
**Evidence basis:** Direct reads of repository files only.

---

## Definition

Dead code in this context means: implemented logic that exists in the repository but whose output is never consumed by a CI gate, never causes a workflow to fail, or whose execution path is unreachable.

---

## Finding 1 — Broken Topological Sort Inner Loop (`recommend.py` lines 98–108)

**File:** `tools/recommend.py`  
**SHA:** `3d95d515`  
**Lines:** 98–108  
**Status:** DEAD CODE — unreachable inner loop body

**Evidence (verbatim from file):**
```python
    while queue:
        skill = queue.popleft()
        result.append(skill)
        for (dependent, edge_type) in [(t, et) for t, et in
                                         [(x, y) for (x, y) in
                                          [(s, e) for s in skill_ids
                                           for (t, e) in [(t, et) for (t, et) in []
                                                          if t == skill]]
                                          if False]
                                         if False]:  # placeholder — simplified
            pass  # full implementation below
```

The innermost comprehension iterates over an empty list `[]`. The outer two comprehensions both have `if False` guards. The `for` loop body (`pass`) therefore **never executes**. The comment `# placeholder — simplified` and `# full implementation below` confirm the author knew this was scaffolding. The actual implementation replaces this block entirely starting at line 111 (`# Simplified stable topo sort`). The dead block does nothing but adds confusion.

**Impact:** Zero functional impact — the dead block is followed by a complete replacement implementation. However, the replacement implementation itself contains the cycle bypass bug (Finding 2).

---

## Finding 2 — Silent Cycle Bypass in Topological Sort (`recommend.py` lines 126–129)

**File:** `tools/recommend.py`  
**SHA:** `3d95d515`  
**Lines:** 126–129  
**Status:** MISREPRESENTED AS DETECTION — it is suppression

**Evidence (verbatim from file):**
```python
        if not ready:  # cycle detected — add arbitrarily
            ready = [sorted(remaining)[0]]
```

The comment says `# cycle detected` but the action is to silently pick an arbitrary node and continue. This means:
1. Cycles are never reported to the caller.
2. No `ValueError` or exit code is raised.
3. The function always returns a result, even on a cyclic graph.
4. No workflow step consumes this function's output to detect cycles.

**Impact:** All 9 committed REQUIRES edges, and any future edges, could form a cycle with zero CI detection. The recommendation engine would silently return a corrupted learning path.

---

## Finding 3 — `dependency-auditor.yml` Has No Graph Governance Role

**File:** `.github/workflows/dependency-auditor.yml` (not fully read, but context from `dependency_auditor.py` SHA `4a3e7a3e` is sufficient)  
**Status:** MISNAMED relative to graph governance expectations

**Evidence:** `dependency_auditor.py` exclusively:
- Reads frontmatter `dependencies:` blocks from skill `.md` files
- Installs listed Python packages via `pip install` in isolated venvs
- Runs the first `python` code snippet found in the skill file
- Writes green badge JSON if install + snippet succeed
- Writes a PR body summarising pass/fail counts

It contains zero graph topology logic. It never reads `data/SKILLS_GRAPH.json`. It never reads any `edges` array. It never reads any `nodes` array. The name `dependency_auditor` refers to **Python package dependencies**, not **graph edge dependencies**.

**Impact:** Any governance plan that assumes `dependency_auditor.py` contributes to graph integrity validation is based on a naming confusion. The tool is entirely unrelated to graph governance.

---

## Finding 4 — `quality-report` Job Never Blocks PRs

**File:** `.github/workflows/validate-graph.yml`  
**SHA:** `667323ca`  
**Job:** `quality-report`  
**Status:** RESULT NEVER CONSUMED as a gate

**Evidence (verbatim from file):**
```yaml
  quality-report:
    name: Skill Quality Score
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

The `if:` condition restricts this job to `push` events on `main` only. It never runs on `pull_request` events. Therefore:
1. No PR can be blocked by a quality score regression.
2. Quality scores are computed only after code is already merged.
3. The output `meta/SKILL_QUALITY_INDEX.md` is a historical record, not a gate.

**Impact:** A quality-degrading change to the graph can be merged to `main` and the score drop will only be visible in the next post-merge commit.

---

## Finding 5 — `pr-checks.yml` Graph Scope is Zero

**File:** `.github/workflows/pr-checks.yml`  
**SHA:** `c5414f05`  
**Status:** MISNAMED relative to graph governance expectations

**Evidence:** The file's own header comment states explicitly:
> `# NOTE: Skill file structural validation (H1, frontmatter, sections, schema) is fully handled by validate-skills.yml and schema-enforce.yml. The old duplicate validator that lived here has been removed to prevent rule drift between the two workflows. This file now owns only: HTML lint (docs/index.html relative-path guard), PR summary comment`

The two jobs are:
1. `html-lint` — checks `docs/index.html` for relative `src=` or `href=` paths
2. `summary` — posts a Markdown comment listing changed skill files

Neither job reads `data/SKILLS_GRAPH.json`. Neither job fails on any graph topology condition.

**Impact:** `pr-checks.yml` provides zero graph governance enforcement. Its name creates a false impression of PR-level graph protection.

---

## Finding 6 — Tag Matching Dead Weight in `match_goal_to_skills()`

**File:** `tools/recommend.py`  
**SHA:** `3d95d515`  
**Function:** `match_goal_to_skills()` line ~51  
**Status:** STRUCTURALLY PRESENT, FUNCTIONALLY INERT

**Evidence from `recommend.py`:**
```python
        haystack = " ".join([
            node.get("title", "").lower(),
            node.get("id", "").lower(),
            " ".join(node.get("tags", [])).lower(),
        ])
```

**Evidence from `MEMORY_STATE.md` (SHA `1d7e0d5f`):**
> `Tags populated: 0/368`

The tags branch of the haystack construction runs on every node lookup but produces an empty string for all 368 nodes. The code is not wrong — it is simply operating on empty data. Keyword matching is degraded to title and ID matching only.

**Impact:** Recommendation quality is reduced. Goal queries that would match on tags (e.g., "NLP", "embeddings", "vector") may return no results or incorrect results when the matching concept is present in tags but absent from the title/ID.

---

## Dead Code Summary

| Finding | File | Type | Functional Impact |
|---|---|---|---|
| 1 | `recommend.py` lines 98–108 | Unreachable inner loop | None (superseded by lines 111–129) |
| 2 | `recommend.py` lines 126–129 | Cycle bypass disguised as detection | HIGH — cycles silently pass |
| 3 | `dependency_auditor.py` entire file | Wrong domain (pip, not graph) | Medium — naming confusion |
| 4 | `validate-graph.yml` `quality-report` job | Post-merge only, never PR-blocking | Medium — quality regressions unblocked |
| 5 | `pr-checks.yml` entire workflow | Zero graph governance scope | High — false safety impression |
| 6 | `recommend.py` tag matching | Empty data for 368 nodes | Medium — degraded recommendation quality |

---

*No synthetic metrics. No inferred relationships. All findings traceable to direct file reads.*
