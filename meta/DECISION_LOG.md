# DECISION_LOG.md

**Last updated:** 2026-06-23T12:10:00+03:00  
**Rule:** Only record decisions that can be proven from commits, files, or repository structure.

---

## D-006A-001

**Date:** 2026-06-23  
**Initiative:** INITIATIVE-006A  
**Decision:** Add `prerequisites: [03-memory/rag]` to `agentic-rag.md`; all other approved REQUIRES edges already present in frontmatter.  
**Evidence:**
- `agentic-rag.md` (SHA `d48010cf`) had no `prerequisites` field before this commit
- Body text: *"Extends basic RAG"* — "extends" is approved REQUIRES language per INITIATIVE-006 classification rules
- Related Skills in body: `../03-memory/rag.md` — confirms cross-category target, not `09-agentic-patterns/rag`
- All other 7 approved edges verified already present in their source files (SHAs confirmed by direct reads)
- Rejected edges (`reflection→react`, `memory-augmented→react`) confirmed absent from all files

**Result:** Commit `ec014904f8af1620ac6622fb252ebbcbe9a64547` pushed. agentic-rag.md version bumped v1 → v1.1.

---

## D-006-001

**Date:** 2026-06-23  
**Initiative:** INITIATIVE-006  
**Decision:** Relationship typology audit of all 22 skills in `09-agentic-patterns/`. 13 candidate edges reviewed.  
**Evidence:** Direct reads of all 9 candidate skill files (SHAs recorded in audit report)  
**Result:**
- 7 APPROVED REQUIRES edges
- 2 REJECTED (reflection→react, memory-augmented→react)
- 2 RECLASSIFIED (react→function-calling as SUPPORTS; rag-pipeline→rag as SUBSKILL_OF)
- 2 NEW DISCOVERIES (lats→tot, lats→reflection from frontmatter reads)
- REQUIRES_CONFIDENCE_SCORE: 0.778 → corrected to 0.889 after target fix

---

## D-INIT-004W1-001

**Date:** 2026-06-22  
**Initiative:** INITIATIVE-004W.1  
**Decision:** Mark pipeline as LIVE and READY_FOR_INITIATIVE_005  
**Evidence:**
- `data/SKILLS_GRAPH.json` SHA `c9b0be60b3a1d3fac16e6d8653e2254dbd182be2` read directly
- `schema_version: 3.1`, `requires_count: 1`, `node_count: 368` confirmed
- `generated_at: 2026-06-22T12:03:48Z` — after remediation commit `f6be264e`

**Result:** Pipeline confirmed operational.

---

## D-INIT-004W-001

**Date:** 2026-06-22  
**Initiative:** INITIATIVE-004W  
**Decision:** Root cause of PIPELINE_VERIFICATION_FAILED is workflow concurrency cancellation race condition  
**Evidence:** GitHub Actions log showed `build-graph` cancelled before completing  
**Result:** Remediation push `f6be264e` executed. Workflow ran to completion.

---

## D-INIT-004-001

**Date:** 2026-06-22  
**Initiative:** INITIATIVE-004  
**Decision:** Activate REQUIRES edge pipeline via `prerequisites` field in skill markdown frontmatter  
**Evidence:** `tools/build_graph.py` SCHEMA_VERSION = `3.1`; `prerequisites` key in `SkillSchema`  
**Result:** First REQUIRES edge generated on successful rebuild.

---

## D-003-001

**Date:** 2026-06 (INITIATIVE-003)  
**Decision:** Bump graph schema to v3.1; add `prerequisites` field to skill node schema  
**Evidence:** `tools/build_graph.py` SCHEMA_VERSION = `3.1` (confirmed by direct file read)  
**Result:** Schema v3.1 live.

---

## D-R01-001

**Date:** 2026-06-22 (MISSION R-01)  
**Decision:** All governance documents rebuilt from repository evidence only; prior hallucinated metrics removed  
**Evidence:** Direct reads of all files under `meta/`, `skills/`, `.github/workflows/`  
**Result:** Core governance files rewritten with verified data only.
