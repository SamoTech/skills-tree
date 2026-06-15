# Commit Convention

This repository uses **Conventional Commits** as the single source of truth for
automatic versioning and changelog generation.

https://www.conventionalcommits.org/en/v1.0.0/

---

## Format

```
<type>(<optional scope>): <short description>

[optional body]

[optional footer(s)]
```

---

## Types and Their Version Impact

| Type | Example | Version bump | Appears in CHANGELOG |
|---|---|---|---|
| `feat` | `feat: add blueprint caching` | **minor** (1.0.x → 1.1.0) | ✅ |
| `fix` | `fix: handle missing graph file` | **patch** (1.0.3 → 1.0.4) | ✅ |
| `perf` | `perf: cache taxonomy at startup` | **patch** | ✅ |
| `refactor` | `refactor: extract engine loader` | **patch** | ✅ |
| `BREAKING CHANGE` | footer or `feat!:` | **major** (1.x.x → 2.0.0) | ✅ |
| `docs` | `docs: update README` | none | ❌ |
| `chore` | `chore: update deps` | none | ❌ |
| `ci` | `ci: add matrix test` | none | ❌ |
| `test` | `test: add blueprint edge cases` | none | ❌ |
| `style` | `style: fix ruff warnings` | none | ❌ |
| `build` | `build: update setuptools` | none | ❌ |

---

## Breaking Changes

Two ways to declare a breaking change (both trigger a **major** bump):

**Option A — `!` after type:**
```
feat!: redesign recommendation API
```

**Option B — footer:**
```
feat: redesign recommendation API

BREAKING CHANGE: /recommend now requires `experience` field
```

---

## Scopes (optional but recommended)

| Scope | Meaning |
|---|---|
| `api` | FastAPI routes |
| `cli` | CLI commands |
| `mcp` | MCP server tools |
| `engine` | Recommendation / blueprint engine |
| `packaging` | pyproject.toml, MANIFEST.in, data files |
| `ci` | GitHub Actions workflows |
| `docs` | Documentation files |
| `release` | Release infrastructure |

---

## Examples

```bash
# Patch release — bug fix
git commit -m "fix(engine): handle missing benchmarks directory gracefully"

# Minor release — new feature
git commit -m "feat(cli): add --dry-run flag to recommend command"

# Major release — breaking change
git commit -m "feat(api)!: remove deprecated /v0/recommend endpoint"

# No release — documentation update
git commit -m "docs: add MCP quickstart guide"

# No release — CI change
git commit -m "ci: add Python 3.13 to test matrix"
```

---

## What Happens When You Push to `main`

1. `semantic-release.yml` runs on every push to `main`.
2. It scans commits since the last tag.
3. If any commit matches `feat`, `fix`, `perf`, or `refactor` — or contains `BREAKING CHANGE` — it:
   - Bumps `version` in `pyproject.toml`
   - Updates `CHANGELOG.md`
   - Commits both with `chore(release): vX.Y.Z [skip ci]`
   - Pushes the tag `vX.Y.Z`
4. The tag push triggers `release.yml`, which builds, publishes to PyPI, and creates the GitHub Release.
5. If no releasable commits exist, nothing happens.

---

## PR Title Convention

When squash-merging PRs, the PR title becomes the commit message. Follow the same
Conventional Commits format in PR titles so the squash merge produces a correctly
formatted commit automatically.
