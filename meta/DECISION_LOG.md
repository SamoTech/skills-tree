# Decision Log

## D-INIT-012B1-001 — Explorer Path Normalization
**Date:** 2026-06-23  
**Decision:** Replace hardcoded `../../data/SKILLS_GRAPH.json` with `getGraphUrl()` runtime hostname check.  
**Rationale:** GitHub Pages base path `/skills-tree/` makes relative paths climb above the repo boundary. Runtime check is zero-dependency and works without build tooling.  
**Alternatives Rejected:** `<base href>` tag (side-effects on all relative links); build-time path substitution (requires CI change).  
**Status:** ✅ IMPLEMENTED

---

## D-INIT-014A2-001 — Launch Readiness Score: 75/100 → Spawn 014A.3
**Date:** 2026-06-24  
**Decision:** Do NOT launch Show HN immediately. Spawn INITIATIVE-014A.3 to close 5 identified blockers.  
**Score:** 75/100 (threshold: 85/100)  
**Key blocker:** README P0 issues (Highlights block, missing demo GIF) will torpedo HN conversion for all traffic. A P0 README on launch day cannot be recovered from — first impressions are permanent.  
**Rationale:** The distribution assets (Show HN copy, Reddit, LinkedIn, X thread) are high quality and ready. The product infrastructure is sound. The failure mode is conversion, not product. Fixing B1–B4 (estimated 5–6 hours) gains +13 points and clears the threshold.  
**Launch window:** Tuesday, June 30, 2026, 9:00 AM ET (16:00 EEST)  
**Decision owner:** Graph Architect  
**Status:** ✅ SPAWNED INITIATIVE-014A.3
