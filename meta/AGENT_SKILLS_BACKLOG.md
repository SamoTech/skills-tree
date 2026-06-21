# AGENT SKILLS BACKLOG

**Version:** R-01 (Governance Recovery)  
**Date:** 2026-06-21  
**Source:** PROJECT_MEMORY.md (Sections 3, 5, 14, 15) — verified as governing document  
**Previous file state:** PLACEHOLDER (19 bytes) — all prior content voided  

> Backlog items are derived only from observed gaps in the repository as documented
> in PROJECT_MEMORY.md. No items have been invented. Every item references its source.

---

## CRITICAL BLOCKERS (resolve first)

| ID | Item | Evidence of Gap | Unblocks |
|---|---|---|---|
| B-001 | **`data/SKILLS_GRAPH.json` is a placeholder** | TASK-000A audit; file = 24 bytes | All graph tasks (T-11, T-12, graph-dependent features) |
| B-002 | **`meta/PROJECT_CONSTITUTION.md` is missing** | VERIFIED_BASELINE_V2.md Section 8 | All tasks referencing the Constitution |
| B-003 | **Governance files were placeholders** | TASK-000A audit | Agent session continuity |

---

## P0 BACKLOG — CRITICAL (blocks growth)

*Source: PROJECT_MEMORY.md Section 5 (P0 features) and Section 15 (task sequence)*

### B-P0-01 — Enable GitHub Discussions
- **Task ID:** T-01
- **Effort:** 2 hours
- **Dependencies:** None
- **Gap evidence:** PROJECT_MEMORY.md Section 12: "No GitHub Discussions"; Section 3: listed as missing feature
- **Value:** Opens community loop; enables contributor engagement; unblocks T-02, T-18, T-22

### B-P0-02 — Tag 30 Stubs as `good first issue`
- **Task ID:** T-02
- **Effort:** 3 hours
- **Dependencies:** T-01
- **Gap evidence:** PROJECT_MEMORY.md Section 3 UX Issues: no guided entry for contributors
- **Value:** Community onramp; creates visible contribution opportunities

### B-P0-03 — Stub Upgrade Wave 1 (50 v1→v2)
- **Task ID:** T-04
- **Effort:** 2 weeks
- **Dependencies:** `meta/skill-template.md` (verified exists)
- **Gap evidence:** PROJECT_MEMORY.md Section 2: ~302 of 377 skills (~80%) are v1 stubs
- **Value:** Eliminates the #1 trust killer; unlocks T-05, T-06, T-07, T-08, T-23, T-24

### B-P0-04 — Stub Upgrade Wave 2 (100 v1→v2)
- **Task ID:** T-05
- **Effort:** 3 weeks
- **Dependencies:** T-04
- **Gap evidence:** Same as B-P0-03
- **Value:** Continues stub elimination; required before benchmark expansion

### B-P0-05 — Stub Upgrade Wave 3 (~152 remaining stubs)
- **Task ID:** T-06
- **Effort:** 4 weeks
- **Dependencies:** T-05
- **Gap evidence:** Same as B-P0-03
- **Value:** Completes stub blitz; unlocks AI draft PR automation (T-21)

### B-P0-06 — Model Comparison AST Sweep
- **Task ID:** T-07
- **Effort:** 1 week
- **Dependencies:** T-04 (need enough v2 skills)
- **Gap evidence:** PROJECT_MEMORY.md Section 3: "most skills lack Claude/GPT-4o/Gemini table"; listed as top-requested feature
- **Value:** Makes content immediately actionable; `ast-sweep.yml` already exists

### B-P0-07 — Populate `paths/` with 4 Learning Tracks
- **Task ID:** T-08
- **Effort:** 3 days
- **Dependencies:** T-04
- **Gap evidence:** PROJECT_MEMORY.md Section 3: "`paths/` directory empty or undeveloped"; Section 2 weakness list item 11
- **Value:** Dramatically improves discoverability and SEO; creates first-timer friendly entry point

---

## P1 BACKLOG — HIGH PRIORITY

### B-P1-01 — Per-Category README.md Files (17 dirs)
- **Task ID:** T-03
- **Effort:** 1 day
- **Dependencies:** None
- **Gap evidence:** PROJECT_MEMORY.md Section 3: "Category README files missing for most categories"
- **Value:** GitHub renders these automatically; improves per-category discoverability

