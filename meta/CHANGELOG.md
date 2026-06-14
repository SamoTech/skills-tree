# Changelog

All notable changes to Skills Tree are documented here.
Format: [Semantic Versioning](https://semver.org) · [Keep a Changelog](https://keepachangelog.com)

---

## [v2.3.0] — 2026-06-14

### Added
- **`meta/EXECUTION_PRIORITY_MATRIX.md`** — Impact-scored, ROI-ordered execution backlog for all 25 remaining tasks. Scores every task across 5 dimensions (Product Value, User Value, Adoption Impact, Technical Leverage, Sponsor Attractiveness). Reorders roadmap into 6 capability-first waves. Rejects 4 marketing/community tasks below the 25/50 threshold. Product capability work: 95.5% of total effort.
- **`meta/CONTRIBUTING.md` — 5-minute quickstart** (T-17 ✅) — New "⚡ 5-Minute First Contribution" section with step-by-step fork → branch → edit → PR flow. Table of contents, PR template, commit convention, and full PR checklist added.
- **`meta/START-HERE-DISCUSSION.md`** — Pinned community onboarding post ready for GitHub Discussions, with directory tour, contribution priorities table, and labels guide.
- **`meta/LAUNCH-ANNOUNCEMENT.md`** — Three ready-to-post announcement drafts: Show HN, Reddit r/MachineLearning, LinkedIn.
- **`.github/workflows/release-package.yml`** (T-16 ✅) — New workflow triggered on `v*.*.*` tag pushes. Produces `skills-tree-{version}.zip` + `MANIFEST.json` and attaches them to the GitHub Release as downloadable assets. ZIP contains: `skills/`, `systems/`, `blueprints/`, `benchmarks/`, `labs/`, `api/skills.json`, `api/skills.yaml`, `api/skills-schema.json`.
- **`tools/package_release.py`** (T-16 ✅) — Python packaging script. Computes SHA-256 checksum, writes `MANIFEST.json` with skill counts (total, v1, v2, v3), category count, file count, zip size, commit SHA, and download URL. Runnable standalone: `python3 tools/package_release.py --tag v2.3.0`.

### Changed
- `meta/ROADMAP.md` — T-16 and T-17 marked ✅ Done in the Phase 2 table. Wave 0 release packaging row updated.
- `PROJECT_MEMORY.md` — Section 2 (Existing Functionality) updated to reflect new workflows and scripts; Section 3 (Technical Debt) updated; Section 5 (Master Feature Backlog) P2-5 marked complete.

### Measurable Outcomes (T-16)
- **GitHub Release assets count:** was `0` per release → now `2` per tag push (`skills-tree-{version}.zip` + `MANIFEST.json`)
- **Offline usability:** researchers can cite a specific tagged artifact with SHA-256 checksum
- **CLI prerequisite:** release zip satisfies the bundled-data requirement for `pip install skills-tree` (T-19)
- **Download count:** visible in GitHub Releases UI, tracked passively

---

## [v2.2.0] — 2026-04-13

### Added
- **4 new blueprints** with full implementations:
  - `blueprints/multi-agent-mesh.md` — N parallel specialists + orchestrator + merger + debate variant
  - `blueprints/human-in-the-loop.md` — Risk classifier, approval gate, audit log, Slack/email channels
  - `blueprints/self-healing-agent.md` — Error classification, exponential backoff retry, checkpoint, rollback
  - `blueprints/memory-first-agent.md` — Profile + episodic + semantic vector memory, 3-layer injection
- **2 new labs experiments:**
  - `labs/memory/episodic-compression.md` — Lossy session compression at 10-15x ratio, dedup, temporal decay
  - `labs/tool-use/adaptive-tool-selection.md` — Two-stage routing, -76% token cost, benchmark vs full registry
- **1 new benchmark** — `benchmarks/memory/rag-retrieval-strategies.md` (HyDE +12% recall, 6 strategies × 2 datasets)
- **Logo SVGs** — `docs/assets/logo-dark.svg` + `docs/assets/logo-light.svg` added to `docs/index.html` nav
- **Views badge** fixed in README (hits.seeyoufarm.com)

### Fixed
- `blueprints/README.md` — updated to list all 7 blueprints including 4 new ones
- `labs/README.md` — updated to list all 3 active lab experiments
- Broken README benchmark link (`rag-retrieval-strategies.md` now exists)

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
