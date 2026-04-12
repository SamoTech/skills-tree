# Changelog

All notable changes to the AI Agent Skills Tree are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- CI workflow: skill format validation on every PR (`validate-skills.yml`)
- CI workflow: weekly external link health check (`check-links.yml`)
- `CODEOWNERS` file for review assignments
- Issue template: skill update form (`skill-update.md`)
- Issue template chooser config (`config.yml`)
- `meta/ROADMAP.md` — planned expansions and coverage gaps
- `meta/CHANGELOG.md` — this file
- `meta/skill-schema.json` — machine-readable skill metadata schema
- `docs/404.html` — custom GitHub Pages not-found page
- `docs/_config.yml` — GitHub Pages Jekyll configuration

---

## [1.2.0] — 2026-04

### Added
- **11 expanded skill files in `skills/01-perception/`**:
  - `chart-reading.md` — image chart parsing with base64 + URL support
  - `code-reading.md` — multi-language source file analysis
  - `database-reading.md` — NL-to-SQL pipeline for SQLite/PostgreSQL
  - `structured-data-reading.md` — JSON/YAML/TOML/CSV normalization
  - `file-system-reading.md` — directory traversal and summarization
  - `email-parsing.md` — MIME-aware email structured extraction
  - `screen-reading.md` — UI state extraction from screenshots
  - `sensor-reading.md` — IoT/telemetry anomaly detection pipeline
  - `pdf-parsing.md` — native Claude document block + pypdf fallback
  - `url-dom-inspection.md` — httpx + BeautifulSoup web page intelligence
  - `handwriting-recognition.md` — multi-format handwritten text transcription
- **4 expanded skill files in `skills/02-reasoning/`**:
  - `abductive.md` — ranked hypothesis generation with falsification tests
  - `analogical.md` — structural analogy mapping across domains
  - `causal.md` — causal chain analysis with confounder detection
  - `commonsense.md` — implicit world knowledge inference
- **7 expanded skill files in `skills/03-memory/`**:
  - `fact-verification.md` — claim classification (verified/contradicted/uncertain)
  - `forgetting.md` — GDPR-aware hard/soft memory deletion
  - `memory-injection.md` — fact extraction + mem0 storage pipeline
  - `memory-summarization.md` — rolling compression for long-running agents
  - `procedural.md` — how-to knowledge store with versioning
  - `user-profile.md` — confidence-gated signal extraction from conversations

### Changed
- All expanded files include: full description, inputs/outputs table, runnable Python example, frameworks table, notes, related skills, and per-file changelog

---

## [1.1.0] — 2025-04

### Added
- Redesigned `docs/index.html` with full dark/light mode toggle
- Level-based filtering (Basic / Intermediate / Advanced / Experimental)
- Real-time search synced across navbar and hero search bar
- Count-up animation for hero statistics
- CSS scroll-driven reveal animations
- Accessible empty state when search yields no results
- Stats bar highlighting key category counts
- Card redesign: gradient top-edge, skill level badges, browse CTA

### Fixed
- Level filter buttons were non-functional — now correctly filter categories
- Search previously case-sensitive — now case-insensitive

---

## [1.0.0] — 2025-03

### Added
- Initial release of the AI Agent Skills Tree
- 16 skill categories covering the full agent capability spectrum
- 515+ individual skill files in Markdown format
- `meta/skill-template.md` — standard template for new skills
- `meta/glossary.md` — definitions for all key terms
- `meta/frameworks.md` — framework and model reference
- `CONTRIBUTING.md` — contribution guide
- `SECURITY.md` — security and responsible use policy
- `SPONSORS.md` — sponsorship information
- GitHub issue templates: bug report, new skill request
- GitHub Pages documentation site (`docs/index.html`)
