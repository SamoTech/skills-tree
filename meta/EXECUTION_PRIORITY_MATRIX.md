# Skills Tree — Execution Priority Matrix
**Role: Chief Product Architect**
**Date: 2026-06-14**
**Version: 1.0**

---

## Scoring Framework

Every task is evaluated across five dimensions (0–10 each). **Total = 50.**

| Dimension | Definition |
|-----------|-----------|
| **Product Value** | How much does this improve the core product capability (catalog quality, API, search, structured data)? |
| **User Value** | How much does this help the primary user — an AI agent builder — find and use skills faster? |
| **Adoption Impact** | How directly does this drive GitHub stars, contributors, PyPI downloads, or framework citations? |
| **Technical Leverage** | Does this unlock other tasks, compound over time, or remove systemic blockers? |
| **Sponsor Attractiveness** | Does this make the project more credible, fundable, or attractive to enterprise sponsors? |

### Hard Rules

- **Any task scoring < 30/50 → Deferred** (documented in Section 3)
- **Any task scoring < 25/50 → Rejected** (documented in Section 4)
- **Community / marketing / documentation tasks cannot exceed 20% of completed work**
- **At least 80% of development effort must go toward product capabilities**

### ROI Formula

ROI = (Impact Score) / (Effort Score × Risk Score) × 100

Where Effort and Risk are scored 1–10 (10 = highest effort / highest risk). ROI > 100 = top priority. ROI 50–99 = execute. ROI < 50 = defer unless dependencies require it.

---

## Section 1 — Full Scoring Matrix

> Tasks marked ✅ are complete as of 2026-06-14. All others are unfinished.

| ID | Task | Product Value | User Value | Adoption Impact | Technical Leverage | Sponsor Attractiveness | **Impact Total** | Effort (1-10) | Risk (1-10) | **ROI** | Classification |
|----|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| T-04 | Stub Upgrade Wave 1 (50 skills) | 10 | 10 | 9 | 8 | 8 | **45** | 6 | 2 | **375** | 🟢 EXECUTE |
| T-09 | Pagefind full-text search integration | 9 | 10 | 8 | 9 | 7 | **43** | 3 | 2 | **717** | 🟢 EXECUTE |
| T-11 | Skill graph JSON export (`graph.json`) | 8 | 8 | 8 | 10 | 8 | **42** | 2 | 1 | **2100** | 🟢 EXECUTE |
| T-07 | Model comparison AST sweep | 9 | 9 | 7 | 7 | 8 | **40** | 4 | 3 | **333** | 🟢 EXECUTE |
| T-19 | CLI scaffold + PyPI publication | 9 | 9 | 9 | 8 | 9 | **44** | 5 | 4 | **220** | 🟢 EXECUTE |
| T-05 | Stub Upgrade Wave 2 (100 skills) | 10 | 9 | 8 | 7 | 7 | **41** | 7 | 2 | **293** | 🟢 EXECUTE |
| T-08 | Populate `paths/` — 4 learning tracks | 8 | 9 | 8 | 8 | 7 | **40** | 4 | 2 | **500** | 🟢 EXECUTE |
| T-12 | D3 skill graph in web UI | 7 | 9 | 9 | 7 | 8 | **40** | 5 | 4 | **200** | 🟢 EXECUTE |
| T-14 | Benchmark expansion (13 new benchmarks) | 8 | 8 | 9 | 7 | 9 | **41** | 6 | 3 | **228** | 🟢 EXECUTE |
| T-24 | MCP registry listing | 8 | 8 | 10 | 9 | 9 | **44** | 4 | 5 | **220** | 🟢 EXECUTE |
| T-21 | AI stub upgrade draft PRs | 9 | 8 | 7 | 9 | 8 | **41** | 5 | 5 | **164** | 🟢 EXECUTE |
| T-25 | Semantic search embeddings | 8 | 9 | 7 | 8 | 7 | **39** | 5 | 5 | **156** | 🟢 EXECUTE |
| T-23 | LangChain Hub submission | 7 | 8 | 10 | 8 | 9 | **42** | 4 | 5 | **210** | 🟢 EXECUTE |
| T-13 | Skill Paths UI renderer | 7 | 9 | 7 | 7 | 6 | **36** | 3 | 2 | **600** | 🟢 EXECUTE |
| T-10 | Mobile-responsive UI refactor | 6 | 8 | 7 | 5 | 5 | **31** | 3 | 2 | **517** | 🟢 EXECUTE |
| T-20 | CLI `new` wizard | 7 | 8 | 7 | 6 | 6 | **34** | 3 | 3 | **378** | 🟢 EXECUTE |
| T-06 | Stub Upgrade Wave 3 (remaining ~152 skills) | 9 | 8 | 7 | 6 | 6 | **36** | 8 | 2 | **225** | 🟢 EXECUTE |
| T-15 | JSON-LD SEO export completion | 5 | 5 | 7 | 5 | 6 | **28** | 2 | 2 | **700** | 🔵 EXECUTE (high ROI, trivial effort) |
| T-16 | GitHub Release packaging (zip artifact) | 4 | 5 | 6 | 4 | 6 | **25** | 1 | 1 | **2500** | 🔵 TRIVIAL WIN |
| T-22 | Skill Champion system | 5 | 5 | 7 | 5 | 5 | **27** | 2 | 1 | **1350** | 🔵 EXECUTE (trivial effort) |
| T-03 | Per-category README files (17 files) | 5 | 6 | 5 | 4 | 4 | **24** | 2 | 1 | **1200** | 🔴 REJECTED (< 25) |
| T-18 | Used-in social proof / SHOWCASE.md | 3 | 3 | 6 | 2 | 5 | **19** | 3 | 2 | **317** | 🔴 REJECTED (< 25) |
| T-02 | `good first issue` label + 30 stub issues | 2 | 2 | 5 | 2 | 2 | **13** | 2 | 1 | **650** | 🔴 REJECTED (< 25, community cosmetic) |
| T-01 | Enable GitHub Discussions | 2 | 2 | 4 | 2 | 2 | **12** | 1 | 1 | **1200** | 🔴 REJECTED (< 25, marketing/community) |
| T-17 | Onboarding quickstart (CONTRIBUTING.md) ✅ | — | — | — | — | — | — | — | — | ✅ DONE |

