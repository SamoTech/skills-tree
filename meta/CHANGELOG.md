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
