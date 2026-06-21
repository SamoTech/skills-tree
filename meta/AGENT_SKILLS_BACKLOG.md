# AGENT_SKILLS_BACKLOG.md — Full Task Backlog

> Rebuilt from repository evidence on 2026-06-21.  
> Status derived from graph node counts and existing report files.  
> No estimates for completed tasks — actual values used.

---

## Phase 1 Tasks

### TASK-001 ✅ DONE
**Title:** Map `09-agentic-patterns/` skill files to graph  
**Actual outcome:** +23 nodes, +59 edges  
**Commit:** `d47878dbef6c11e9932672d1747ab367eb6cb6c6`  
**Report:** `meta/TASK_001_REPORT.md` ✅

---

### TASK-002 🔲 OPEN
**Title:** Add Context Engineering skills  
**Category:** `02-reasoning` or new `context-engineering` sub-area  
**Priority:** HIGH — no dependencies, Phase 1  
**Planned nodes (~5):**
- `skill:context-window-management` — managing token budget and context length
- `skill:prompt-caching` — reusing prefix caches for efficiency
- `skill:context-compression` — techniques to compress/summarize context
- `skill:system-prompt-design` — structured system prompt architecture
- `skill:retrieval-augmented-context` — dynamically injecting retrieved content

**Planned edges (~10–12):** connections to `skill:prompt-engineering`, `skill:rag-retrieval`, `skill:context-management`, `skill:llm-orchestration`  
**Acceptance criteria:**
- [ ] All nodes exist in `data/SKILLS_GRAPH.json`
- [ ] `meta/TASK_002_REPORT.md` created
- [ ] DECISION_LOG entry added
- [ ] MEMORY_STATE.md updated

---

### TASK-003 ✅ DONE
**Title:** Add advanced reasoning layer  
**Actual outcome:** +9 nodes, +21 edges  
**Commit:** UNKNOWN (SHA not recorded in DECISION_LOG — recover from git log)  
**Report:** `meta/TASK_003_REPORT.md` ✅ | `meta/TASK_003_SELF_REVIEW.md` ✅

---

### TASK-004 🔲 OPEN (unblocked)
**Title:** Add causal + counterfactual reasoning  
**Category:** `02-reasoning`  
**Priority:** HIGH — TASK-003 ✅ complete, no remaining blockers  
**Depends on:** TASK-003 ✅  
**Planned nodes (~3):**
- `skill:causal-reasoning` — identifying cause-effect relationships
- `skill:counterfactual-thinking` — evaluating what-if alternatives
- `skill:abductive-reasoning` — inference to the best explanation

**Planned edges (~6–8):** connections to `skill:hypothesis-generation`, `skill:cot`, `skill:reasoning-under-uncertainty`  
**Acceptance criteria:**
- [ ] All nodes exist in `data/SKILLS_GRAPH.json`
- [ ] `meta/TASK_004_REPORT.md` created
- [ ] DECISION_LOG entry added

---

### TASK-005 🔲 OPEN
**Title:** Add core perception skills (OCR, screen parsing, visual grounding)  
**Category:** `01-perception`  
**Priority:** HIGH — `01-perception` has 0 nodes; blocks G03 Browser Agent  
**Planned nodes (~6):**
- `skill:ocr` — optical character recognition from images/screenshots
- `skill:screen-parsing` — extracting UI structure from screenshots
- `skill:visual-grounding` — linking text to visual elements
- `skill:image-understanding` — interpreting image content
- `skill:layout-analysis` — document and UI layout detection
- `skill:multimodal-input` — processing text + image inputs together

**Planned edges (~12–15):** connections to `skill:browser-automation`, `skill:data-extraction`, `skill:context-management`  
**Acceptance criteria:**
- [ ] All nodes exist in `data/SKILLS_GRAPH.json`
- [ ] `meta/TASK_005_REPORT.md` created
- [ ] `01-perception` category has ≥6 nodes

---

### TASK-006 🔒 BLOCKED
**Title:** Add document/data perception skills  
**Category:** `01-perception`  
**Blocked by:** TASK-005  
**Planned nodes (~9):** PDF parsing, table extraction, form understanding, structured data parsing, etc.  
**Acceptance criteria:** TASK-005 must be DONE first.

---

## Phase 2 Tasks (all BLOCKED — Phase 1 not complete)

TASK-007 through TASK-042: blocked pending Phase 1 completion (53-node threshold).  
See `meta/ROADMAP.md` and `meta/ROADMAP_V2.md` for full Phase 2 descriptions.

---

## Backlog Metrics

| Status | Count |
|---|---|
| DONE | 2 (TASK-001, TASK-003) |
| OPEN (no blockers) | 3 (TASK-002, TASK-004, TASK-005) |
| BLOCKED | 1+ (TASK-006, Phase 2 tasks) |

---

*Backlog version: 2.0.0 — Rebuilt from graph evidence 2026-06-21*
