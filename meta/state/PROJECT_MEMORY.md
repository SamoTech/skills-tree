## SECTION 1 — PROJECT IDENTITY

### Project Name
**Skills Tree** — The AI Agent Skill OS

### Mission
Provide the world's most comprehensive, versioned, community-powered index of AI agent capabilities — documented with working code, real benchmarks, real failure modes, and evolution history — so that every AI agent builder never has to rediscover the same skills from scratch.

### Vision
> Skills Tree becomes the **canonical index of AI agent capabilities** — versioned, benchmarked, community-powered, and integrated into every major agent framework.

AI agents are becoming teammates, not tools. Skills Tree is the shared foundation they run on — a living OS of capabilities that the community builds, tests, and evolves together. Every skill added saves every agent builder who comes after. Every benchmark prevents someone else from wasting a week. Every system documented becomes a launchpad for the next builder.

### Goals

1. **Content:** Reach 1,000+ skills — all battle-tested, all benchmarked
2. **Community:** 50+ active contributors; self-sustaining growth loop
3. **Discoverability:** 1,000+ GitHub stars as credibility threshold
4. **Integration:** Referenced by LangChain, LangGraph, MCP registry, OpenAI Cookbook
5. **Access:** CLI tool (`pip install skills-tree`) and JSON/YAML API for programmatic access
6. **Education:** Curated Skill Paths (learning tracks) from beginner to production-ready

### Success Criteria

| Metric | Current (2026-06-14) | Target (v3.0) |
|--------|---------------------|---------------|
| Total skills | 377 | 1,000+ |
| Battle-tested (v3) skills | 27 | 300+ |
| Expanded skills (v2+) | 48 | 600+ |
| Contributors | 3 | 50+ |
| GitHub Stars | Unknown | 1,000+ |
| Framework integrations | 0 | 4 (LangChain, LangGraph, MCP, OpenAI) |
| Localization | 10 README languages | Full category translation in top 3 |

---

## SECTION 2 — CURRENT STATE

### Existing Functionality

**Core Content Corpus**
- 377 skill files across 17 taxonomy categories (as of leaderboard 2026-05-18)
- 27 battle-tested (v3) skills — production-ready, copy-paste safe
- 48 expanded (v2+) skills — with full examples and failure modes
- ~302 stubs awaiting upgrade to v2 or v3

**Multi-Layer Content Structure**
- `skills/` — 361+ atomic skill files with typed I/O, versioned, categorized
- `systems/` — 8 multi-skill workflow files (research agent, code reviewer, voice agent, etc.)
- `blueprints/` — 7 copy-paste production architectures (RAG stack, multi-agent mesh, human-in-the-loop, self-healing agent, etc.)
- `benchmarks/` — 4 reproducible head-to-head skill comparisons (ReAct vs LATS, RAG strategies, memory injection, function calling)
- `labs/` — 4 experimental/bleeding-edge entries (tree-of-agents, episodic compression, adaptive tool selection, MCTS)

