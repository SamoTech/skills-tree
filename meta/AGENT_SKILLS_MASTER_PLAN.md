# AGENT SKILLS MASTER PLAN

**Version:** R-01 (Governance Recovery)  
**Date:** 2026-06-21  
**Source:** PROJECT_MEMORY.md (48,049 bytes) — verified as governing document  
**Previous file state:** PLACEHOLDER (23 bytes) — all prior content voided  

> This document is a faithful reconstruction of the roadmap from `PROJECT_MEMORY.md`.
> No metrics have been invented. Completion percentages are not estimated — only
> verified facts from the commit history are recorded.

---

## PROJECT MISSION

> Provide the world's most comprehensive, versioned, community-powered index of AI agent capabilities — documented with working code, real benchmarks, real failure modes, and evolution history — so that every AI agent builder never has to rediscover the same skills from scratch.

**Source:** PROJECT_MEMORY.md Section 1

---

## VERIFIED CURRENT STATE

| Metric | Verified Value | Source |
|---|---|---|
| Total skill files | 377 | PROJECT_MEMORY.md Section 1 |
| Battle-tested (v3) | 27 | PROJECT_MEMORY.md Section 1 |
| Expanded (v2+) | 48 | PROJECT_MEMORY.md Section 1 |
| Stubs (v1) | ~302 | PROJECT_MEMORY.md Section 1 |
| Categories | 17 | PROJECT_MEMORY.md Section 1 |
| CI Workflows | 30 | PROJECT_MEMORY.md Section 2 |
| Skill graph nodes | **UNKNOWN — verify SKILLS_GRAPH.json** | data/SKILLS_GRAPH.json |
| Skill graph edges | **UNKNOWN — verify SKILLS_GRAPH.json** | data/SKILLS_GRAPH.json |
| Contributors (human) | 1 (@SamoTech) | PROJECT_MEMORY.md Section 12 |
| GitHub Stars | Unknown | PROJECT_MEMORY.md Section 1 |

---

## SUCCESS TARGETS (from PROJECT_MEMORY.md Section 1)

| Metric | Current (2026-06-14) | Target (v3.0) |
|---|---|---|
| Total skills | 377 | 1,000+ |
| Battle-tested (v3) | 27 | 300+ |
| Expanded (v2+) | 48 | 600+ |
| Contributors | 3 (1 human, 2 bots) | 50+ |
| GitHub Stars | Unknown | 1,000+ |
| Framework integrations | 0 | 4 (LangChain, LangGraph, MCP, OpenAI) |

---

## PHASE ROADMAP

### Phase 1 — Foundation ✅ COMPLETE
*Verified complete per PROJECT_MEMORY.md Section 14*

- ✅ 17 skill categories defined
- ✅ 377 skill files (27 battle-tested, 48 v2+, ~302 stubs)
- ✅ GitHub Pages UI (dark/light, search, filter, count animations)
- ✅ 30 GitHub Actions workflows
- ✅ CI validation (schema, links, quality report)
- ✅ JSON/YAML export API (`docs/api/skills.json`, `docs/api/skills.yaml`)
- ✅ Versioning system (v1/v2/v3)
- ✅ Badge lifecycle (grey→yellow→green, phantom revocation)
- ✅ Localization (10 language READMEs)
- ✅ Security scanning (Gitleaks, OSV.dev 15-min CVE SLA, osv-scanner, Dependabot)
- ✅ Systems (8), Blueprints (7), Benchmarks (4), Labs (4)
- ✅ Templates: skill, benchmark, system, blueprint
- ✅ JSON Schema (draft-07) for skill frontmatter validation
- ✅ Python tooling: `check_skill_quality.py`, `export_skills.py`
- ✅ SBOM (CycloneDX), FUNDING.yml, CODEOWNERS, Dependabot
- ✅ Workflow security: least-privilege permissions (commit `33af1551`, 2026-06-21)

---

### Phase 2 — Core Platform ⬜ NOT STARTED
*Target: v2.x, Q3 2026 (from PROJECT_MEMORY.md Section 14)*

