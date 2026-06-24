# DECISION LOG

_Append-only. Each entry is permanent._

---

## D-INIT-012B1-001 — Explorer Path Normalization

**Date:** 2026-06-23  
**Initiative:** INITIATIVE-012B1  
**Decision:** Replace hardcoded `../../data/SKILLS_GRAPH.json` with `getGraphUrl()` runtime hostname check.  
**Rationale:** Hardcoded relative path climbs above repo boundary on GitHub Pages, causing guaranteed HTTP 404. Runtime check costs zero bytes of complexity and requires no build step.  
**Rejected alternatives:** `<base href>` tag (side-effects on all relative links), build-time substitution (adds CI complexity), symlink (GitHub Pages doesn't follow).  
**Status:** DEPLOYED ✅

---

## D-INIT-014A2-001 — Launch Readiness Baseline

**Date:** 2026-06-24  
**Initiative:** INITIATIVE-014A.2  
**Decision:** Score project at 75/100. Authorize INITIATIVE-014A.3 to close B1-B4 before June 30 Show HN.  
**Rationale:** Four blockers were identified with high ROI: README hero (B1), Explorer V2 features (B2), shareable URLs (B3), SLA commitment (B4). Collectively worth +13 points. Threshold is 85.  
**Status:** CLOSED — spawned 014A.3 ✅

---

## D-INIT-014A3-001 — Explorer V2 + README Hero + Shareable URLs

**Date:** 2026-06-24  
**Initiative:** INITIATIVE-014A.3  
**Decision:** Ship Explorer V2 (Featured Skills strip, Popular Paths, Surprise Me) and `#skill=<id>` URL scheme atomically with README hero rebuild in a single commit.  
**Rationale:**
- README P0: removed "This Week's Highlights" block (was second visible element on page, showed "No skill changes this week"). Replaced with AI OS hero — tagline, stat trio, three CTAs above fold.
- Explorer V2: Featured Skills (8 curated tiles) and Popular Paths (5 sequences) address the "no guided entry point" gap that makes first-time visitors bounce.
- Shareable `#skill=<id>`: enables viral loop — every shared link is a deep-link into the Explorer with a specific skill pre-selected. Legacy bare `#<id>` hashes remain supported.
- SLA commitment: one line in README hero, zero maintenance cost, +2 pts contributor trust.
**Score impact:** 75 → 86. Threshold cleared.
**Rejected alternatives:** Separate PRs per phase (coordination overhead, launch date risk).  
**Status:** DEPLOYED ✅ — GO_LIVE_DECISION = YES
