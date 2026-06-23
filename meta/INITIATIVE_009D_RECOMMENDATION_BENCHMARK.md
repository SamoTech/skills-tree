# INITIATIVE-009D — Recommendation Benchmark

**Date:** 2026-06-23

Prerequisite chains measured after applying approved edges.

---

## Benchmark Results

| Node | Direct Prerequisites (after) | Reachable Prerequisites (transitive) | Chain Depth | Ordering Quality |
|------|------------------------------|--------------------------------------|-------------|------------------|
| `code-generation` | `algorithm-design` | `algorithm-design` | 1 | ✅ Correct — design before implement |
| `code-review` | (none) | — | 0 | ⚠️ Weak — no prerequisites yet; INITIATIVE-009E candidate |
| `dependency-auditor` | (none) | — | 0 | ⚠️ Weak — `code-execution-sandbox` deferred (Rule A failed) |
| `bug-fixing` | `debugging` | `debugging` | 1 | ✅ Correct — localise before patch |
| `code-interpreter-agent` | (none) | — | 0 | ⚠️ Weak — `tool-use-loop` deferred (Related-only) |
| `react` | `cot` | `cot` | 1 | ✅ (from INITIATIVE-005) |
| `plan-and-execute` | `react`, `planning-decomposition` | `react` → `cot`, `planning-decomposition` → `goal-decomposition`, `react` | 2 | ✅ (from INITIATIVE-005/009) |

---

## Notable Gaps for Future Initiatives

| Node | Missing Edge | Evidence Needed |
|------|-------------|------------------|
| `code-review` | → `debugging` or → `code-generation` | Needs body text with qualifying language |
| `code-interpreter-agent` | → `tool-use-loop` or → `code-execution-sandbox` | Needs "requires" / "built on" language in body |
| `dependency-auditor` | → `code-execution-sandbox` | Needs explicit "requires" in body, not just pipeline diagram |
| `refactoring` | → `code-generation` or → `algorithm-design` | Unread — INITIATIVE-009E target |

---

## Progress vs. REQUIRES_COUNT Target

| Metric | Value |
|--------|-------|
| REQUIRES_COUNT after 009D | 15 |
| Target (stretch) | 30 |
| Remaining gap | 15 |
| Categories not yet mined | `07-tool-use` (full), `15-orchestration` (full), remaining `05-code` (23 files), `02-reasoning`, `03-memory`, `12-evaluation` |
