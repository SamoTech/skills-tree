# PyPI Release and Distribution Contract

Status: current repository release contract, verified 2026-10-03.

This document describes the release mechanism actually configured in the repository. Historical C-11 planning material is intentionally replaced here because it no longer describes the executable release path.

## Package identity

- Project: `skills-tree`
- Repository: `SamoTech/skills-tree`
- Python requirement: `>=3.11`
- Repository version at this audit: `1.68.0`
- Version source of truth: `pyproject.toml [project].version`
- Console entry point: `skills-tree = cli.main:app`

The repository package is a beta-stage installable distribution. Release readiness is determined by the executable CI/release gates, not by this document.

## Versioning

The repository uses semantic-release configuration in `pyproject.toml`.

Relevant commit classification:
- `feat` → minor release
- `fix`, `perf`, `refactor` → patch release
- other allowed tags may participate according to semantic-release configuration
- release commits use `chore(release): v{version} [skip ci]`
- tags use `v{version}`

The version in `pyproject.toml` and the release tag must agree before an artifact is built.

## Executable release pipeline

The authoritative workflow is:

`.github/workflows/zero-touch-release.yml`

It runs on every push to `main` and performs:

1. Semantic-release version calculation.
2. Verification of the resulting version/tag state.
3. Checkout of the release tag.
4. Build of sdist and wheel.
5. `twine check`.
6. Verification that required runtime assets are present in the wheel.
7. PyPI publication through GitHub OIDC Trusted Publishing.
8. Attachment of the built artifacts to the GitHub Release.

If semantic-release determines that there is no releasable change, downstream build/publish jobs are skipped.

## Trusted Publishing

PyPI publication does not use the historical `PYPI_API_TOKEN` workflow described in older documentation.

The executable workflow uses:
- GitHub Actions OIDC
- job-level `id-token: write` on the PyPI publishing job
- PyPI environment: `pypi`
- workflow filename: `zero-touch-release.yml`
- publisher repository: `SamoTech/skills-tree`

The workflow contains an OIDC pre-flight check that verifies the repository and workflow identity before publication.

No long-lived PyPI API token is required by the current release workflow.

## Build verification

The release workflow builds both:
- source distribution
- Python wheel

It verifies the wheel contains these required runtime assets:

- `data/SKILLS_GRAPH.json`
- `meta/GOAL_TAXONOMY.md`
- `benchmarks/INDEX.json`

It also runs `twine check` and checks for a matching CHANGELOG entry.

The normal PR CI remains a separate prerequisite for repository changes. A successful release workflow does not replace the repository's test, security, build, integrity, provenance, and documentation gates.

## Developer validation

Before a release-bearing change is merged, use the repository's normal validation gates. The executable CLI boundary currently includes:

```bash
pip install -e .
skills-tree validate
skills-tree recommend --goal "Coding Agent"
skills-tree blueprint --goal "Coding Agent"
```

The repository does not currently expose the historical `skills-tree search`, `show`, `list`, or `categories` commands.

## Installation

Published releases can be installed with:

```bash
pip install skills-tree
```

Development installation:

```bash
git clone https://github.com/SamoTech/skills-tree
cd skills-tree
pip install -e .[dev]
```

For an agent consuming Skills Tree as a knowledge source, the canonical discovery guidance is to inspect `docs/api/skills.json`, then open the canonical skill file and verify evidence, dependencies, security boundaries, and freshness before relying on it.

## Upgrade strategy

Consumers that require a controlled compatibility boundary should pin an explicit release version rather than relying on an unbounded latest install.

The repository does not claim that a version pin alone establishes skill safety or production readiness; consumers must inspect the relevant skill evidence and limitations.

## Historical material

Older references to `publish.yml`, `PYPI_API_TOKEN`, TestPyPI staging, version `1.0.0`, or a manual `twine upload` production step are historical planning material and are not the current executable release contract.
