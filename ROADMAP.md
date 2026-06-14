# ROADMAP.md — Skills Tree

> **Executable Sprint Roadmap** | Derived from `PROJECT_MEMORY.md`
> Repository: [https://github.com/SamoTech/skills-tree](https://github.com/SamoTech/skills-tree)
> Generated: 2026-06-14 | Maintainer: @SamoTech
> Current Version: v2.2 → Target: v3.0 (Q4 2026)

---

## Overview

This roadmap converts the full product backlog from `PROJECT_MEMORY.md` into 7 independently executable sprints. Each sprint has a clear scope boundary, defined deliverables, explicit dependencies, risk register, and measurable success metrics. No sprint requires a prior sprint to be in flight simultaneously — each can be picked up and executed in isolation.

**Sprint Calendar**

| Sprint | Theme | Duration | Target Version |
|--------|-------|----------|---------------|
| Sprint 1 | Community Foundation | 1 week | v2.3 |
| Sprint 2 | Content Infrastructure | 2 weeks | v2.4 |
| Sprint 3 | Stub Upgrade Wave 1 | 2 weeks | v2.5 |
| Sprint 4 | Stub Upgrade Wave 2 | 3 weeks | v2.6 |
| Sprint 5 | UI & Search Overhaul | 2 weeks | v2.7 |
| Sprint 6 | CLI & API Expansion | 2 weeks | v2.8 |
| Sprint 7 | AI Automation & Integrations | 3 weeks | v3.0 |

---

## Sprint 1 — Community Foundation

**Theme:** Open the community loop. Zero engineering required. Highest ROI per hour spent.
**Duration:** 1 week
**Target Version:** v2.3

### Milestone
Enable async community engagement so external contributors can begin participating before content work completes.

### Deliverables

| ID | Deliverable | Task Ref | Effort |
|----|-------------|----------|--------|
| D1-1 | GitHub Discussions enabled with 5 categories (Ideas, Benchmarks, Q&A, Showcase, Roadmap) | T-01 | 2h |
| D1-2 | Pinned "Start Here" discussion with contribution guide, current priorities, and first-issue links | T-01 | 1h |
| D1-3 | `good first issue` label created; 30+ stub files tagged as first-issue targets with linked issues | T-02 | 3h |
| D1-4 | `CONTRIBUTING.md` updated with "5-minute first contribution" quickstart section | T-17 | 1d |
| D1-5 | Initial launch announcement drafted (Show HN + Reddit r/MachineLearning) | — | 3h |
| D1-6 | Sponsor CTA added to GitHub Pages UI (visible above-the-fold) | — | 2h |

### Dependencies

- **None.** Sprint 1 is the entry point with zero upstream dependencies.
- Requires: admin access to the repository to toggle Discussions.
- Requires: GitHub token with `issues:write` scope for bulk issue filing.

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Discussions enabled but no engagement arrives | High | Medium | Pre-seed with 3–5 self-authored posts to remove "empty room" effect before announcing |
| Good-first-issue flood overwhelms @SamoTech | Low | High | Cap at 30 issues; set response SLA expectation in the pinned post |
| Launch announcement gets no traction | Medium | Low | Plan 2nd post after Sprint 3 when content quality is significantly higher |

### Success Metrics

- [ ] GitHub Discussions enabled and visible
- [ ] ≥ 30 issues labeled `good first issue`
- [ ] CONTRIBUTING.md quickstart section live
- [ ] ≥ 1 external comment or reaction within 7 days of launch post

---

## Sprint 2 — Content Infrastructure

**Theme:** Build the scaffolding that makes all content work in Sprint 3–4 coherent and discoverable.
**Duration:** 2 weeks
**Target Version:** v2.4

### Milestone
Every category directory has a landing page; the `paths/` directory has a defined structure; the data model for Skill Paths is finalized and ready for population.

### Deliverables

| ID | Deliverable | Task Ref | Effort |
|----|-------------|----------|--------|
| D2-1 | `README.md` added to all 17 category directories (200-word description, skill list, badges) | T-03 | 1d |
| D2-2 | `paths/` directory `README.md` written — purpose, format spec, contribution guide | — | 2h |
| D2-3 | 4 Skill Path YAML files scaffolded: Research Agent, Memory-First, Computer Use, Zero-to-Production | T-08 (partial) | 3d |
| D2-4 | `docs/api/paths.json` export target defined in `export-skills.yml` (schema only; data populated in Sprint 3) | — | 1d |
| D2-5 | `ARCHITECTURE.md` created — ADR document for directory structure, technology choices, and design constraints | — | 1d |
| D2-6 | Per-skill `champion` field added to `meta/skill-schema.json` and validated in `schema-enforce.yml` | T-22 | 2d |
| D2-7 | `used-in` issue template reviewed; `SHOWCASE.md` stub file created | T-18 (partial) | 2h |
| D2-8 | GitHub Release CI step added to `export-skills.yml` — zips skill index on version tag push | T-16 | 1d |

### Dependencies

- D2-3 depends on D2-1 — paths must reference valid category README files.
- D2-4 depends on D2-3 — schema mirrors the path YAML structure.
- D2-6 depends on Sprint 1 → D1-1 (Discussions must be live for champion nomination flow).

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Category READMEs written hastily and contain inaccurate skill lists | Medium | Medium | Use `tools/check_skill_quality.py` output to enumerate skills per category programmatically |
| Skill Path YAML format designed now conflicts with future UI needs | Medium | High | Design the YAML to match the data model spec in SECTION 7 of PROJECT_MEMORY.md exactly; treat it as frozen after this sprint |
| Schema change for `champion` field breaks existing PRs in flight | Low | Medium | Make field optional (not required) in JSON Schema draft-07 definition |

### Success Metrics

- [ ] All 17 category `README.md` files merged to `main`
- [ ] `paths/README.md` live with format specification
- [ ] 4 Skill Path YAML stubs committed (structure complete, skills list may be partial)
- [ ] `ARCHITECTURE.md` merged
- [ ] `champion` field validated by `schema-enforce.yml` in CI
- [ ] GitHub Release zip generated on next version tag push

---

## Sprint 3 — Stub Upgrade Wave 1

**Theme:** Eliminate the #1 trust killer. Every page becomes useful.
**Duration:** 2 weeks
**Target Version:** v2.5

### Milestone
50 of the highest-visibility v1 stub skills upgraded to v2 minimum: real runnable code example, documented failure modes, populated `related_skills`, and at least one framework compatibility entry.

### Deliverables

| ID | Deliverable | Task Ref | Effort |
|----|-------------|----------|--------|
| D3-1 | 50 v1 stubs upgraded to v2 standard (prioritized by category traffic and `related_skills` link density) | T-04 | 2w |
| D3-2 | Model comparison table template verified against `ast-sweep.yml` — sweep run on all 50 upgraded skills | T-07 (partial) | 1d |
| D3-3 | 4 Skill Path YAML files fully populated using the newly upgraded skills | T-08 | 2d |
| D3-4 | 5+ "Used In" submissions solicited from the community via the Discussions Showcase category | T-18 | 1w |

### Selection Criteria for Wave 1 Skills

Prioritize stubs that:
1. Are referenced by `related_skills` in other files (highest dependency weight)
2. Fall in categories with the most existing v2/v3 skills (context for consistent style)
3. Are tagged as `good first issue` targets already (validates the contribution pipeline)
4. Belong to the 5 most-searched agent capability categories (memory, RAG, tool use, planning, communication)

### Dependencies

- D3-1 depends on Sprint 2 → D2-1 (category READMEs provide context for writing upgrades).
- D3-3 depends on Sprint 2 → D2-3 (path YAML stubs must exist before population).
- D3-4 depends on Sprint 1 → D1-1 (Discussions must be live to solicit submissions).

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| 50 upgrades in 2 weeks is too aggressive for 1 person | High | High | Scope to 30 if velocity data shows overrun after week 1; defer 20 to Sprint 4 |
| Code examples in upgraded skills are not runnable (LLM-generated hallucinations) | Medium | High | Every code example must be locally executed before PR merge; no untested pseudocode |
| `quality-report.yml` blocks PRs for policy reasons mid-upgrade | Medium | Medium | Review current quality gate thresholds before starting; temporarily adjust stub block policy if needed |
| Community "Used In" submissions don't arrive | High | Low | Proactively reach out to 5 known AI agent projects with a direct DM/email |

### Success Metrics

- [ ] ≥ 50 skills upgraded from v1 → v2 (merged to `main`)
- [ ] `QUALITY-REPORT.md` shows v2+ count ≥ 98 (48 existing + 50 new)
- [ ] All 4 Skill Paths fully populated and committed to `paths/`
- [ ] `ast-sweep.yml` model comparison pass completes with ≥ 50 skills updated
- [ ] ≥ 1 "Used In" submission in `SHOWCASE.md`

---

## Sprint 4 — Stub Upgrade Wave 2

**Theme:** Reach the content threshold where the catalog becomes self-reinforcing.
**Duration:** 3 weeks
**Target Version:** v2.6

### Milestone
All 302 v1 stubs upgraded to v2 minimum. Benchmark coverage reaches 1 per category (17 total). The repository crosses the "majority content is useful" threshold.

### Deliverables

| ID | Deliverable | Task Ref | Effort |
|----|-------------|----------|--------|
| D4-1 | Next 100 stubs upgraded to v2 (Wave 2) | T-05 | 3w |
| D4-2 | Remaining ~152 stubs upgraded to v2 (Wave 3) | T-06 | 4w (may overlap with Sprint 5) |
| D4-3 | 13 new benchmark files written — 1 per category currently missing a benchmark | T-14 | 2w |
| D4-4 | Category 17 (Infrastructure) expanded from 1 to 15+ skills | T — P2-8 | 1w |
| D4-5 | Full model comparison AST sweep run across all v2+ skills post-Wave 3 | T-07 | 1w |
| D4-6 | Onboarding tutorial added to web UI landing page ("Start Here" path for visitors) | T-17 partial | 1d |

> **Note on D4-2:** If Wave 3 (152 stubs) cannot complete within Sprint 4, the overflow carries into Sprint 5 as a parallel track. Sprint 5 has no hard dependency on D4-2 completion.

### Dependencies

- D4-1 depends on Sprint 3 → D3-1 (Wave 1 must be complete to establish consistent upgrade style).
- D4-3 depends on Sprint 3 → D3-1 (benchmark files reference skills that must be at v2+).
- D4-5 depends on D4-1 and D4-2 (sweep runs after the majority of stubs are upgraded).
- D4-6 depends on Sprint 1 → D1-4 (builds on the quickstart section already in CONTRIBUTING.md).

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| 252 upgrades across 3 weeks exceeds solo capacity | Very High | High | Activate the `good first issue` campaign from Sprint 1 to offload upgrades to community contributors; @SamoTech reviews rather than writes |
| Benchmark quality is inconsistent across 13 categories | Medium | Medium | Use `meta/benchmark-template.md` strictly; require a reproducibility script with every benchmark |
| AST sweep injects incorrect model comparison data | Medium | High | Run sweep on 5 test files first; validate output manually before full batch |
| `QUALITY-REPORT.md` (68KB) performance degrades further | Low | Low | Add summary view or pagination stub as a P2 task; document in KNOWN-LIMITATIONS.md |

### Success Metrics

- [ ] ≥ 250 additional skills upgraded to v2 (total ≥ 300 v2+ skills across the catalog)
- [ ] Benchmark count reaches ≥ 17 (1 per category)
- [ ] Category 17 has ≥ 15 skill files
- [ ] Model comparison table present in ≥ 80% of all v2+ skills
- [ ] `QUALITY-REPORT.md` shows stub (v1) count < 30
- [ ] ≥ 5 community-contributed PRs merged (validation that contributor pipeline works)

---

## Sprint 5 — UI & Search Overhaul

**Theme:** Transform the web UI from a static card grid into an interactive, mobile-ready platform.
**Duration:** 2 weeks
**Target Version:** v2.7

### Milestone
The GitHub Pages UI becomes fully mobile-responsive, offers full-text search via Pagefind, renders Skill Paths interactively, and displays the D3.js skill relationship graph.

### Deliverables

| ID | Deliverable | Task Ref | Effort |
|----|-------------|----------|--------|
| D5-1 | `docs/index.html` refactored to mobile-first CSS (1-col mobile, 2-col tablet, 3-col desktop; hamburger nav) | T-10 | 2d |
| D5-2 | Pagefind or FlexSearch integrated for full-text search — replaces substring match; `deploy-pages.yml` updated to build index | T-09 | 2d |
| D5-3 | `build-graph.yml` extended to write `docs/api/graph.json` (nodes = skills, edges = `related_skills` links) | T-11 | 1d |
| D5-4 | D3.js force-directed skill graph added to `docs/index.html` — node click opens skill side-panel | T-12 | 3d |
| D5-5 | Skill Paths tab added to web UI — renders from `docs/api/paths.json`; localStorage "mark complete" per step | T-13 | 2d |
| D5-6 | `docs/index.html` modularized — split into separate JS bundles (graph.js, search.js, paths.js) via light Vite build | — | 2d |
| D5-7 | `jsonld-export.yml` completed — JSON-LD `<script>` tags injected into each skill's GitHub Page | T-15 | 1d |
| D5-8 | Search result ranking updated: v3 > v2 > v1, recency, relevance score | — | 1d |

### Dependencies

- D5-3 must precede D5-4 (graph data must exist before graph UI is built).
- D5-5 depends on Sprint 2 → D2-3 and Sprint 3 → D3-3 (`paths/` YAML must be populated).
- D5-6 should be done last — modularization wraps D5-1 through D5-5 after they are individually validated.
- D5-7 depends on `jsonld-export.yml` existing (confirmed done per PROJECT_MEMORY.md).

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| D3.js graph is too complex / slow for 377+ nodes | Medium | High | Implement virtual rendering; cap initial render to top 100 most-connected skills; add a "load full graph" toggle |
| Pagefind build step significantly increases `deploy-pages.yml` build time | Medium | Low | Benchmark build time; cache Pagefind binary across runs; set a 3-minute timeout alert |
| Vite modularization breaks existing CI/CD pipeline for Pages | Medium | High | Keep a fallback build script; test modular build in a branch before merging to main |
| Mobile refactor breaks existing desktop animations | Medium | Medium | Use CSS feature queries and test on BrowserStack or equivalent before merge |
| GitHub Pages throttling under high-velocity UI rebuild pushes | Low | Low | Documented in KNOWN-LIMITATIONS.md; batch UI commits |

### Success Metrics

- [ ] Web UI passes Lighthouse Mobile score ≥ 85
- [ ] Full-text search returns results from skill body content (not just frontmatter)
- [ ] Skill graph renders in browser with ≥ 200 nodes visible within 3 seconds
- [ ] Skill Paths tab shows ≥ 4 tracks with working "mark complete" (localStorage)
- [ ] `docs/api/graph.json` is generated by CI on every push
- [ ] `docs/index.html` is split into ≥ 3 separate JS modules
- [ ] JSON-LD tags present on ≥ 90% of skill pages

---

## Sprint 6 — CLI & API Expansion

**Theme:** Put Skills Tree in every developer's terminal. Extend the static API surface.
**Duration:** 2 weeks
**Target Version:** v2.8

### Milestone
`pip install skills-tree` is live on PyPI. The CLI implements `search`, `show`, and `new` commands. Extended API endpoints (`graph.json`, `paths.json`, `stats.json`) are live and documented.

### Deliverables

| ID | Deliverable | Task Ref | Effort |
|----|-------------|----------|--------|
| D6-1 | `skills_tree/` Python package scaffolded with `pyproject.toml`, `setup.cfg`, README, and PyPI classifiers | T-19 | 1d |
| D6-2 | `skills-tree search <query>` command — fetches `docs/api/skills.json` (cached 24h), filters, displays ranked results | T-19 | 2d |
| D6-3 | `skills-tree show <category/skill>` command — renders Markdown to terminal using `rich` | T-19 | 1d |
| D6-4 | `skills-tree new` interactive wizard — prompts for title, category, level; injects `meta/skill-template.md` | T-20 | 3d |
| D6-5 | CLI published to PyPI (`pip install skills-tree`); PyPI badge added to README | T-19 | 1d |
| D6-6 | `docs/api/stats.json` endpoint added — aggregate counts by category, version, battle-tested % | — | 1d |
| D6-7 | `docs/api/leaderboard.json` endpoint added — machine-readable leaderboard data | — | 1d |
| D6-8 | API documentation page added to `docs/` — describes all `/api/` endpoints with example responses | — | 1d |
| D6-9 | `skills-tree search --battle-tested --category <name>` filter flags implemented | — | 1d |
| D6-10 | `skills-tree export --format json > skills.json` command for local tooling | — | 1d |

### Dependencies

- D6-1 through D6-5 depend on `docs/api/skills.json` being populated (confirmed done per PROJECT_MEMORY.md).
- D6-4 depends on Sprint 2 → D2-6 (`champion` field in schema must be finalized before wizard injects it).
- D6-6 and D6-7 depend on Sprint 3 → D3-1 (accurate counts require v2+ upgrade completion).
- D6-8 depends on D6-6 and D6-7 (documents endpoints that must exist first).

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| PyPI package name `skills-tree` already taken | Low | Medium | Check PyPI before building; have fallback names ready (`skillstree`, `ai-skills-tree`) |
| GitHub raw URL rate limiting for CLI cache fetches | Medium | Medium | Bundle a fallback local snapshot of `skills.json` with the package; add `--offline` flag |
| `rich` library version conflicts with user environments | Low | Low | Pin `rich>=13.0` as a minimum; test on Python 3.10, 3.11, 3.12 |
| CLI build pipeline in GitHub Actions needs secrets for PyPI token | Medium | Medium | Set up `PYPI_API_TOKEN` secret in repository settings before Sprint 6 begins |
| `skills-tree new` generates invalid frontmatter | Medium | High | Unit test the wizard output against `meta/skill-schema.json` using `jsonschema` before release |

### Success Metrics

- [ ] `pip install skills-tree` succeeds from PyPI
- [ ] `skills-tree search "memory injection"` returns ≥ 3 relevant results
- [ ] `skills-tree show` renders a skill's Markdown in terminal with syntax highlighting
- [ ] `skills-tree new` produces a file that passes `validate-skills.yml` CI check
- [ ] `docs/api/stats.json` live and reflects accurate counts
- [ ] API documentation page live at `https://samotech.github.io/skills-tree/api/`
- [ ] PyPI badge showing download count visible in `README.md`

---

## Sprint 7 — AI Automation & Integrations

**Theme:** Automate content quality at scale. Embed Skills Tree into the AI ecosystem.
**Duration:** 3 weeks
**Target Version:** v3.0

### Milestone
AI-powered stub upgrade drafts are running in CI. Skills Tree is listed in LangChain Hub and the MCP registry. Semantic search is live. The project is discoverable from every major agent framework.

### Deliverables

| ID | Deliverable | Task Ref | Effort |
|----|-------------|----------|--------|
| D7-1 | GitHub Action for AI-powered stub upgrade drafts — nightly LLM call (Claude/GPT-4o) per remaining stub → draft PR with v2 content | T-21 | 1w |
| D7-2 | Skill Quality Reviewer Bot — GitHub Action reviews incoming skill PRs for quality criteria; posts structured PR review comment | P2-9 | 1w |
| D7-3 | Semantic search embeddings — CI step pre-computes embeddings for all skill descriptions; stored as `docs/api/embeddings.json` | T-25 | 3d |
| D7-4 | Client-side cosine similarity search integrated into web UI — natural language query support | T-25 | 2d |
| D7-5 | Top 20 battle-tested skills converted to LangChain Hub template format and submitted | T-23 | 1w |
| D7-6 | Skills mapped to MCP tool format and registered in official MCP registry | T-24 | 1w |
| D7-7 | `docs/api/benchmarks.json` endpoint added — all benchmark metadata (not full content) | — | 1d |
| D7-8 | Skills Council governance document drafted — 5-member rotating committee, RFC process, Verified Contributor tier spec | — | 1d |
| D7-9 | `SHOWCASE.md` populated with ≥ 5 real-world project entries | T-18 | 1w |
| D7-10 | v3.0 GitHub Release cut — zipped skill index, CHANGELOG, updated README with all new features | T-16 | 1d |

### Dependencies

- D7-1 depends on Sprint 4 → D4-2 (AI drafts target remaining stubs; fewer stubs = cleaner batch).
- D7-1 requires an LLM API key (`OPENAI_API_KEY` or `ANTHROPIC_API_KEY`) set as a repository secret.
- D7-3 and D7-4 depend on Sprint 5 → D5-2 (search infrastructure must be in place; embeddings augment it).
- D7-5 depends on Sprint 3 → D3-1 (LangChain Hub templates must reference v2+ skills).
- D7-6 depends on Sprint 4 → D4-5 (MCP mapping requires stable, tested skill content).
- D7-8 depends on Sprint 1 → D1-1 (Discussions must be active to nominate initial council members).
- D7-10 depends on all prior deliverables being merged to `main`.

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| LLM API costs for nightly stub upgrade drafts exceed budget | High | High | Rate-limit to 10 draft PRs/night; set a monthly spend cap; pause if budget exceeded |
| AI-generated code examples contain bugs / hallucinations | High | High | Add required label `ai-generated` to all draft PRs; block auto-merge; require human review before merge |
| LangChain Hub submission rejected or requires significant format rework | Medium | Medium | Review LangChain Hub submission guidelines before conversion; pilot with 3 skills first |
| MCP registry launch timeline is external dependency beyond our control | High | Medium | Prepare the MCP-formatted skills in `docs/api/mcp/` regardless; submit when registry opens |
| Semantic search embeddings JSON file is too large (all 377+ skills) | Medium | Low | Compress with gzip; lazy-load in browser; cache with Service Worker |
| v3.0 release scope creep delays the cut | Medium | Medium | Define v3.0 as exactly D7-1 through D7-10 with no additions; defer P3 features to v3.5 |

### Success Metrics

- [ ] AI stub upgrade draft PRs running nightly; ≥ 10 draft PRs generated in first week
- [ ] `skills-tree search "retry an API call"` returns semantically relevant results (not just keyword matches)
- [ ] ≥ 5 skills listed and approved on LangChain Hub
- [ ] Skills Tree registered in MCP registry (or submission pending with confirmation)
- [ ] v3.0 GitHub Release published with zipped skill index and CHANGELOG
- [ ] `docs/api/benchmarks.json` live
- [ ] ≥ 5 projects listed in `SHOWCASE.md`
- [ ] Total skills at v2+ exceeds 300
- [ ] Battle-tested (v3) skills count ≥ 50

---

## Cross-Sprint Dependencies Map

```
Sprint 1 (Community)
    └─→ Sprint 2 (champion field schema)
    └─→ Sprint 3 (Discussions for Used-In solicitation)
    └─→ Sprint 7 (Discussions for Skills Council)

Sprint 2 (Infrastructure)
    └─→ Sprint 3 (category READMEs inform upgrade style)
    └─→ Sprint 3 (path YAML stubs ready for population)
    └─→ Sprint 5 (paths.json schema finalized)
    └─→ Sprint 6 (champion field in wizard)

Sprint 3 (Wave 1 Upgrades)
    └─→ Sprint 4 (establishes upgrade style for Wave 2)
    └─→ Sprint 3 (path YAML populated with real v2 skills)
    └─→ Sprint 7 (LangChain Hub templates use Wave 1 v2 skills)

Sprint 4 (Wave 2+3 Upgrades)
    └─→ Sprint 7 (AI drafts target remaining stubs)
    └─→ Sprint 7 (MCP mapping needs stable content)

Sprint 5 (UI & Search)
    └─→ Sprint 7 (semantic search augments Pagefind)

Sprint 6 (CLI & API)
    └─→ Sprint 7 (CLI benchmark run command foundation)
```

---

## Global Risk Register

| ID | Risk | Sprints Affected | Likelihood | Impact | Mitigation |
|----|------|-----------------|-----------|--------|-----------|
| R-01 | Bus factor = 1 (@SamoTech sole human contributor) | All | High | Critical | Activate community contribution from Sprint 1; document every process so others can take over |
| R-02 | LLM API cost overruns | Sprint 7 | High | High | Pre-set monthly budget caps; run smaller batches; use cheaper models for draft quality |
| R-03 | GitHub Pages throttling under high commit velocity | Sprints 3–7 | Medium | Low | Batch commits; document in KNOWN-LIMITATIONS.md; accept as acceptable degradation |
| R-04 | `badge-data` branch strategy fragility | Sprints 3–5 | Medium | Medium | Evaluate migrating to `docs/api/badges.json` in Sprint 2; document in ADR |
| R-05 | Workflow overlap creates double-execution bugs (stale.yml + stale-skills.yml; heartbeat + keepalive) | All | Medium | Low | Audit and consolidate redundant workflows in Sprint 2 as a D2 subtask |
| R-06 | External framework integration timeline slips (MCP registry, LangChain Hub) | Sprint 7 | High | Medium | Decouple preparation from submission; prepare assets independently of external timelines |
| R-07 | Content quality regression if AI-generated PRs auto-merged | Sprint 7 | High | High | Hard rule: zero auto-merge on AI-generated content; always requires human approval |
| R-08 | `meta/QUALITY-REPORT.md` at 68KB causes GitHub rendering issues | Sprints 3–4 | Medium | Low | Generate a summary-only variant alongside the full report in `quality-report.yml` |

---

## Overall Success Metrics (v3.0 Target)

| Metric | Baseline (2026-06-14) | Sprint 3 Gate | Sprint 5 Gate | v3.0 Target |
|--------|----------------------|--------------|--------------|-------------|
| Total skills | 377 | 377 | 377+ | 400+ |
| v2+ skills | 48 | 98+ | 300+ | 350+ |
| Battle-tested (v3) | 27 | 30+ | 40+ | 50+ |
| Contributors | 3 | 5+ | 10+ | 20+ |
| GitHub Stars | Unknown | 50+ | 200+ | 1,000+ |
| Benchmark files | 4 | 10+ | 17+ | 20+ |
| Framework integrations | 0 | 0 | 0 | 2+ (LangChain, MCP) |
| CLI on PyPI | ❌ | ❌ | ❌ | ✅ |
| Skill Paths | 0 | 4 | 4 (live in UI) | 4+ |
| SHOWCASE entries | 0 | 1+ | 3+ | 5+ |

---

## Deferred to v3.5+ (Post-Roadmap)

The following items from the P3 backlog are explicitly out of scope for this roadmap and should not be started until v3.0 is cut:

| Feature | Reason for Deferral |
|---------|---------------------|
| GraphQL API (P3-1) | Requires hosting infrastructure change; CLI is the proof of concept first |
| Skill Playground / WASM (P3-3) | Requires enough battle-tested v3 skills with clean, tested code first |
| AI Skill Proposal Bot / arXiv sweep (P3-4) | Requires stable framework and active community to review proposals |
| Full multilingual skill content (P3-5) | English content must be fully stable at v2+ before translation |
| Enterprise Skill Packs (P3-6) | Requires sponsorship tiers to be active and proven first |
| "Ask Skills Tree" RAG chatbot (P3-7 / AI-7) | Requires Cloudflare Worker infrastructure decision and sufficient budget |
| Skills Certification Program (P3-2) | Requires community maturity (v3.0+) and legal/process work |

---

*This document is the executable roadmap for Skills Tree v2.3 → v3.0. Update after each sprint retrospective. All task IDs reference `SECTION 15 — IMPLEMENTATION ORDER` in `PROJECT_MEMORY.md`.*