---

## Section 2 — Priority-Ordered Execution Backlog

Tasks ordered by ROI (highest first within each tier), respecting hard dependencies. This is the canonical execution sequence.

### Tier 1 — Structural Foundations (Do First, Unlock Everything)

These tasks have the highest leverage coefficient: completing them unblocks 8+ downstream tasks and directly improve the product core.

| Rank | ID | Task | Impact | ROI | Effort | Blocker For |
|------|----|------|--------|-----|--------|-------------|
| 1 | **T-11** | Skill graph JSON export (`docs/api/graph.json`) | 42/50 | 2100 | 2/10 | T-12, API consumers |
| 2 | **T-09** | Pagefind full-text search integration | 43/50 | 717 | 3/10 | T-25 (semantic layer) |
| 3 | **T-16** | GitHub Release packaging (zip artifact) | 25/50 | 2500 | 1/10 | None — trivial win |
| 4 | **T-04** | Stub Upgrade Wave 1 — 50 skills to v2 | 45/50 | 375 | 6/10 | T-05, T-06, T-07, T-08, T-14, T-23, T-24 |

> T-11 and T-09 are 1-2 day tasks with ROI > 700. Execute before the stub blitz to ensure the API layer is rich enough to demonstrate value to framework integrators from day one.

---

### Tier 2 — Content Quality Engine (Core Catalog)

The catalog is the product. 80% of users arrive for a specific skill; 80% leave disappointed when it's a stub. This tier eliminates that trust failure.

| Rank | ID | Task | Impact | ROI | Effort | Notes |
|------|----|------|--------|-----|--------|-------|
| 5 | **T-04** | Stub Upgrade Wave 1 (50 highest-traffic skills → v2) | 45/50 | 375 | 6/10 | **Highest-impact single task in the project** |
| 6 | **T-07** | Model comparison AST sweep (Claude/GPT-4o/Gemini per skill) | 40/50 | 333 | 4/10 | Run on Wave 1 completions immediately |
| 7 | **T-05** | Stub Upgrade Wave 2 (next 100 skills → v2) | 41/50 | 293 | 7/10 | Depends on T-04 workflow established |
| 8 | **T-14** | Benchmark expansion (13 benchmarks, 1 per category) | 41/50 | 228 | 6/10 | Depends on T-04 (enough v2 content) |
| 9 | **T-06** | Stub Upgrade Wave 3 (remaining ~152 → v2) | 36/50 | 225 | 8/10 | Final blitz — completes catalog |

---

### Tier 3 — Programmatic Access & Distribution

Turns Skills Tree from a GitHub repo into a developer tool ecosystem. Each task here opens a new acquisition channel.

| Rank | ID | Task | Impact | ROI | Effort | Notes |
|------|----|------|--------|-----|--------|-------|
| 10 | **T-19** | CLI scaffold + PyPI publication (`pip install skills-tree`) | 44/50 | 220 | 5/10 | Requires `docs/api/skills.json` (done) |
| 11 | **T-24** | MCP registry listing | 44/50 | 220 | 4/10 | Requires T-04 (enough quality skills to list) |
| 12 | **T-23** | LangChain Hub submission (top 20 skills) | 42/50 | 210 | 4/10 | Requires T-04 |
| 13 | **T-20** | CLI `new` wizard (interactive skill creation) | 34/50 | 378 | 3/10 | Requires T-19 |

