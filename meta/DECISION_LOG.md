# DECISION_LOG.md

---

## D-INIT-012A-001

**Date:** 2026-06-23  
**Initiative:** INITIATIVE-012A  
**Decision:** Build static GitHub Pages product layer as first public surface.  
**Rationale:** Zero infrastructure cost. Immediately deployable. Indexable by search engines. No auth friction.  
**Status:** IMPLEMENTED

---

## D-INIT-012C-001

**Date:** 2026-06-23  
**Initiative:** INITIATIVE-012C  
**Decision:** Blueprint Generator V1 uses category-order as learning path topology (not full Kahn's algorithm).  
**Rationale:** CAT_ORDER encodes the correct pedagogical progression (perception → reasoning → memory → action → tools → orchestration). Full topological sort adds complexity without meaningfully changing output for the current 25 goals. Kahn's algorithm scheduled for Phase 2.  
**Trade-off:** One level of prerequisite expansion only. Transitive closure deferred.  
**Status:** IMPLEMENTED. Gap documented in LEARNING_PATH_ENGINE.md.

---

## D-INIT-012C-002

**Date:** 2026-06-23  
**Initiative:** INITIATIVE-012C  
**Decision:** Goal catalog hardcoded in `app.js` rather than fetched from a separate JSON file.  
**Rationale:** Eliminates a fetch dependency, enables instant rendering, and works in all GitHub Pages environments without CORS issues. Catalog is small (25 goals, ~8KB). When goals exceed 50, migrate to `data/BLUEPRINT_GOALS.json`.  
**Status:** IMPLEMENTED

---

_Append new decisions above this line in reverse-chronological order._
