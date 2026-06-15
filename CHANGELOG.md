# Changelog

All notable changes to `skills-tree` are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.0.3] — 2026-06-15

### Changed
- Bumped version from `1.0.2` to `1.0.3` (release-hardening patch).
- Added CI workflow `.github/workflows/build-and-verify.yml` that runs on every push to `main` and every PR:
  - Executes `python -m build` and fails if it exits non-zero.
  - Asserts `data/SKILLS_GRAPH.json`, `meta/GOAL_TAXONOMY.md`, and `benchmarks/INDEX.json` are present in the wheel.
  - Asserts `meta/GOAL_TAXONOMY.json` (phantom file) is **absent** from the wheel.
  - Runs `twine check dist/*` for metadata validation.
  - Uploads `dist/` as a downloadable artifact for 30 days.
- Added explicit inline comment in `pyproject.toml` `[tool.setuptools.data-files]` documenting the rule: *only list files that exist in the repository*.
- Added `CHANGELOG.md` (this file).

### Fixed
- Repository is now self-consistent: no references to `meta/GOAL_TAXONOMY.json` in any packaged configuration.

---

## [1.0.2] — 2026-06-15

### Fixed
- Removed `meta/GOAL_TAXONOMY.json` from `[tool.setuptools.data-files]` in `pyproject.toml`.
  The file does not exist in the repository and is not referenced by any runtime code.
  Its presence in the manifest caused `python -m build` to fail with:
  `error: can't copy 'meta/GOAL_TAXONOMY.json': doesn't exist or not a regular file`.

---

## [1.0.1] — 2026-06-15

### Added
- `MANIFEST.in` — `recursive-include` directives for `data/`, `benchmarks/`, `meta/`, `docs/`, `evaluation/`, `tests/`.
- `[tool.setuptools.data-files]` in `pyproject.toml` to ship top-level runtime assets (`data/SKILLS_GRAPH.json`, `meta/GOAL_TAXONOMY.md`, `benchmarks/INDEX.json`) into the wheel.
- `tools/data_resolver.py` — `importlib`-safe path resolver with `SKILLS_TREE_DATA_ROOT` env override.
- `[tool.setuptools]` `include-package-data = true`.
- Switched package discovery to `[tool.setuptools.packages.find]` auto-discovery.

### Fixed
- Wheel previously installed successfully but was missing all runtime data files because `[tool.setuptools.package-data]` globs are silently ignored for directories without `__init__.py`.

---

## [1.0.0] — 2026-06-15

### Added
- Initial release: CLI (`skills-tree`), FastAPI service, MCP server, recommendation engine, blueprint generator.
- 5 CLI commands: `recommend`, `blueprint`, `goals`, `skills`, `validate`.
- 36 CLI tests, 5 REST endpoints, 4 MCP tools.
- GitHub Pages portal (`docs/index.html`), Codespaces support, GitHub Actions blueprint generator.