### B-P1-02 — Pagefind/FlexSearch Full-Text Search
- **Task ID:** T-09
- **Effort:** 2 days
- **Dependencies:** None
- **Gap evidence:** PROJECT_MEMORY.md Section 3: "`generate-search-index.yml` exists but client-side integration needs verification"
- **Value:** Replaces substring match; full-text indexing of skill content

### B-P1-03 — Mobile-Responsive UI Refactor
- **Task ID:** T-10
- **Effort:** 2 days
- **Dependencies:** None
- **Gap evidence:** PROJECT_MEMORY.md Section 2 weakness #4; Section 3 UX Issues: "No mobile-optimized UI"
- **Value:** Opens access to mobile developers; reduces bounce rate

### B-P1-04 — Skill Graph JSON Export (`docs/api/graph.json`)
- **Task ID:** T-11
- **Effort:** 1 day
- **Dependencies:** None (but `build-graph.yml` must be working)
- **Gap evidence:** PROJECT_MEMORY.md Section 3: "Interactive skill graph — `build-graph.yml` exists but UI does not render it"
- **Value:** Unblocks D3 visualization (T-12); enables programmatic skill relationship queries

### B-P1-05 — D3 Skill Graph Visualization
- **Task ID:** T-12
- **Effort:** 3 days
- **Dependencies:** T-11
- **Gap evidence:** Same as B-P1-04
- **Value:** Highly shareable; demonstrates the "OS" metaphor visually

### B-P1-06 — Skill Paths Web UI Renderer
- **Task ID:** T-13
- **Effort:** 2 days
- **Dependencies:** T-08 (paths content must exist first)
- **Gap evidence:** PROJECT_MEMORY.md Section 3: "Skill Paths — `paths/` directory exists but is empty"
- **Value:** Guided learning experience; SEO long-tail content

### B-P1-07 — Benchmark Expansion (13 new benchmarks)
- **Task ID:** T-14
- **Effort:** 2 weeks
- **Dependencies:** T-04
- **Gap evidence:** PROJECT_MEMORY.md Section 2: "Benchmark coverage thin: Only 4 benchmarks for 377+ skills"
- **Value:** Each benchmark is highly linkable and shareable; academic citation potential

### B-P1-08 — Skill Champion System
- **Task ID:** T-22
- **Effort:** 2 days
- **Dependencies:** T-01
- **Gap evidence:** PROJECT_MEMORY.md Section 3: "Skill Champion system — no formal ownership role for contributors"
- **Value:** Distributes maintenance load; incentivizes sustained contribution

### B-P1-09 — CLI Tool (`pip install skills-tree`)
- **Task ID:** T-19
- **Effort:** 1 week
- **Dependencies:** `docs/api/skills.json` (verified exists)
- **Gap evidence:** PROJECT_MEMORY.md Section 2 weakness #6: "No `skills-tree` CLI published to PyPI"
- **Value:** Puts Skills Tree in every developer's terminal; PyPI discoverability

### B-P1-10 — CLI `new` Wizard
- **Task ID:** T-20
- **Effort:** 3 days
- **Dependencies:** T-19
- **Gap evidence:** Part of complete CLI experience (PROJECT_MEMORY.md Section 5 P1-1)
- **Value:** Removes contribution friction; interactive skill scaffolding

### B-P1-11 — Used-In Social Proof / SHOWCASE.md
- **Task ID:** T-18
- **Effort:** 1 week
- **Dependencies:** T-01
- **Gap evidence:** PROJECT_MEMORY.md Section 2 weakness #13: "No real-world usage data"
- **Value:** Each submission is a social amplifier; `used-in-tracker.yml` already exists

---

## P2 BACKLOG — MEDIUM PRIORITY

### B-P2-01 — JSON-LD SEO Injection Completion
- **Task ID:** T-15
- **Effort:** 1 day
- **Dependencies:** `jsonld-export.yml` (verified exists)
- **Gap evidence:** PROJECT_MEMORY.md Section 3: "`jsonld-export.yml` exists but SEO metadata injection needs completion"
- **Value:** Structured data; skill pages rank in Google for agent queries

### B-P2-02 — GitHub Release Packages (Zipped Skill Index)
- **Task ID:** T-16
- **Effort:** 1 day
- **Dependencies:** Export scripts (verified exist)
- **Gap evidence:** PROJECT_MEMORY.md Section 3: "no zipped skill index as a GitHub Release asset"
- **Value:** Offline use; citable artifact for researchers

### B-P2-03 — Onboarding Quickstart
- **Task ID:** T-17
- **Effort:** 1 day
- **Dependencies:** None
- **Gap evidence:** PROJECT_MEMORY.md Section 3 Documentation Gaps item 3: "No onboarding tutorial"
- **Value:** Reduces contributor drop-off at first PR

