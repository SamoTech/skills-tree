# Automated Release Process

Repository: **SamoTech/skills-tree** | Mode: **Zero-touch**

---

## The New Workflow (zero-touch)

```
Write code with Conventional Commits
        │
        ▼
git push / merge PR to main
        │
        ▼
semantic-release.yml (on every push to main)
        ├── Scan commits since last tag
        ├── No releasable commits? → STOP (nothing happens)
        └── Releasable commits found:
                ├── Bump version in pyproject.toml
                ├── Update CHANGELOG.md
                ├── Commit "chore(release): vX.Y.Z [skip ci]"
                └── Push tag vX.Y.Z
                        │
                        ▼
                release.yml (triggered by tag push)
                        ├── python -m build
                        ├── twine check dist/*
                        ├── Assert wheel assets present
                        ├── Publish → PyPI (OIDC)
                        └── Create GitHub Release + attach dist/
```

**No manual version edits. No manual tags. No manual changelog.**

---

## Bump Rules (Conventional Commits)

| Commit type | Bump | Example |
|---|---|---|
| `feat:` | **minor** | `feat: add blueprint caching` |
| `fix:` / `perf:` / `refactor:` | **patch** | `fix: handle empty graph` |
| `feat!:` or `BREAKING CHANGE:` | **major** | `feat!: redesign API` |
| `docs:` / `chore:` / `ci:` / `test:` | none | `docs: update README` |

---

## One-Time Setup

### 1. Create a Personal Access Token (PAT)

The default `GITHUB_TOKEN` cannot trigger other workflows. You need a PAT so that
the tag pushed by `semantic-release.yml` fires `release.yml`.

- Go to: **GitHub → Settings → Developer settings → Fine-grained tokens**
- Create a token with these permissions on `SamoTech/skills-tree`:
  - **Contents:** Read and write
  - **Metadata:** Read-only
- Copy the token value.

### 2. Store the PAT as a repository secret

- Go to: **Repository → Settings → Secrets and variables → Actions**
- Click **New repository secret**
- Name: `RELEASE_PAT`
- Value: (paste the PAT)

### 3. Configure PyPI Trusted Publisher

See the PyPI section in the original release docs or go directly to:
https://pypi.org/manage/project/skills-tree/settings/publishing/

Settings:

| Field | Value |
|---|---|
| PyPI Project Name | `skills-tree` |
| Owner | `SamoTech` |
| Repository name | `skills-tree` |
| Workflow filename | `release.yml` |
| Environment name | `pypi` |

### 4. Create the `pypi` GitHub Environment

**Repository → Settings → Environments → New environment**

- Name: `pypi`
- Deployment protection rules: restrict to tags matching `v*.*.*`

---

## Developer Workflow (daily use)

```bash
# Just write code and commit with Conventional Commits.
# Versioning, changelog, tagging, PyPI publish, and GitHub Release
# all happen automatically.

git commit -m "fix(engine): handle missing benchmarks directory"
git push origin main
# ↑ if this is the first fix since the last release, 1.0.3 → 1.0.4 happens automatically

git commit -m "feat(cli): add --dry-run flag"
git push origin main
# ↑ 1.0.4 → 1.1.0 happens automatically

git commit -m "docs: update README"
git push origin main
# ↑ no release triggered (docs: is not releasable)
```

---

## Bypassing Zero-Touch (emergency manual release)

If you need to release immediately without waiting for CI:

```bash
pip install python-semantic-release
semantic-release version   # bumps version + creates tag locally
git push origin main --follow-tags
# tag push triggers release.yml as normal
```

---

## Configuration Location

All semantic-release config lives in `pyproject.toml` under `[tool.semantic_release]`.
No separate `.releaserc` or `release.config.js` file is needed.

---

## Commit Convention Reference

See [`.github/COMMIT_CONVENTION.md`](./../.github/COMMIT_CONVENTION.md) for the full
Conventional Commits reference, scope list, and PR title guidance.
