# Decision Log

All entries reference repository evidence only.  
No speculative or hallucinated decisions recorded.

---

## D-INIT-009D-001

**Date:** 2026-06-23  
**Initiative:** INITIATIVE-009D  
**Action:** Evidence-Dense Dependency Mining — `skills/05-code/` Priority A files  

**Files read in full:**
- `skills/05-code/code-generation.md` (8,361 bytes)
- `skills/05-code/bug-fixing.md` (7,913 bytes)
- `skills/05-code/dependency-auditor.md` (18,380 bytes)
- `skills/05-code/code-review.md` (10,174 bytes)
- `skills/05-code/code-interpreter-agent.md` (~2,800 bytes)

**Approved edges:** 2
- `05-code/bug-fixing` → `05-code/debugging`  
  Evidence: "Don't use when: you don't know what's broken (use Debugging first to localise)" — `bug-fixing.md` § When to Use  
- `05-code/code-generation` → `05-code/algorithm-design`  
  Evidence: "Don't use when: the user wants you to design the architecture (use Algorithm Design first)" — `code-generation.md` § When to Use  

**Rejected candidates:** 5
- `code-generation → refactoring`: routing rule ("use instead"), not prerequisite — Rule A FAIL
- `code-generation → function-calling`: conditional dependency ("when X") — Rule A FAIL
- `dependency-auditor → code-execution-sandbox`: Related Skills listing only, no qualifier — Rule A FAIL
- `bug-fixing → reflection`: conceptual description in Related Skills — Rule A FAIL
- `code-interpreter-agent → tool-use-loop`: Related listing only — Rule A FAIL

**REQUIRES_COUNT:** 13 → **15**  
**Cycles introduced:** 0  
**Dangling targets:** 0  
**Duplicates:** 0  
**Status:** QUALITY_APPROVED_PARTIAL (approved < 5, but standards not lowered)

---

## D-INIT-009C-001

**Date:** 2026-06-23  
**Initiative:** INITIATIVE-009C  
**Action:** High-Density Dependency Mining — `skills/09-agentic-patterns/` + `skills/05-code/` inventory  
**Approved edges:** 0  
**Rejected candidates:** 6 (all failed Rule A — no qualifying dependency language)  
**REQUIRES_COUNT:** 13 (unchanged)  
**Status:** QUALITY_APPROVED_PARTIAL

---

## D-INIT-009-001

**Date:** 2026-06-23  
**Initiative:** INITIATIVE-009  
**Action:** Initial dependency extraction from `skills/09-agentic-patterns/` frontmatter reads  
**Approved edges:** 4  
- `agentic-rag` → `03-memory/rag`
- `plan-and-execute` → `02-reasoning/planning-decomposition`
- `planning-decomposition` → `02-reasoning/goal-decomposition`
- `planning-decomposition` → `09-agentic-patterns/react`

**REQUIRES_COUNT:** 9 → 13  
**Status:** CLOSED

---

## D-INIT-008R-001

**Date:** Pre-2026-06-23  
**Initiative:** INITIATIVE-008R  
**Action:** Cycle fix and dangling target cleanup  
**Result:** 0 cycles, 0 dangling targets in validated graph  
**Status:** CLOSED

---

## D-INIT-006A-001

**Date:** Pre-2026-06-23  
**Initiative:** INITIATIVE-006A  
**Action:** Added prerequisite: `agentic-rag` → `03-memory/rag`  
**REQUIRES_COUNT delta:** +1  
**Status:** CLOSED

---

## D-INIT-005-001

**Date:** Pre-2026-06-23  
**Initiative:** INITIATIVE-005  
**Action:** Bulk REQUIRES edge addition across `09-agentic-patterns/`  
**REQUIRES_COUNT delta:** +8  
**Status:** CLOSED