### B-P2-04 — LangChain Hub Submission (Top 20 Skills)
- **Task ID:** T-23
- **Effort:** 1 week
- **Dependencies:** T-04
- **Gap evidence:** PROJECT_MEMORY.md Section 2 weakness #8: "Framework integration absent"
- **Value:** Massive distribution channel; immediate credibility signal

### B-P2-05 — MCP Registry Listing
- **Task ID:** T-24
- **Effort:** 1 week
- **Dependencies:** T-04
- **Gap evidence:** PROJECT_MEMORY.md Section 5 P2-2
- **Value:** Future-proofs the project; early-mover advantage in agentic protocols

### B-P2-06 — AI Stub Upgrade Draft PRs (Nightly LLM)
- **Task ID:** T-21
- **Effort:** 1 week
- **Dependencies:** T-06, LLM API key
- **Gap evidence:** PROJECT_MEMORY.md Section 11: "AI-Powered Stub Upgrade Drafts (High Impact)" — not yet implemented
- **Value:** Accelerates stub-to-v2 pipeline; reduces human effort per upgrade

### B-P2-07 — Verify Automated Changelog Activation
- **Effort:** Low
- **Gap evidence:** PROJECT_MEMORY.md Section 3 Technical Debt: "`generate-changelog.yml` exists but effectiveness not verified in production"
- **Value:** Reduces maintainer toil; demonstrates active development

---

## P3 BACKLOG — FUTURE

| Item | Task ID | Evidence of Need | Effort |
|---|---|---|---|
| Semantic search (pre-computed embeddings) | T-25 | PROJECT_MEMORY.md Section 9 Phase 3 | 3d |
| GraphQL API (Cloudflare Worker) | T-P3-1 | PROJECT_MEMORY.md Section 5 P3-1 | Very High |
| Skill Playground (WASM in-browser) | T-P3-3 | PROJECT_MEMORY.md Section 5 P3-3 | Very High |
| "Ask Skills Tree" RAG chatbot | T-P3-7 | PROJECT_MEMORY.md Section 11 Opportunity 7 | Very High |
| Enterprise Skill Packs | T-P3-6 | PROJECT_MEMORY.md Section 5 P3-6 | High |
| Skills Certification Program | T-P3-2 | PROJECT_MEMORY.md Section 5 P3-2 | Very High |
| Multilingual skill content (5 languages) | T-P3-5 | PROJECT_MEMORY.md Section 5 P3-5 | Very High |
| AI Emerging Skills Detector | T-P3-4 | PROJECT_MEMORY.md Section 11 Opportunity 6 | Very High |

---

## TECHNICAL DEBT BACKLOG

*Source: PROJECT_MEMORY.md Section 3 Technical Debt*

| Item | Severity | Evidence |
|---|---|---|
| `docs/index.html` is a 40KB monolith — no build pipeline | Medium | PROJECT_MEMORY.md Section 3 |
| 30 workflows is high maintenance surface — overlap between `stale.yml` + `stale-skills.yml`, `heartbeat.yml` + `keepalive.yml` | Low | PROJECT_MEMORY.md Section 3 |
| Phantom badge window — debounce fix not yet implemented | Low | PROJECT_MEMORY.md Section 3 |
| Python scripts lack unified test runner — coverage unknown | Medium | PROJECT_MEMORY.md Section 3 |
| `meta/QUALITY-REPORT.md` is 68KB — renders slowly | Low | PROJECT_MEMORY.md Section 3 |
| `badge-data` branch strategy is non-standard and fragile | Low | PROJECT_MEMORY.md Section 3 |

---

## DOCUMENTATION GAPS

*Source: PROJECT_MEMORY.md Section 3 Documentation Gaps*

| Gap | Priority |
|---|---|
| No `ARCHITECTURE.md` — no ADR document | P2 |
| `paths/` has no README explaining its purpose | P2 |
| No 5-minute quickstart for first-time contributors | P2 |
| Category-level READMEs missing for 17 directories | P1 (Task T-03) |
| API documentation lacking — no Swagger/OpenAPI reference | P3 |
| `generate-changelog.yml` effectiveness unverified | P2 |

---

*This backlog was rebuilt from PROJECT_MEMORY.md during Mission R-01 on 2026-06-21.*
*Add items only when a gap can be proven from repository files or commit history.*
*Mark items complete only when a verified commit closes the gap.*