**Interactive Web UI**
- GitHub Pages at [https://samotech.github.io/skills-tree](https://samotech.github.io/skills-tree)
- Dark/light mode toggle, real-time search, level-based filtering (basic/intermediate/advanced/experimental)
- Count-up animations, CSS scroll-driven reveals, card redesign with gradient top-edge

**Automation & CI/CD (30 GitHub Actions Workflows)**

| Workflow | Purpose |
|----------|---------|
| `validate-skills.yml` | Skill frontmatter format validation on every PR |
| `schema-enforce.yml` | JSON Schema enforcement against `meta/skill-schema.json` |
| `quality-report.yml` | Auto-generates `meta/QUALITY-REPORT.md`; blocks new stubs |
| `pr-checks.yml` | Full PR gate (links, schema, quality) |
| `auto-label.yml` | Auto-labels PRs by type (feat/improve/benchmark/system) |
| `leaderboard.yml` | Weekly leaderboard regeneration from PR history |
| `weekly-highlights.yml` | Monday auto-update of README highlights block |
| `skill-upgrade-comment.yml` | Comments on PRs that upgrade a skill to v2/v3 |
| `skill-version-badge.yml` | Applies Battle-Tested label at v3 |
| `version-stats.yml` | Weekly version distribution update in VERSIONING.md |
| `export-skills.yml` | Generates `docs/api/skills.json` + `docs/api/skills.yaml` |
| `generate-search-index.yml` | Builds client-side search index for UI |
| `build-graph.yml` | Constructs skill dependency graph data |
| `ast-sweep.yml` | Machine-inferred badge scanning |
| `sync-badges.yml` / `revoke-phantom-badges.yml` | Badge lifecycle management |
| `dependency-auditor.yml` | Python dependency vulnerability and license audit |
| `osv-watch.yml` | OSV.dev CVE polling every 15 minutes |
| `check-links.yml` | Broken internal link detection |
| `generate-changelog.yml` | Automated changelog generation on merge |
| `inject-badge-links.yml` | Badge link injection into skill files |
| `deploy-pages.yml` | GitHub Pages deployment on push |
| `heartbeat.yml` / `keepalive.yml` | Uptime and stale workflow prevention |
| `uptime-monitor.yml` | GitHub Pages uptime checking |
| `stale-skills.yml` / `stale.yml` | Stale skill and issue management |
| `issue-welcome.yml` | Welcome message automation for new issues |
| `used-in-tracker.yml` | Tracks projects that use Skills Tree skills |
| `jsonld-export.yml` | JSON-LD metadata export for SEO |
| `sync-readme-badges.yml` | Skill count badge sync in README |
| `update-skill-count.yml` | Nightly skill count update |
| `security-scan.yml` | Gitleaks secret scanning + osv-scanner |

**Localization**
- 10 language READMEs: Arabic, Chinese, Spanish, German, French, Hindi, Japanese, Korean, Portuguese, Russian

**Developer Meta**
- `meta/skill-schema.json` — JSON Schema (draft-07) for skill frontmatter validation
- `meta/skill-template.md` — canonical contribution template
- `meta/benchmark-template.md`, `meta/system-template.md`, `meta/blueprint-template.md`
- `meta/glossary.md` — AI agent terminology reference
- `meta/frameworks.md` — framework compatibility matrix
- `meta/VERSIONING.md` — v1/v2/v3 upgrade spec
- `meta/QUALITY-REPORT.md` — live auto-generated stub/battle-tested audit (68KB)
- `meta/skills-sbom.cdx.json` — CycloneDX SBOM
- CODEOWNERS, FUNDING.yml, Dependabot config, mlc-config.json

**Python Tooling (`tools/`, `scripts/`)**
- `tools/check_skill_quality.py` — live v1/v2/v3 counts
- `tools/export_skills.py` — generates `docs/api/skills.json` + `docs/api/skills.yaml`
- `requirements.txt` — pinned: httpx 0.28.1, PyYAML 6.0.3, PyGithub 2.9.1, jsonschema 4.26.0, pytest 8.3.4

### Existing Architecture

```
skills-tree/
├── skills/            → 17 category dirs, 361+ atomic .md files
├── systems/           → 8 multi-skill workflow docs
├── blueprints/        → 7 production architecture docs
├── benchmarks/        → 4 reproducible comparisons
├── labs/              → 4 experimental entries
├── docs/              → GitHub Pages (index.html, 404.html, assets/, api/)
│   └── api/           → skills.json, skills.yaml, skills-schema.json (exported)
├── meta/              → Schema, templates, versioning, roadmap, leaderboard
├── tools/             → Python CI/quality scripts
├── scripts/           → Auxiliary shell/Python scripts
├── tests/             → pytest test suite
├── i18n/              → 10 localized READMEs
├── badges/            → Badge data (served via badge-data branch)
├── public/            → Static assets
├── paths/             → Skill path/track definitions
├── assets/            → Repository-level assets
├── .github/
│   ├── workflows/     → 30 GitHub Actions workflows
│   ├── ISSUE_TEMPLATE/→ Bug report, new skill, skill-update templates
│   ├── scripts/       → Workflow helper scripts
│   └── CODEOWNERS, FUNDING.yml, dependabot.yml, labeler.yml
├── requirements.txt   → Pinned Python deps
├── .gitleaks.toml     → Secret scanning config
└── osv-scanner.toml   → Vulnerability scanner config
```

**Technology Stack**

| Layer | Technology |
|-------|-----------|
| Content format | Markdown (GFM) with YAML frontmatter |
| Schema validation | JSON Schema draft-07 (`meta/skill-schema.json`) |
| UI | Vanilla HTML/CSS/JS (GitHub Pages, no framework) |
| CI/CD | GitHub Actions (30 workflows) |
| Scripting | Python 3 (httpx, PyYAML, PyGithub, jsonschema, pytest) |
| Security | Gitleaks, osv-scanner, OSV.dev API, Dependabot |
| API | Static JSON/YAML export (`docs/api/`) |
| SBOM | CycloneDX JSON |
| Hosting | GitHub Pages |
| Versioning | Semantic Versioning + skill-level v1/v2/v3 |
| License | MIT |

### Existing Strengths

1. **Comprehensive taxonomy:** 17 well-defined categories covering the full AI agent capability spectrum
2. **Quality gate system:** CI blocks new stubs; AST sweep; schema enforcement; link validation
3. **Badge lifecycle:** Grey→Yellow→Green badge system with automated phantom-revocation
4. **Versioning model:** v1/v2/v3 progression with clear upgrade checklists
5. **Viral mechanics:** Weekly leaderboard, highlights, skill-upgrade comments, PR activity tracking
6. **Security-first:** Gitleaks + OSV.dev 15-minute CVE detection SLA + osv-scanner + Dependabot
7. **Localization:** 10-language README coverage from day one
8. **JSON/YAML API:** Programmatic access via `docs/api/skills.json` for downstream tools
9. **Rich templates:** Canonical templates for skills, benchmarks, systems, blueprints
10. **Automation density:** 30 workflows; near-zero manual maintenance overhead

### Existing Weaknesses

1. **Stub ratio:** 302/377 skills (~80%) remain at v1 stub level — thin content, placeholder I/O
2. **Contributor count:** Only 3 contributors (1 bot, 1 GitHub Actions bot, 1 human) — no community yet
3. **Single maintainer risk:** @SamoTech is the only human contributor — bus factor = 1
4. **No community channels:** GitHub Discussions not yet enabled; no Discord; no forum
5. **UI is static HTML:** No interactivity beyond search/filter; cannot browse skill graph visually
6. **CLI missing:** No `skills-tree` CLI published to PyPI
7. **No skill rating system:** Users cannot vote/rate or signal quality preference
8. **Framework integration absent:** Not yet listed in LangChain Hub, MCP registry, or LangGraph docs
9. **Benchmark coverage thin:** Only 4 benchmarks for 377+ skills
10. **Category 17 (Infrastructure) is nascent:** Only 1 skill file; needs expansion
11. **`paths/` directory empty or undeveloped:** Skill learning tracks are defined but not populated
12. **Pages throttling under high-velocity merges:** Accepted limitation in `meta/KNOWN-LIMITATIONS.md`
13. **No real-world usage data:** `used-in-tracker.yml` exists but no projects submitted yet

---

## SECTION 3 — PRODUCT AUDIT

### Missing Features

1. **Interactive skill graph** — no visual map of skill relationships (`build-graph.yml` exists but UI does not render it)
2. **Skill Paths / Learning Tracks** — `paths/` directory exists but is empty; no curated learning sequences
3. **Community ratings/upvotes** — no mechanism to surface community-validated quality signals
4. **CLI tool** — `skills-tree search`, `skills-tree show`, `skills-tree new` wizard not yet published
5. **Contributor attribution per skill** — no per-skill author/owner tracking
6. **GitHub Discussions** — not enabled; community has no async forum
7. **Skill Champion system** — no formal ownership role for contributors
8. **Search index on web UI** — `generate-search-index.yml` exists but client-side integration needs verification
9. **Model comparison tables** — most skills lack a Claude vs GPT-4o vs Gemini table despite being in v2 template
10. **JSON-LD per skill** — `jsonld-export.yml` exists but SEO metadata injection needs completion
11. **GitHub Release packages** — no zipped skill index as a GitHub Release asset

### UX Issues

1. **Dead-end stubs in UI:** Browsing to a stub skill shows thin content with no code — degrades trust
2. **No "start here" path:** New visitors to the live UI have no guided entry point beyond README
3. **Skill count drift:** README badge count and actual file count can diverge between nightly runs
4. **No mobile-optimized UI:** GitHub Pages UI uses desktop-first design
5. **Category README files missing for most categories** — no per-category landing pages in the UI
6. **No difficulty/complexity filter combination** — UI filters by level but not combined level+category
7. **Leaderboard shows no real human activity:** Current leaderboard shows only bots — cosmetically damaging to perception of community health

### Technical Debt

1. **`osv-watch.yml` originally used inline `pip install requests`** — fixed 2026-06-14, now in `requirements.txt` but the migration is recent and untested at scale
2. **`badge-data` branch strategy** — custom branch for badge JSON is non-standard and fragile under high-velocity pushes (documented in KNOWN-LIMITATIONS.md)
3. **30 workflows is high maintenance surface** — some workflows overlap in scope (`stale.yml` + `stale-skills.yml`; `heartbeat.yml` + `keepalive.yml`)
4. **Python scripts lack a unified test runner** — `tests/` directory exists but coverage of tooling scripts is unknown
5. **`docs/index.html` is a monolithic 40KB file** — no build pipeline; hard to maintain at scale
6. **Phantom badge window** — accepted limitation; v1.1 debounce fix not yet implemented
7. **`meta/QUALITY-REPORT.md` is 68KB** — renders slowly in GitHub; may need pagination or summary view

### Documentation Gaps

1. **No `ARCHITECTURE.md`** — directory structure exists but no architectural decision record (ADR) document
2. **`paths/` has no README** — the directory exists but has no explanation of purpose
3. **No onboarding tutorial** — CONTRIBUTING.md is thorough but lacks a "5-minute quickstart" for first-time contributors
4. **Category-level READMEs missing** — 17 category directories have no `index.md` explaining what belongs in each
5. **API documentation lacking** — `docs/api/skills-schema.json` exists but no Swagger/OpenAPI developer reference
6. **No CHANGELOG automation post-v2** — `generate-changelog.yml` exists but effectiveness not verified in production

### Growth Limitations

1. **No social proof loop** — no "Used In" section populated yet; no testimonials; no case studies
2. **No email/newsletter** — no way to re-engage visitors after first visit
3. **Sponsorship cold start** — 0 current sponsors; no tier-differentiated perks visible in the UI
4. **No cross-promotion with frameworks** — LangChain, CrewAI, AutoGen do not reference Skills Tree
5. **Content monoculture risk** — all content currently authored/curated by one person; community has not taken ownership
6. **Discovery limited to GitHub** — no presence on npm, PyPI, or developer aggregators

---

## SECTION 4 — FUTURE PRODUCT VISION

### The Ideal State in 3 Years (2029)

**Skills Tree is the Wikipedia of AI agent capabilities.**

Every AI agent framework — LangChain, LangGraph, CrewAI, AutoGen, Microsoft Semantic Kernel, and the next generation of agent orchestrators — links to Skills Tree as the canonical reference for what their framework implements. Every agent developer, from student to Staff Engineer at a Fortune 500, has a Skills Tree tab bookmarked.

The repository hosts 1,500+ skills across 25+ categories, all at v2 or above, with 500+ at full v3 battle-tested status. Community contributions arrive daily from hundreds of contributors spanning every major language and agent framework. An automated AI sweep pipeline continuously proposes stub upgrades, which human reviewers then approve.

A CLI (`pip install skills-tree`) lets developers search, preview, and scaffold skills directly in their terminal. A REST/GraphQL API serves the skill catalog to downstream tools. An MCP-native skills registry means any MCP-compatible agent can query the catalog in real time.

Skill Paths guide learners from "prompt engineering" through to "production multi-agent mesh" in structured, milestone-verified tracks. Community governance — a Skills Council, monthly RFC process, and verified Skill Champions — ensures quality remains high as volume grows.

Monetization is sustainable: enterprise sponsors fund dedicated skill maintenance in high-demand domains (healthcare, finance, legal DevOps). A "Skills Tree Verified" certification program for agent frameworks drives B2B revenue.

---

## SECTION 5 — MASTER FEATURE BACKLOG

### P0 — Critical (Blocks Growth)

| ID | Feature | Business Value | Technical Complexity | Dependencies |
|----|---------|---------------|---------------------|--------------| 
| P0-1 | **Stub Upgrade Blitz** — Upgrade all 302 v1 stubs to v2 minimum (description, runnable example, failure modes, related skills) | Eliminates the #1 trust killer; every page becomes useful | Medium — content work, not engineering | `meta/skill-template.md` (done), `QUALITY-REPORT.md` (done) |
| P0-2 | **GitHub Discussions** — Enable with categories: Ideas, Benchmarks, Q&A, Showcase, Roadmap | Opens the community loop; enables async contributor engagement | Low — GitHub feature toggle + pinned posts | None |
| P0-3 | **Skill Paths** — Populate `paths/` with 4 curated learning tracks (Research Agent, Memory-First, Computer Use, Zero-to-Production) | Dramatically improves discoverability and SEO; creates first-timer friendly entry | Medium — content + UI integration needed | P0-1 (enough v2 skills must exist) |
| P0-4 | **Model Comparison Tables** — AST sweep pass to add Claude/GPT-4o/Gemini comparison to all v2+ skills | Top-requested feature; makes content actionable immediately | Medium — Python AST sweep + template injection | v2 template (done), `ast-sweep.yml` (exists) |

### P1 — High Priority

| ID | Feature | Business Value | Technical Complexity | Dependencies |
|----|---------|---------------|---------------------|--------------| 
| P1-1 | **CLI Tool** — `pip install skills-tree`; implement `search`, `show`, `new` commands | Puts Skills Tree in every developer's terminal; drives PyPI discoverability | High — CLI framework, packaging, PyPI release pipeline | Export API (done) |
| P1-2 | **Community Skill Ratings** — Thumbs up/down or star ratings via GitHub Reactions on skill issues | Surfaces quality signals; drives engagement loop | Medium — GitHub Reactions API + leaderboard integration | Discussions (P0-2) |
| P1-3 | **Interactive Skill Graph** — Visual D3.js/Mermaid graph of skill relationships in `docs/index.html` | Highly shareable; demonstrates the "OS" metaphor visually | High — `build-graph.yml` data + frontend D3 visualization | `build-graph.yml` (done) |
| P1-4 | **Skill Champion System** — Formal ownership role per skill; champion gets credit in frontmatter | Distributes maintenance load; incentivizes contribution | Low-Medium — frontmatter field + CODEOWNERS automation | P0-2 (Discussions for nomination) |
| P1-5 | **Social Proof / "Used In" Section** — Populate the used-in section in README with real submissions | Drives credibility; each submission is a social amplifier | Low — `used-in-tracker.yml` exists; need 5+ real submissions | Used-in issue template (done) |
| P1-6 | **Mobile-Responsive UI** — Refactor `docs/index.html` for mobile-first layout | Opens access to developers on mobile; reduces bounce rate | Medium — CSS refactor; must not break existing animations | None |
| P1-7 | **Per-Category Index Pages** — Add `README.md` to each of the 17 category directories | Improves discoverability; GitHub renders these automatically | Low — 17 markdown files with description, skill list, badges | P0-1 (need populated skills per category) |

### P2 — Medium Priority

| ID | Feature | Business Value | Technical Complexity | Dependencies |
|----|---------|---------------|---------------------|--------------| 
| P2-1 | **LangChain Hub Integration** — Publish top 20 battle-tested skills as Hub templates | Massive distribution channel; immediate credibility signal | High — LangChain Hub API + template format conversion | P0-1 |
| P2-2 | **MCP Registry Integration** — Register skills as MCP tools in the official registry | Future-proofs the project; early-mover advantage in agentic protocols | High — MCP protocol compliance + schema mapping | MCP registry launch timeline |
| P2-3 | **Benchmark Expansion** — Add benchmarks for all 17 categories (minimum 1 per category) | Each benchmark is highly linkable/shareable; academic citation magnet | Medium-High — real dataset required per benchmark | P0-1 |
| P2-4 | **JSON-LD SEO per Skill** — Complete `jsonld-export.yml` to inject `<script type="application/ld+json">` into each skill's GitHub Page | SEO structured data; skill pages rank in Google for agent queries | Medium — `jsonld-export.yml` exists; needs frontend injection | `jsonld-export.yml` (exists) |
| P2-5 | **GitHub Release Packages** — Zip the full skill index as a GitHub Release asset on each version tag | Enables offline use; citable artifact for researchers | Low — CI step + GitHub Release API | Export scripts (done) |
| P2-6 | **Automated Changelog on Merge** — Verify and fully activate `generate-changelog.yml` | Reduces maintainer toil; demonstrates active development to visitors | Low-Medium — workflow debugging + format validation | None |
| P2-7 | **Onboarding Tutorial** — Add "5-minute quickstart" section to CONTRIBUTING.md and the web UI | Reduces contributor drop-off at first PR | Low — content only | None |
| P2-8 | **Category 17 Infrastructure Expansion** — Grow from 1 to 15+ infrastructure skills | Fills a critical gap for DevOps agent builders | Medium — content + review | P0-1 methodology |
| P2-9 | **Stale Skill Detection with AI Suggestions** — Extend `stale-skills.yml` to suggest upgrade content using LLM-generated drafts | Accelerates stub-to-v2 pipeline; reduces human effort per upgrade | High — LLM API integration in CI | None |

### P3 — Future Ideas

| ID | Feature | Business Value | Technical Complexity | Dependencies |
|----|---------|---------------|---------------------|--------------| 
| P3-1 | **GraphQL API** — Expose the skills catalog as a queryable GraphQL endpoint | Enables rich downstream integrations | Very High — hosting infrastructure change | P1-1 CLI as proof of concept |
| P3-2 | **Skills Certification Program** — "Skills Tree Verified" badge for agent frameworks | B2B revenue stream; framework adoption incentive | Very High — process + tooling + legal | Community maturity (v3.0+) |
| P3-3 | **Skill Playground** — Run a skill's code example in-browser via WASM/Pyodide | Turns the repo into an interactive demo platform | Very High — WASM, sandboxing | Enough battle-tested skills with clean code |
| P3-4 | **AI Skill Proposal Bot** — GitHub App that reads emerging papers/repos and proposes new skill stubs as PRs | Keeps content ahead of the curve without manual research | Very High — LLM + GitHub App + paper ingestion pipeline | Framework stability |
| P3-5 | **Multilingual Skill Content** — Translate full skill files (not just READMEs) into top 5 languages | Opens contribution from non-English communities | Very High — translation pipeline + quality control | P0-1 (English content must be stable first) |
| P3-6 | **Enterprise Skill Packs** — Private, domain-specific skill packs (healthcare, legal, finance) for paying sponsors | Direct monetization pathway | High — private repo structure + access control | Sponsorship tiers (P1-5) |
| P3-7 | **Skill Deprecation Protocol** — Formal process + CI automation to mark skills as deprecated when superseded | Keeps catalog accurate as AI moves fast | Medium — workflow + frontmatter field | `stability: deprecated` already in schema |

---

## SECTION 6 — ARCHITECTURE ROADMAP

### Current Architecture

```
Static Markdown Repository (GitHub as CMS)
├── Content: .md files with YAML frontmatter (no database)
├── Validation: Python + jsonschema in GitHub Actions CI
├── UI: Monolithic docs/index.html (vanilla JS, no bundler)
├── API: Static JSON/YAML export (read-only, regenerated by CI)
├── Search: Client-side (generated JSON index loaded into browser)
└── Hosting: GitHub Pages (CDN, free tier)
```

**Strengths of current arch:** Zero hosting cost; entire catalog is versionable and diffable; GitHub native; contributions via PR (familiar workflow).  
**Limitations:** Monolithic UI file; no dynamic search ranking; no user accounts; no real-time updates; no programmatic write access.

### Target Architecture (v3.0, 2026–2027)

```
Hybrid: Static Markdown + CLI + Light API Layer
├── Content: Same .md files (do not change the source of truth)
├── Validation: Same GitHub Actions CI pipeline (hardened)
├── UI: Modular docs/ with separate JS bundles (Vite build or similar)
│   ├── Skill graph visualization (D3.js, data from docs/api/graph.json)
│   ├── Skill Paths renderer (data from paths/*.yaml)
│   └── Search: Pagefind or FlexSearch (pre-built index at CI)
├── CLI: Python package on PyPI (`skills-tree` command)
│   ├── skills-tree search <query>
│   ├── skills-tree show <category/skill>
│   ├── skills-tree new  (interactive wizard)
│   └── skills-tree benchmark run <skill>
├── API: Static JSON/YAML (extended schema; graph.json; paths.json)
│   └── Optional: Cloudflare Worker proxy for search/filter API calls
└── Hosting: GitHub Pages (static) + PyPI (CLI) + optional CF Worker
```

### Migration Plan

| Phase | Action | Risk |
|-------|--------|------|
| Now → v2.x | Stub upgrade blitz; per-category READMEs; Skill Paths content | Low — pure content |
| v2.x → v2.5 | Modularize `docs/index.html`; add D3 skill graph; Pagefind search | Medium — UI refactor |
| v2.5 → v3.0 | Build + publish CLI to PyPI; extend API schema with graph/paths | Medium — packaging pipeline |
| v3.0+ | Framework integrations (LangChain Hub, MCP); optional API layer | High — external dependencies |

---

## SECTION 7 — DATA MODEL ROADMAP

### Current Data Model (Skill Frontmatter)

```json
{
  "title": "string (required)",
  "category": "enum: 01-perception … 17-infrastructure (required)",
  "level": "enum: basic | intermediate | advanced | experimental (required)",
  "stability": "enum: stable | experimental | deprecated (required)",
  "version": "pattern: ^v[0-9]+$ (optional)",
  "added": "pattern: YYYY-MM (required)",
  "last_updated": "pattern: YYYY-MM (optional)",
  "description": "string 1-3 sentences (required)",
  "related_skills": ["array of relative paths (optional)"],
  "frameworks": [{"name": "string", "url": "uri", "implementation": "string", "since": "string"}]
}
```

### Future Entities to Add

**Skill (Extended)**
- `champion`: GitHub username of skill owner
- `battle_tested_since`: YYYY-MM when v3 was reached
- `used_in_count`: integer, populated by CI from used-in submissions
- `benchmark_links`: array of relative paths to benchmarks
- `model_scores`: object — `{"claude-opus-4": {"accuracy": 0.92}, "gpt-4o": {"accuracy": 0.89}}`
- `paths`: array of path IDs that include this skill
- `tags`: free-form tags for cross-cutting concerns (e.g., `["streaming", "async", "token-budget"]`)
- `deprecated_by`: relative path to the replacing skill (when `stability: deprecated`)

**SkillPath Entity** (new — `paths/*.yaml`)
```yaml
id: research-agent-path
title: "Build a Research Agent"
level: intermediate
skills:
  - skills/11-web/web-search.md
  - skills/03-memory/rag.md
  - skills/06-communication/summarize.md
  - skills/03-memory/memory-injection.md
  - skills/09-agentic-patterns/react.md
milestones:
  - after: 2
    check: "Can the agent retrieve and filter results?"
  - after: 5
    check: "Does the final agent cite sources?"
```

**Benchmark Entity** (extended)
- `dataset`: string — name + size
- `metrics`: array of `{name, winner, value, margin}`
- `models_tested`: array of model names
- `reproduced_by`: array of GitHub usernames who have independently reproduced
- `script_path`: relative path to reproducibility script

**UsedIn Entity** (new — sourced from issues/tracker)
- `project_name`: string
- `project_url`: URL
- `skills_used`: array of skill IDs
- `contributor`: GitHub username
- `submitted_at`: YYYY-MM-DD

**Contributor/Champion Entity** (new — sourced from PR history + frontmatter)
- `github_username`: string
- `skills_added`: integer
- `skills_improved`: integer
- `skills_championed`: array of skill IDs
- `total_prs`: integer
- `joined_at`: YYYY-MM-DD

---

## SECTION 8 — UI/UX ROADMAP

### Current UI State

- Single `docs/index.html` (~40KB monolith, vanilla JS)
- Dark/light mode, search, level filter, category cards, count-up stats
- No routing; no pagination; no skill graph view; no path view

### Future Interfaces

**Interface 1: Skill Graph View** (v2.5)
- Interactive D3.js force-directed graph
- Nodes: skills, colored by category
- Edges: `related_skills` links
- Click node → side panel with skill summary + link
- Filter by category, level, version status
- Data source: `docs/api/graph.json` (built by `build-graph.yml`)

**Interface 2: Skill Path View** (v2.5)
- Linear progress track for each defined path
- Step cards with skill name, level badge, estimated time
- "Mark complete" mechanism (localStorage, no account needed)
- "Where am I in this path?" resume indicator

**Interface 3: Skill Detail Page** (v3.0)
- Full rendered Markdown per skill with syntax-highlighted code
- Model comparison score table
- Benchmark links panel
- "Used In" project examples
- Version history timeline
- Requires: static site generator or server-side rendering

**Interface 4: Benchmark Dashboard** (v3.0)
- Sortable table of all benchmarks
- Filter by category, metric, model
- Reproducibility status indicator (⚪ unverified / 🟡 1 verification / 🟢 3+ verifications)

**Interface 5: CLI Output** (v3.0)
- Terminal-rendered skill preview using `rich` library
- Syntax-highlighted code blocks in terminal
- Progress bars for path completion

### Mobile Strategy
- Existing UI must be refactored to mobile-first CSS breakpoints
- Card grid: 1 column on mobile, 2 on tablet, 3+ on desktop
- Navigation: hamburger menu on mobile
- Search: always-visible on mobile (not collapsed behind icon)

---

## SECTION 9 — SEARCH ROADMAP

### Current Search
- Client-side JavaScript substring match against skill titles and descriptions loaded from `docs/api/skills.json`
- Real-time, no latency; works offline
- Limitation: no ranking, no fuzzy match, no full-text search in skill body content

### Search Evolution Phases

**Phase 1 — Enhanced Client-Side (v2.5)**
- Replace substring match with [Pagefind](https://pagefind.app) or [FlexSearch](https://github.com/nextapps-de/flexsearch)
- Full-text indexing of skill content (not just frontmatter)
- Fuzzy matching with typo tolerance
- Search result ranking by: version (v3 > v2 > v1), recency, relevance score

**Phase 2 — Faceted Filtering (v2.5)**
- AND/OR combinations across: category + level + stability + version + framework
- "Show only battle-tested" toggle
- "Show only stubs (for contribution)" toggle

**Phase 3 — Semantic Search (v3.0+)**
- Optional: embed skill descriptions via Sentence Transformers
- Store embeddings as static JSON (pre-computed by CI)
- Client queries against embeddings using `cos-similarity` in browser (WASM)
- Example: "Skills related to: 'retry an API call 3 times'" → returns `http-request.md`, `self-healing-agent` blueprint, etc.

**Phase 4 — CLI Search (v3.0)**
- `skills-tree search "memory injection"` → terminal results with rank, version, category
- `skills-tree search --battle-tested --category memory` → filtered results
- Results link to the raw Markdown URL for direct reading

---

## SECTION 10 — API ROADMAP

### Current API State
- `docs/api/skills.json` — array of all skill objects (frontmatter + metadata), rebuilt by CI on every push to `skills/`
- `docs/api/skills.yaml` — same data in YAML
- `docs/api/skills-schema.json` — JSON Schema for a skill object
- All are static files served by GitHub Pages

### Future API Endpoints (Static JSON, Extended)

| Endpoint | Description | Priority |
|----------|-------------|----------|
| `docs/api/graph.json` | Skill dependency graph (nodes + edges from `related_skills`) | P1 |
| `docs/api/paths.json` | All Skill Paths with ordered skill sequences | P1 |
| `docs/api/leaderboard.json` | Machine-readable leaderboard data | P2 |
| `docs/api/benchmarks.json` | All benchmark metadata (not full content) | P2 |
| `docs/api/stats.json` | Aggregate counts: total, by category, by version, battle-tested % | P2 |
| `docs/api/used-in.json` | Projects using Skills Tree skills | P2 |
| `docs/api/search-index.json` | Pre-built Pagefind/FlexSearch index | P2 |
| `docs/api/jsonld/` | JSON-LD per-skill files for SEO | P2 |

### Optional Dynamic API (v3.0+, if Cloudflare Workers adopted)
- `GET /api/skills?q=memory&level=intermediate&battle_tested=true` — filtered skill search
- `GET /api/skills/{category}/{slug}` — single skill detail
- `GET /api/paths/{id}` — single learning path
- Rate-limited; read-only; CORS open; no auth required

### CLI API Integration
- CLI reads from `docs/api/skills.json` (GitHub raw URL, cached locally with TTL=24h)
- Optional `--offline` flag uses last cached copy
- `skills-tree export --format json > skills.json` for local tooling

---

## SECTION 11 — AI ROADMAP

### Current AI Surface
- The *subject matter* is AI agents — Skills Tree is a catalog of AI capabilities
- No AI is used *in the operation or maintenance* of the repository yet (except Devin bot for 4 PRs)
- `ast-sweep.yml` does code analysis (Python AST, not LLM-based)

### AI Opportunities

**Opportunity 1: AI-Powered Stub Upgrade Drafts (High Impact)**
- GitHub Action that calls an LLM (Claude/GPT-4o) with the stub content + skill template
- Generates a v2 draft PR automatically (code example, failure modes, related skills)
- Human reviewer approves/edits and merges
- Workflow: nightly sweep of all v1 stubs → batch LLM calls → draft PRs
- Risk: LLM-generated code examples must be verified for correctness before merging

**Opportunity 2: Semantic Skill Search (Medium Impact)**
- Pre-compute embeddings for all skill descriptions using a CI step (sentence-transformers or OpenAI Embeddings)
- Store as static JSON alongside `skills.json`
- Client-side cosine similarity for natural language queries
- No infrastructure required — runs entirely at build time + browser

**Opportunity 3: Benchmark Auto-Runner (High Impact, High Complexity)**
- `skills-tree benchmark run <skill>` CLI command
- Executes the skill's benchmark script against a reference dataset
- Reports pass/fail + metrics back via GitHub issue comment
- Requires: sandboxed execution environment (Docker or GitHub Actions runner)

**Opportunity 4: Skill Quality Reviewer Bot (Medium Impact)**
- GitHub App that reviews incoming skill PRs for quality criteria
- Checks: code is real Python, no pseudocode, description length, `related_skills` populated, changelog present
- Posts structured feedback as PR review comments
- Uses LLM for nuanced content quality assessment beyond schema validation

**Opportunity 5: AI-Generated Model Comparison Tables (Medium Impact)**
- Weekly CI job: for every battle-tested skill, run the code example against Claude, GPT-4o, Gemini
- Parse outputs, compute accuracy/latency/cost metrics
- Auto-update or propose PR to add/update model comparison table in skill file
- Risk: cost of running LLM API calls at scale; requires budget allocation

**Opportunity 6: Emerging Skills Detector (Low Impact, Long-term)**
- Weekly agent that reads arXiv + Papers With Code + GitHub trending
- Identifies new agent techniques not yet in the catalog
- Files GitHub issues tagged `skill-proposal` with title, description, source paper
- Requires: web search + classification pipeline

**Opportunity 7: Interactive Skills Q&A (Long-term)**
- "Ask Skills Tree" chatbot powered by RAG over the entire skill catalog
- Answers questions like: "What's the best memory pattern for a long-running coding agent?"
- Returns skill citations from the catalog
- Deployment: GitHub Pages + Cloudflare Workers (edge inference)

---

## SECTION 12 — COMMUNITY ROADMAP

### Current Community State
- 3 total contributors (2 bots, 1 human)
- No GitHub Discussions
- No Discord
- No newsletter
- LEADERBOARD.md shows no real human activity this week
- Issue templates exist but no issues are open

### Community Growth Phases

**Phase 1 — Open the Channels (Immediate)**
- Enable GitHub Discussions with 5 categories: Ideas, Benchmarks, Q&A, Showcase, Roadmap
- Pin a "Start Here" discussion with contribution guide and current priorities
- Create a `good first issue` label and tag 30+ stub files as first-issue targets
- Post initial "Show HN" / Reddit r/MachineLearning launch announcement

**Phase 2 — Incentivize Quality (v2.x)**
- Skill Champion system: first contributor to take a skill from v1→v3 becomes the champion
- Champion username added to skill frontmatter (`champion: @username`)
- Monthly "Contributor of the Month" shoutout in README and Discussions
- Automated congratulations comment when a PR completes a stub-to-v3 upgrade

**Phase 3 — Build the Loop (v2.x)**
- Monthly "State of the Skills Tree" post on Reddit, LinkedIn, Twitter/X
- "Powered by Skills Tree" badge for projects using the skills (markdown snippet in README)
- Cross-post new battle-tested skills to relevant framework communities (LangChain Discord, etc.)
- Track and feature real projects built with Skills Tree skills in a `SHOWCASE.md`

**Phase 4 — Governance (v3.0+)**
- Skills Council: 5-member rotating committee reviews major taxonomy changes
- RFC process for new categories, deprecations, breaking schema changes
- Verified Contributor tier: contributors who have merged 5+ quality PRs get maintainer-lite access
- Quarterly virtual community calls (recorded and linked from Discussions)

---

## SECTION 13 — SPONSORSHIP ROADMAP

### Current State
- `SPONSORS.md` defines 4 tiers: Coffee ($5/mo), Builder ($15/mo), Pro ($49/mo), Teams ($199/mo)
- `FUNDING.yml` configured for GitHub Sponsors
- 0 current sponsors

### Sponsorship Strategy

**Short-term: Achieve First 10 Sponsors**
- Add a prominent sponsor CTA to the GitHub Pages UI (not just README)
- Show sponsor names/logos on the live web UI with tier-based display size
- Reach out personally to 20 AI tooling companies with a tailored pitch
- Offer free "custom skill category" (Pro tier perk) to the first 3 Pro sponsors

**Medium-term: Enterprise Tier**
- Redesign the Teams tier ($199/mo) with clearer enterprise value:
  - Private Slack or Discord channel
  - 2 consulting hours/month on AI agent architecture
  - Logo + link on all README translations and web UI
  - Priority review of contributed skills from the company's engineers
- Add an Enterprise tier ($999/mo):
  - Dedicated domain skill pack (healthcare, legal, finance, DevOps)
  - Co-authored case study published to skills-tree blog
  - Early access to CLI and API beta features

**Long-term: Certification Revenue**
- "Skills Tree Verified" certification for agent frameworks that pass a skills compatibility test
- Annual renewal fee
- Listed prominently in the catalog and web UI

**Sponsor Fund Allocation**
- 40% — LLM API credits for AI automation (stub upgrades, benchmark runs)
- 30% — Maintainer stipend (compensate @SamoTech and future core maintainers)
- 20% — Community tooling (Discord premium, tooling subscriptions)
- 10% — Event sponsorship (conference talks, meetup presentations)

---

## SECTION 14 — TECHNICAL ROADMAP

### Phase 1 — Foundation (COMPLETE: v1.0–v2.2, Dec 2025–Apr 2026)
✅ 17 skill categories defined  
✅ 377 skill files (stubs + 27 battle-tested)  
✅ GitHub Pages UI (dark/light, search, filter)  
✅ 30 GitHub Actions workflows  
✅ CI validation (schema, links, quality report)  
✅ JSON/YAML export API  
✅ Versioning system (v1/v2/v3)  
✅ Badge lifecycle management  
✅ Localization (10 languages)  
✅ Security scanning (Gitleaks, OSV.dev, osv-scanner, Dependabot)  
✅ Systems, Blueprints, Benchmarks, Labs directories  

### Phase 2 — Core Platform (Target: v2.x, Q3 2026)
⬜ Stub Upgrade Blitz: 302 stubs → v2 minimum  
⬜ GitHub Discussions enabled + seeded  
⬜ Per-category `README.md` files (17 files)  
⬜ Skill Paths: populate `paths/` with 4 tracks  
⬜ Model comparison tables: AST sweep for all v2+ skills  
⬜ Mobile-responsive UI refactor  
⬜ Pagefind/FlexSearch integration for full-text search  
⬜ `good first issue` labeling campaign (30+ issues)  
⬜ Onboarding quickstart in CONTRIBUTING.md  
⬜ 20+ benchmark files (at least 1 per category)  

### Phase 3 — Advanced Features (Target: v3.0, Q4 2026)
⬜ CLI tool: `pip install skills-tree`; PyPI publication  
⬜ Skill graph visualization in web UI (D3.js)  
⬜ AI-powered stub upgrade draft PRs  
⬜ Skill Champion system + frontmatter field  
⬜ JSON-LD SEO injection completed  
⬜ GitHub Release packages (zipped skill index)  
⬜ Semantic search with pre-computed embeddings  
⬜ LangChain Hub integration (top 20 skills)  
⬜ MCP registry listing  
⬜ Skills detail pages (individual rendered Markdown)  

### Phase 4 — Ecosystem (Target: v3.5, H1 2027)
⬜ LangGraph + OpenAI Cookbook cross-references  
⬜ "Powered by Skills Tree" badge widget  
⬜ Community governance (Skills Council, RFC process)  
⬜ Enterprise sponsorship tiers activated  
⬜ Skills certification program prototype  
⬜ Interactive benchmark dashboard  
⬜ SHOWCASE.md with real-world projects  
⬜ AI Skill Quality Reviewer bot (GitHub App)  

### Phase 5 — Global Scale (Target: v4.0, H2 2027+)
⬜ 1,000+ skills, 300+ battle-tested  
⬜ 50+ contributors  
⬜ GraphQL API (optional Cloudflare Worker)  
⬜ Skill Playground (WASM in-browser code execution)  
⬜ "Ask Skills Tree" RAG-powered Q&A chatbot  
⬜ Enterprise Skill Packs (private domain-specific packs)  
⬜ Full multilingual skill content (top 5 languages)  
⬜ Framework integrations: 4+ major frameworks  
⬜ Verified Contributor + Governance tiers active  

---

## SECTION 15 — IMPLEMENTATION ORDER

Exact execution sequence for the next 12 months. Each task has a unique ID, is ordered by dependency and priority, with no overlapping requirements.

| ID | Task | Description | Effort | Dependencies | Priority |
|----|------|-------------|--------|--------------|----------|
| T-01 | Enable GitHub Discussions | Toggle on, create 5 categories, pin "Start Here" post | 2h | None | P0 |
| T-02 | Create `good first issue` label and tag 30 stubs | Label creation + 30 issue filings linking to stub files | 3h | T-01 | P0 |
| T-03 | Add per-category `README.md` files | Write a 200-word README for each of the 17 category dirs | 1d | None | P1 |
| T-04 | Stub Upgrade Wave 1 (50 skills) | Upgrade 50 highest-traffic v1 stubs to v2: real code example, failure modes, related skills | 2w | `meta/skill-template.md` | P0 |
| T-05 | Stub Upgrade Wave 2 (100 skills) | Next 100 stubs to v2 | 3w | T-04 | P0 |
| T-06 | Stub Upgrade Wave 3 (remaining ~152 skills) | Complete stub upgrade blitz | 4w | T-05 | P0 |
| T-07 | Model comparison AST sweep | Run `ast-sweep.yml` pass to add model comparison tables to all v2+ skills | 1w | T-04 | P0 |
| T-08 | Populate `paths/` with 4 learning tracks | Write YAML for Research Agent, Memory-First, Computer Use, Zero-to-Production paths | 3d | T-04 | P0 |
| T-09 | Integrate Pagefind for full-text search | Replace client-side substring match in `docs/index.html`; add Pagefind build step to `deploy-pages.yml` | 2d | None | P1 |
| T-10 | Mobile-responsive UI refactor | Refactor `docs/index.html` CSS to mobile-first breakpoints | 2d | None | P1 |
| T-11 | Add skill graph JSON export | Extend `build-graph.yml` to write `docs/api/graph.json` | 1d | None | P1 |
| T-12 | Add D3 skill graph to UI | Import D3.js, render force-directed graph from `graph.json` in `docs/index.html` | 3d | T-11 | P1 |
| T-13 | Skill Paths web UI renderer | Add paths tab to `docs/index.html`, render from `paths.json` | 2d | T-08 | P1 |
| T-14 | Benchmark expansion (13 new benchmarks) | Write 1 benchmark per category for the 13 categories currently without one | 2w | T-04 | P1 |
| T-15 | JSON-LD export completion | Complete `jsonld-export.yml` to inject structured data into GitHub Pages | 1d | `jsonld-export.yml` | P2 |
| T-16 | GitHub Release packaging | Add CI step to `export-skills.yml` to create GitHub Release zip on version tag | 1d | None | P2 |
| T-17 | Onboarding quickstart | Write "5-minute first contribution" section in CONTRIBUTING.md + web UI | 1d | None | P2 |
| T-18 | Used-in social proof | Solicit 5+ project submissions via used-in issue template; add `SHOWCASE.md` | 1w | T-01 | P1 |
| T-19 | CLI scaffold + PyPI setup | Create `skills_tree/` Python package; implement `search` + `show`; publish to PyPI | 1w | `docs/api/skills.json` | P1 |
| T-20 | CLI `new` wizard | Add interactive `skills-tree new` command with template injection | 3d | T-19 | P1 |
| T-21 | AI stub upgrade draft PRs | GitHub Action: nightly LLM call per stub → draft PR with v2 content | 1w | T-06, LLM API key | P2 |
| T-22 | Skill Champion system | Add `champion` field to `skill-schema.json`; update CODEOWNERS automation | 2d | T-01 | P1 |
| T-23 | LangChain Hub submission | Convert top 20 skills to Hub template format; submit | 1w | T-04 | P2 |
| T-24 | MCP registry listing | Map skills to MCP tool format; register in official MCP registry | 1w | T-04 | P2 |
| T-25 | Semantic search embeddings | CI step: embed all skill descriptions; store in `docs/api/embeddings.json`; client-side similarity | 3d | T-09, embedding API | P3 |

---

## SECTION 16 — DO NOT IMPLEMENT

The following ideas have been **intentionally rejected** for the reasons noted. Do not revisit without a documented reason for the change.

| Idea | Reason for Rejection |
|------|---------------------|
| **Database backend for skills** | Adds hosting cost and infrastructure complexity; the entire value of the project is that content is in Markdown — diffable, clonable, offline-readable. GitHub as CMS is a core design principle. |
| **Next.js / React frontend for docs** | Over-engineering for what is a static documentation site. Adds build complexity, bundle size, and contributor friction for new UI contributors. Vanilla HTML/CSS/JS keeps the UI hackable by everyone. |
| **Enforcing a single programming language per skill** | Skills should demonstrate the pattern in the most natural language for that domain. Forcing Python-only would exclude TypeScript/LangChain, Rust, and Go examples that are genuinely more appropriate for some skills. |
| **Auto-merging AI-generated skill upgrades without human review** | LLMs produce plausible but incorrect code. Auto-merge would destroy content quality — the one thing that differentiates Skills Tree from a generated dataset dump. All AI-generated content must pass human review before merge. |
| **Per-skill GitHub Pages subsite** | Each skill getting its own URL (e.g., `skills-tree.github.io/skills/rag`) requires a static site generator and build complexity that outweighs the SEO benefit at current scale. Revisit at 500+ v3 skills. |
| **Discord server (at this stage)** | Premature with <5 real contributors. An empty Discord is worse than no Discord — it signals abandonment. Activate only when monthly contributor count exceeds 10. |
| **Paid API tier** | Monetization through paywalled API access creates friction for the exact developer audience the project depends on for growth. All API access must remain free forever. Revenue comes from sponsorship and certification, not API gates. |

