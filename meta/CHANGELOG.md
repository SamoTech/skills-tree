# Changelog

All notable changes to Skills Tree are documented here.
Format: [Semantic Versioning](https://semver.org) · [Keep a Changelog](https://keepachangelog.com)

---

## [v2.1.0] — 2026-04-13

### Added
- **5 seed skill files** — full production-ready content:
  - `skills/02-reasoning/react.md` (v3 — runnable example, benchmark, typed I/O)
  - `skills/02-reasoning/chain-of-thought.md` (v2 — variants table, runnable example)
  - `skills/03-memory/memory-injection.md` (v2 — production path, mem0 integration)
  - `skills/09-agentic-patterns/rag.md` (v3 — 6 variants, full pipeline)
  - `skills/11-web/web-search.md` (v2 — provider comparison, agentic loop)
  - `skills/05-code/code-review.md` (v2 — JSON output, CI/CD integration)
- **1 full system** — `systems/research-agent.md` (decompose → search → extract → synthesize)
- **1 blueprint** — `blueprints/rag-stack.md` (full production RAG, deployment options)
- **2 benchmarks** — `benchmarks/reasoning/react-vs-lats.md`, `benchmarks/memory/injection-strategies.md`
- **1 lab** — `labs/reasoning/tree-of-agents.md` (multi-agent tree search, experimental)
- **Logo** — `docs/assets/logo-dark.svg` + `docs/assets/logo-light.svg` (adaptive `<picture>` tag in README)
- **Full badge suite** — Stars, Forks, Watchers, Views, Issues, PRs, Contributors, Last Commit, License, Skills count, Version, GitHub Pages
- **LEADERBOARD.md** — live contributor and skill rankings

### Changed
- README.md fully rewritten — viral hook, roadmap, vision, complete badge row, logo
- `meta/ROADMAP.md` fully rewritten — 6 phases, content strategy, distribution playbook
- `meta/LEADERBOARD.md` seeded with real data

---

## [v2.0.0] — 2026-04-12

### Added
- New folder structure: `/systems`, `/blueprints`, `/benchmarks`, `/labs`
- `docs/index.html` — interactive GitHub Pages UI (40KB, dark/light mode, search, filters)
- `meta/ROADMAP.md` — full strategic plan extracted from positioning brief
- `meta/LEADERBOARD.md` — placeholder for weekly rankings
- `meta/skill-schema.json` — JSON Schema for skill frontmatter validation
- `meta/glossary.md` — AI agent terminology reference
- `meta/frameworks.md` — framework compatibility matrix
- `meta/benchmark-template.md` — standard benchmark format
- `meta/system-template.md` — standard system format
- `.github/workflows/validate-skills.yml` — automated skill frontmatter validation
- `docs/404.html` — custom 404 page

### Changed
- `docs/index.html` — level-based filtering, count-up stats, improved card design
- All 16 skill category folders created and numbered

---

## [v1.0.0] — 2025-12

### Added
- Initial repository structure
- 16 skill category folders
- Basic README
- MIT License
- CONTRIBUTING.md
- GitHub Actions: check-links, validate-skills
- Issue templates: bug-report, new-skill, skill-update
- CODEOWNERS, FUNDING.yml