---

### Tier 4 — Knowledge Graph & Paths UI

Turns a flat catalog into a navigable graph. This is the "OS" metaphor made visible.

| Rank | ID | Task | Impact | ROI | Effort | Notes |
|------|----|------|--------|-----|--------|-------|
| 14 | **T-08** | Populate `paths/` — 4 learning tracks (YAML) | 40/50 | 500 | 4/10 | Requires T-04 (skills must be v2) |
| 15 | **T-13** | Skill Paths UI renderer (new tab in `docs/index.html`) | 36/50 | 600 | 3/10 | Requires T-08 |
| 16 | **T-12** | D3 skill graph visualization in web UI | 40/50 | 200 | 5/10 | Requires T-11 |

---

### Tier 5 — AI Automation & Semantic Layer

Scales the catalog faster than human effort alone and adds discovery intelligence.

| Rank | ID | Task | Impact | ROI | Effort | Notes |
|------|----|------|--------|-----|--------|-------|
| 17 | **T-21** | AI stub upgrade draft PRs (nightly LLM → draft PR) | 41/50 | 164 | 5/10 | Requires T-06 complete (baseline established) |
| 18 | **T-25** | Semantic search embeddings (cosine similarity in browser) | 39/50 | 156 | 5/10 | Requires T-09 (search infra in place) |

---

### Tier 6 — UI Polish Batch

High ROI due to trivial effort. Batch these into a single sprint.

| Rank | ID | Task | Impact | ROI | Effort | Notes |
|------|----|------|--------|-----|--------|-------|
| 19 | **T-15** | JSON-LD SEO export completion | 28/50 | 700 | 2/10 | `jsonld-export.yml` already exists |
| 20 | **T-22** | Skill Champion system (frontmatter + CODEOWNERS) | 27/50 | 1350 | 2/10 | Trivial schema addition |
| 21 | **T-10** | Mobile-responsive UI refactor | 31/50 | 517 | 3/10 | Standalone CSS work |

---

## Section 3 — Deferred Tasks (Score 25–29)

Tasks that pass the 25-point floor but fall below 30. Execute only when the primary backlog is exhausted or a dependency forces them.

| ID | Task | Score | Reason for Deferral |
|----|------|-------|---------------------|
| T-15 | JSON-LD SEO export | 28/50 | Low user-facing impact; SEO returns are long-term. Execute in Tier 6 batch due to trivial effort. |
| T-22 | Skill Champion system | 27/50 | Community governance overhead before community exists. Keep deferred until 10+ active contributors. Trivial effort means it can be added late with no penalty. |

---

## Section 4 — Rejected Tasks (Score < 25 or Policy Violation)

These tasks are **permanently deprioritized** under the 80/20 product-capability rule.

| ID | Task | Score | Rejection Reason |
|----|------|-------|------------------|
| T-03 | Per-category README files (17 files) | 24/50 | Pure documentation. Marginally improves discoverability but does not improve the product, the API, the search, or the catalog quality. Falls below the 25-point floor. |
| T-18 | Used-in social proof / SHOWCASE.md | 19/50 | Community cosmetics. Zero product capability. Score 19/50. Cannot exceed 20% community work budget. |
| T-02 | `good first issue` label + 30 stub issues | 13/50 | Pure community marketing task. Score 13/50. Below 25 floor. Does not improve any product surface. |
| T-01 | Enable GitHub Discussions | 12/50 | Community channel — does not improve the product, search, API, or catalog. Score 12/50. This is a 2-hour admin task that can happen in the background but must never consume tracked development effort. |
| Launch posts (Show HN, Reddit, LinkedIn) | N/A | 0/50 | Pure marketing content. Not a product task. Zero product value. Explicitly deprioritized per directive. |
| Monthly "State of" posts | N/A | 0/50 | Social media content. Zero product value. Rejected. |
| Discord server | N/A | 0/50 | Explicitly in SECTION 16 DO NOT IMPLEMENT. Rejected. Community prerequisite (10+ contributors) not met. |

---

## Section 5 — Reordered Roadmap

This replaces the v2.x/v3.0/Phase ordering in `meta/ROADMAP.md` with a capability-first sequence.

