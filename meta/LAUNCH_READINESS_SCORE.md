# Launch Readiness Score

**Initiative:** INITIATIVE-014A.2 — Phase 6 + Phase 7  
**Date:** 2026-06-24  
**Scoring:** 0–20 per dimension, 100 total  
**Threshold:** 85/100 required for GO

---

## Scoring Matrix

### Dimension 1 — Product (20 pts)

| Criterion | Score | Evidence |
|---|---|---|
| Core feature works end-to-end | 8/8 | Graph loads, search works, filters work (INITIATIVE-012B.1 hotfix complete) |
| Explorer wow factor in <30s | 4/6 | Graph loads visually impressive; V2 features (featured skills, random discovery) not yet shipped |
| Blueprint generator delivers value | 3/6 | 25 goals work; V2 50-goal expansion specced but not implemented |
| **Subtotal** | **15/20** | |

### Dimension 2 — Documentation (20 pts)

| Criterion | Score | Evidence |
|---|---|---|
| README converts visitors | 9/12 | Strong content, weak sequencing; P0 issues identified in README_CONVERSION_AUDIT.md |
| CONTRIBUTING.md is clear | 5/5 | Comprehensive 8.8KB guide |
| Install path works | 3/3 | pip install + CLI validated |
| **Subtotal** | **17/20** | |

### Dimension 3 — Growth (20 pts)

| Criterion | Score | Evidence |
|---|---|---|
| Analytics baseline ready | 3/5 | Tier 1 (GitHub native) available; Tier 2+ not yet instrumented |
| Launch assets ready | 5/5 | All 6 formats complete in LAUNCH_ASSET_PACK.md |
| Referral UTM tracking set up | 3/5 | Spec defined; not yet deployed to live URLs |
| Shareable skill URLs | 2/5 | Specced in EXPLORER_V2_SPEC.md; not yet implemented |
| **Subtotal** | **13/20** | |

### Dimension 4 — Community (20 pts)

| Criterion | Score | Evidence |
|---|---|---|
| GitHub Discussions enabled | 3/5 | Assumed enabled; announcement draft ready |
| Issues labeled for first-timers | 3/5 | CONTRIBUTING.md strong; good-first-issue labels unverified |
| Response time commitment documented | 2/5 | Not formally committed anywhere public |
| Community guidelines present | 4/5 | CODE_OF_CONDUCT.md exists |
| **Subtotal** | **12/20** | |

### Dimension 5 — Distribution (20 pts)

| Criterion | Score | Evidence |
|---|---|---|
| Show HN copy is ready | 5/5 | Primary + 4 variants complete |
| Reddit copy is ready | 4/4 | r/MachineLearning + r/LocalLLaMA versions complete |
| LinkedIn + X ready | 3/4 | Both complete |
| GitHub Discussion draft ready | 2/2 | Complete |
| Launch timing planned | 2/3 | Window identified (June 30); not yet scheduled |
| Pre-seeded upvotes / comment plan | 2/2 | Launch Discussion warms community before HN |
| **Subtotal** | **18/20** | |

---

## Final Score

```
Product        15/20
Documentation  17/20
Growth         13/20
Community      12/20
Distribution   18/20
───────────────────
TOTAL          75/100
```

> ⚠️ **NOTE — Score revised after Phase 1 audit:** The README_CONVERSION_AUDIT revealed that the P0 issues (Highlights block, missing demo GIF, buried CTA) were not accounted for in earlier estimates. The score has been revised downward accordingly.

---

## Phase 7 — Decision

**Score: 75/100 < 85/100 threshold**

```
READY_FOR_SHOW_HN = NO
GO_LIVE_DECISION = CONDITIONAL
```

Launch is blocked on 5 high-ROI gaps identified below. Estimated 4–6 hours of work to close the gap and reach 87+.

---

## TOP 5 BLOCKERS

| # | Blocker | Score Impact | Effort | Phase |
|---|---|---|---|---|
| B1 | README P0: Highlights block + missing demo GIF + buried CTA | +5 pts | 1.5h | Docs |
| B2 | Explorer V2 features not shipped (featured skills, random discovery) | +4 pts | 3h | Product |
| B3 | Shareable skill URLs not implemented | +2 pts | 1h | Growth |
| B4 | Community response time SLA not published | +2 pts | 15m | Community |
| B5 | Blueprint generator: 50-goal expansion not live | +2 pts | 2h | Product |

**Closing B1+B3+B4 alone adds +9 points → 84/100** (still below threshold but near)
**Closing B1+B2+B3+B4 adds +13 points → 88/100** ✅ THRESHOLD MET

---

## TOP 5 STRENGTHS

| # | Strength | Evidence |
|---|---|---|
| S1 | Distribution pack is complete and high-quality | All 6 platform formats written, timing planned |
| S2 | Documentation depth is strong | CONTRIBUTING.md, QUICKSTART, i18n (10 languages), SECURITY.md all polished |
| S3 | Product infrastructure is sound | CI/CD, PyPI, graph hotfix resolved, MCP server live |
| S4 | Differentiation is clear | Comparison table, benchmarks, failure modes — no competitor has this |
| S5 | Install path is frictionless | `pip install skills-tree` + CLI works, zero known blockers |

---

## INITIATIVE-014A.3 Spawn Decision

Since score < 85, INITIATIVE-014A.3 is spawned:

**INITIATIVE-014A.3 — PRE-LAUNCH POLISH SPRINT**  
**Objective:** Close the 5 blockers above to reach 88/100  
**Priority order:** B1 → B4 → B3 → B2 → B5  
**Owner:** Graph Architect  
**Target Launch:** Tuesday, June 30, 2026  

**Success gate:** Re-run readiness score. If ≥ 85 → READY_FOR_SHOW_HN = YES
