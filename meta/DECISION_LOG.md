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
**Rationale:** Four blockers identified with high ROI: README hero (B1), Explorer V2 features (B2), shareable URLs (B3), SLA commitment (B4). Collectively worth +13 points. Threshold is 85.  
**Status:** CLOSED — spawned 014A.3 ✅

---

## D-INIT-014A3-001 — Explorer V2 + README Hero + Shareable URLs

**Date:** 2026-06-24  
**Initiative:** INITIATIVE-014A.3  
**Decision:** Ship Explorer V2 (Featured Skills strip, Popular Paths, Surprise Me) and `#skill=<id>` URL scheme atomically with README hero rebuild in a single commit.  
**Rationale:** Removed "This Week's Highlights" block. Replaced with AI OS hero. Explorer V2 addresses no guided entry point gap. Shareable URLs enable viral loop. SLA commitment costs zero maintenance.  
**Score impact:** 75 → 86. Threshold cleared.  
**Status:** DEPLOYED ✅ — GO_LIVE_DECISION = YES

---

## D-INIT-014B-001 — Launch Sequence and War Room Protocol

**Date:** 2026-06-24  
**Initiative:** INITIATIVE-014B  
**Decision:** Launch on Tuesday 2026-06-30 at 09:00 ET. Platform sequence: LinkedIn + X simultaneous at T+0, Reddit at T+1h, GitHub Discussions at T-1 (warm) and T+2h (feedback threads). War room checks every 4 hours for first 24h, then daily to T+7d.  
**Rationale:** Tuesday 9-11am ET is peak HN traffic. LinkedIn pre-warms the network before HN spikes. Reddit stagger avoids self-vote detection. GitHub Discussions T-1 creates community activity before external visitors arrive.  
**Rejected alternatives:** Weekend launch (lower HN traffic), all platforms simultaneously (coordination risk, looks spammy).  
**Status:** SCHEDULED — 2026-06-30 ⏳

---

## D-INIT-014B-002 — INITIATIVE-014C Activation Trigger

**Date:** 2026-06-24  
**Initiative:** INITIATIVE-014B  
**Decision:** INITIATIVE-014C activates automatically at T+7d (2026-07-07) after war room check, driven by real user feedback, not internal assumptions.  
**Rationale:** Post-launch iteration must be driven by signal, not by what we think users want. Pre-seeding 014C before launch would be premature optimization. T+7d gives enough signal volume to prioritize with confidence.  
**Status:** SCHEDULED — 2026-07-07 ⏳