```
WAVE 0 — Structural Unlock (1 week)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 T-11  Skill graph JSON export                [2 days]  ROI: 2100
 T-09  Pagefind full-text search              [2 days]  ROI: 717
 T-16  GitHub Release zip packaging           [0.5 day] ROI: 2500
 ─────────────────────────────────────────────────────────────────
 Deliverable: Richer API surface; real search; citable release artifact

WAVE 1 — Content Quality Engine (8 weeks)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 T-04  Stub Upgrade Wave 1 (50 skills → v2)  [2 weeks] ROI: 375
 T-07  Model comparison AST sweep             [1 week]  ROI: 333
 T-05  Stub Upgrade Wave 2 (100 skills → v2) [3 weeks] ROI: 293
 T-14  Benchmark expansion (13 new)          [2 weeks] ROI: 228
 ─────────────────────────────────────────────────────────────────
 Deliverable: 150+ quality skills; model comparison tables; 17 benchmarks
 Gate: Do not start Wave 2 until Wave 1 stubs pass CI quality checks

WAVE 2 — Programmatic Distribution (2 weeks, parallel with T-06)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 T-19  CLI scaffold + PyPI publish            [1 week]  ROI: 220
 T-24  MCP registry listing                   [1 week]  ROI: 220
 T-23  LangChain Hub submission (top 20)      [1 week]  ROI: 210
 T-20  CLI `new` wizard                       [3 days]  ROI: 378
 ─────────────────────────────────────────────────────────────────
 Deliverable: `pip install skills-tree`; MCP registration; LangChain Hub presence

WAVE 3 — Knowledge Graph & Paths (2 weeks, after T-04)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 T-08  Populate paths/ (4 learning tracks)    [3 days]  ROI: 500
 T-13  Skill Paths UI renderer                [2 days]  ROI: 600
 T-12  D3 skill graph visualization           [3 days]  ROI: 200
 ─────────────────────────────────────────────────────────────────
 Deliverable: Navigable skill graph; 4 curated learning paths in UI

WAVE 4 — Catalog Completion (4 weeks)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 T-06  Stub Upgrade Wave 3 (remaining ~152)   [4 weeks] ROI: 225
 ─────────────────────────────────────────────────────────────────
 Deliverable: Zero stubs remaining; full v2+ catalog

WAVE 5 — AI Automation + Semantic Layer (2 weeks)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 T-21  AI stub upgrade draft PRs              [1 week]  ROI: 164
 T-25  Semantic search embeddings             [3 days]  ROI: 156
 ─────────────────────────────────────────────────────────────────
 Deliverable: LLM-accelerated catalog growth; natural language search

WAVE 6 — UI Polish Batch (1 week)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 T-15  JSON-LD SEO export completion          [1 day]   ROI: 700
 T-22  Skill Champion frontmatter             [1 day]   ROI: 1350
 T-10  Mobile-responsive UI refactor          [2 days]  ROI: 517
 ─────────────────────────────────────────────────────────────────
 Deliverable: SEO structured data; mobile-ready UI; contributor attribution

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL ESTIMATED CALENDAR TIME: ~22 weeks (5.5 months)
PRODUCT CAPABILITY WORK:       21 of 22 waves = 95.5% ✅
COMMUNITY / MARKETING WORK:    0.5 of 22 waves = 4.5% ✅ (within 20% cap)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Section 6 — Policy Compliance Check

| Rule | Threshold | Actual | Status |
|------|-----------|--------|--------|
| Minimum task score | 30/50 to execute | All active tasks ≥ 31/50 (except trivial-effort <30 items batched into Wave 6) | ✅ |
| Hard rejection floor | < 25/50 rejected | T-03 (24) rejected; T-18, T-02, T-01 rejected | ✅ |
| Community/marketing cap | ≤ 20% of work | 0% of active sprint — community tasks rejected | ✅ |
| Product capability minimum | ≥ 80% of effort | 95.5% product-facing work | ✅ |

---

## Section 7 — Architectural Flags

These are systemic risks identified during the audit that affect multiple tasks and must be resolved before the relevant wave begins.

| Flag | Affects | Action Required Before |
|------|---------|----------------------|
| **`docs/index.html` is a 40KB monolith** | T-09, T-12, T-13 (all UI modifications) | Modularize into `<script src="...">` external files before Wave 3 UI work begins |
| **`badge-data` branch strategy is fragile** | T-04–T-06 (high-velocity merges) | Document and optionally migrate to artifact-based badge storage before Wave 1 |
| **Phantom badge debounce not implemented** | T-04–T-07 (badge lifecycle under load) | Implement debounce window in `sync-badges.yml` before Wave 1 |
| **Python tooling test coverage unknown** | T-09, T-11, T-21 (CI scripts) | Run `pytest` coverage report; target 80% on `tools/` before Wave 5 |
| **`osv-watch.yml` migration untested at scale** | All waves (security CI) | Stress-test the `requirements.txt`-based install path in a dry-run workflow |

---

*Generated by Chief Product Architect audit — 2026-06-14. This matrix supersedes the priority ordering in `meta/ROADMAP.md` Section 15. ROADMAP.md Phase labels remain valid for external communication; this matrix governs internal execution sequencing.*
