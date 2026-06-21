# VERIFIED BASELINE V2

**Created:** 2026-06-21  
**Audit ID:** TASK-000A  
**Method:** Independent repository audit — no prior agent output trusted  
**Source of truth:** Repository file content only  
**Commit baseline:** `474b97de25b59e088a91c7062268be72e4180d0a`

This document is the authoritative starting point for all future task execution. Any agent session reading this document MUST verify the file sizes of governance files before trusting them.

---

## SECTION 1 — VERIFIED NODE COUNT

| Metric | Verified Value | Method |
|---|---|---|
| Graph nodes | **0** | `data/SKILLS_GRAPH.json` = 24 bytes = placeholder string |
| Graph edges | **0** | Same file; no JSON content |
| Skill files (potential nodes) | **377** | PROJECT_MEMORY.md Section 1, 2026-06-14 |
| Skill categories | **17** | Direct directory listing |

**No graph has ever been built. The graph layer starts at zero.**

---

## SECTION 2 — VERIFIED SKILL COUNTS

| Version | Count | % of Total |
|---|---|---|
| v3 (battle-tested) | 27 | 7% |
| v2+ (expanded) | 48 | 13% |
| v1 (stub) | ~302 | ~80% |
| **Total** | **377** | 100% |

---

## SECTION 3 — VERIFIED SCHEMA

| Property | Value | Verified? |
|---|---|---|
| Schema file | `meta/skill-schema.json` | ✅ Referenced in PROJECT_MEMORY |
| Schema version | JSON Schema draft-07 | ✅ PROJECT_MEMORY Section 7 |
| Required fields | title, category, level, stability, added, description | ✅ PROJECT_MEMORY Section 7 |
| Optional fields | version, last_updated, related_skills, frameworks | ✅ PROJECT_MEMORY Section 7 |
| Graph schema | **DOES NOT EXIST** | `data/SKILLS_GRAPH.json` is placeholder |

---

## SECTION 4 — COMPLETED TASKS (VERIFIED)

| Phase | Description | Status | Evidence |
|---|---|---|---|
| Phase 1 Foundation | 17 categories, 377 skills, 30 workflows, CI, schema, Pages, localization, security, versioning | ✅ COMPLETE | PROJECT_MEMORY Section 14 |
| Phase 2 Core Platform | Stub upgrades, Discussions, Paths, mobile UI, search | ⬜ IN PROGRESS | 0 items complete per PROJECT_MEMORY |
| TASK-001 through TASK-005 | Graph planning/implementation | ❌ NOT COMPLETED | All output files are placeholders |

---

## SECTION 5 — OPEN TASKS (VERIFIED FROM PROJECT_MEMORY)

Ordered by priority from PROJECT_MEMORY Section 15:

| ID | Task | Priority | Effort | Dependencies |
|---|---|---|---|---|
| T-01 | Enable GitHub Discussions | P0 | 2h | None |
| T-02 | Tag 30 stubs as good-first-issues | P0 | 3h | T-01 |
| T-03 | Per-category README.md files (17) | P1 | 1d | None |
| T-04 | Stub Upgrade Wave 1 (50 skills) | P0 | 2w | skill-template.md |
| T-05 | Stub Upgrade Wave 2 (100 skills) | P0 | 3w | T-04 |
| T-06 | Stub Upgrade Wave 3 (~152 skills) | P0 | 4w | T-05 |
| T-07 | Model comparison AST sweep | P0 | 1w | T-04 |
| T-08 | Populate paths/ (4 learning tracks) | P0 | 3d | T-04 |
| T-09 | Pagefind full-text search integration | P1 | 2d | None |
| T-10 | Mobile-responsive UI refactor | P1 | 2d | None |
| T-11 | Skill graph JSON export (graph.json) | P1 | 1d | None |
| T-12 | D3 skill graph in UI | P1 | 3d | T-11 |
| T-13 | Skill Paths web UI renderer | P1 | 2d | T-08 |
| T-14 | Benchmark expansion (13 new) | P1 | 2w | T-04 |
| T-19 | CLI scaffold + PyPI | P1 | 1w | docs/api/skills.json |

---

## SECTION 6 — BLOCKED TASKS

| Task | Blocked By | Unblock Action |
|---|---|---|
| Any graph task (T-11, T-12) | Graph placeholder; no governance | Run build-graph.yml OR extend export_skills.py |
| Stub upgrade waves T-05/T-06 | T-04 must complete first | Execute T-04 |
| Paths population T-08 | Enough v2 skills needed | Execute T-04 first |
| CLI T-19 | docs/api/skills.json must be current | Trigger export-skills.yml |
| All future agent governance tasks | Placeholder governance files | Execute Recovery R-01 first |

---

## SECTION 7 — GOVERNANCE FILE STATUS

| File | Required Size for Valid Content | Current Size | Status |
|---|---|---|---|
| `meta/MEMORY_STATE.md` | >1,000B | 18B | ❌ PLACEHOLDER |
| `meta/DECISION_LOG.md` | >1,000B | 24B | ❌ PLACEHOLDER |
| `meta/AGENT_SKILLS_MASTER_PLAN.md` | >2,000B | 23B | ❌ PLACEHOLDER |
| `meta/AGENT_SKILLS_BACKLOG.md` | >1,000B | 19B | ❌ PLACEHOLDER |
| `meta/PROJECT_CONSTITUTION.md` | >1,000B | MISSING | ❌ MISSING |
| `meta/GRAPH_DIFF_PLAN.md` | >500B | MISSING | ❌ MISSING |
| `data/SKILLS_GRAPH.json` | Valid JSON | 24B placeholder | ❌ PLACEHOLDER |

---

## SECTION 8 — CONSTITUTION IMPACT

No `PROJECT_CONSTITUTION.md` exists. Future agent tasks that reference it are operating on a missing document. The closest functional equivalent is `PROJECT_MEMORY.md` (48,049 bytes), which contains explicit mandates, rejected ideas, and success criteria.

**Until PROJECT_CONSTITUTION.md is created:** agent tasks should treat PROJECT_MEMORY.md as the governing document.

---

## MANDATORY PRE-FLIGHT PROTOCOL

Any future agent task MUST complete this pre-flight before proceeding:

1. Read `data/SKILLS_GRAPH.json` — verify it is valid JSON (not a placeholder string)
2. Read `meta/MEMORY_STATE.md` — verify file size > 500 bytes
3. Read `meta/DECISION_LOG.md` — verify file size > 500 bytes
4. If ANY of the above fail: STOP and file a `STATE_DIVERGENCE_REPORT.md`
5. Never trust a claimed node/edge count without reading `data/SKILLS_GRAPH.json` directly

**The minimum bar for a "ready to proceed" state:**
- `data/SKILLS_GRAPH.json` is valid JSON with > 0 nodes
- `meta/MEMORY_STATE.md` > 500 bytes with real content
- No governance files are in placeholder state