| Task ID | Task | Effort | Priority | Dependencies |
|---|---|---|---|---|
| T-01 | Enable GitHub Discussions (5 categories) | 2h | P0 | None |
| T-02 | Tag 30 stubs as `good first issue` | 3h | P0 | T-01 |
| T-03 | Per-category `README.md` files (17 dirs) | 1d | P1 | None |
| T-04 | Stub Upgrade Wave 1 (50 skills v1→v2) | 2w | P0 | `skill-template.md` |
| T-05 | Stub Upgrade Wave 2 (100 skills) | 3w | P0 | T-04 |
| T-06 | Stub Upgrade Wave 3 (~152 skills) | 4w | P0 | T-05 |
| T-07 | Model comparison AST sweep (v2+ skills) | 1w | P0 | T-04 |
| T-08 | Populate `paths/` (4 learning tracks) | 3d | P0 | T-04 |
| T-09 | Pagefind/FlexSearch full-text search | 2d | P1 | None |
| T-10 | Mobile-responsive UI refactor | 2d | P1 | None |
| T-11 | Skill graph JSON export (`graph.json`) | 1d | P1 | None |
| T-12 | D3 skill graph in UI | 3d | P1 | T-11 |
| T-13 | Skill Paths web UI renderer | 2d | P1 | T-08 |
| T-14 | Benchmark expansion (13 new, 1 per category) | 2w | P1 | T-04 |
| T-17 | Onboarding quickstart in CONTRIBUTING.md | 1d | P2 | None |
| T-18 | Used-in social proof / SHOWCASE.md | 1w | P1 | T-01 |

---

### Phase 3 — Advanced Features ⬜ NOT STARTED
*Target: v3.0, Q4 2026 (from PROJECT_MEMORY.md Section 14)*

| Task ID | Task | Effort | Priority | Dependencies |
|---|---|---|---|---|
| T-15 | JSON-LD SEO injection completion | 1d | P2 | `jsonld-export.yml` |
| T-16 | GitHub Release packages (zipped index) | 1d | P2 | None |
| T-19 | CLI scaffold (`skills-tree`) + PyPI | 1w | P1 | `docs/api/skills.json` |
| T-20 | CLI `new` wizard | 3d | P1 | T-19 |
| T-21 | AI stub upgrade draft PRs (nightly LLM) | 1w | P2 | T-06 + LLM API key |
| T-22 | Skill Champion system (frontmatter field) | 2d | P1 | T-01 |
| T-23 | LangChain Hub submission (top 20 skills) | 1w | P2 | T-04 |
| T-24 | MCP registry listing | 1w | P2 | T-04 |
| T-25 | Semantic search embeddings (pre-computed) | 3d | P3 | T-09 + embedding API |

---

### Phase 4 — Ecosystem ⬜ NOT STARTED
*Target: v3.5, H1 2027*

- LangGraph + OpenAI Cookbook cross-references
- "Powered by Skills Tree" badge widget
- Community governance (Skills Council, RFC process)
- Enterprise sponsorship tiers
- Skills certification program prototype
- Interactive benchmark dashboard
- SHOWCASE.md with real-world projects
- AI Skill Quality Reviewer bot (GitHub App)

---

### Phase 5 — Global Scale ⬜ NOT STARTED
*Target: v4.0, H2 2027+*

- 1,000+ skills, 300+ battle-tested
- 50+ contributors
- GraphQL API (Cloudflare Worker)
- Skill Playground (WASM in-browser execution)
- "Ask Skills Tree" RAG-powered Q&A chatbot
- Enterprise Skill Packs (private domain-specific)
- Full multilingual skill content (top 5 languages)
- 4+ framework integrations

---

## HIGHEST PRIORITY NEXT ACTIONS

Based on PROJECT_MEMORY.md Section 15, the immediate execution sequence is:

1. **T-01** — Enable GitHub Discussions (2h, P0, no dependencies)
2. **T-02** — Tag 30 stubs as `good first issue` (3h, P0, depends on T-01)
3. **T-03** — Per-category README files (1d, P1, no dependencies)
4. **T-04** — Stub Upgrade Wave 1 (2w, P0, most downstream dependencies)
5. **T-11** — Skill graph JSON export (1d, P1, no dependencies — enables graph visualization)

---

## ARCHITECTURE DECISIONS (PERMANENT, from PROJECT_MEMORY.md Section 16)

The following are permanently rejected — do not propose them:

| Rejected Idea | Reason |
|---|---|
| Database backend for skills | Destroys diffability; Markdown-as-CMS is core design principle |
| Next.js / React frontend | Over-engineering; vanilla HTML keeps UI hackable by everyone |
| Enforce single programming language | Excludes legitimate TypeScript/Rust/Go skill examples |
| Auto-merge AI-generated content | LLMs produce plausible but incorrect code; human review required |
| Per-skill GitHub Pages subsite | Static site generator complexity outweighs SEO benefit at current scale |
| Discord (before 10+ contributors) | Empty Discord signals abandonment |
| Paid API tier | Developer audience growth depends on free access |

---

*Rebuilt from PROJECT_MEMORY.md during Mission R-01 on 2026-06-21.*
*Update only when a task from the roadmap is verifiably completed (commit evidence required).*
