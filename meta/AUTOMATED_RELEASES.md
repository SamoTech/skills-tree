# Automated Release Process

Repository: **SamoTech/skills-tree**

---

## How to Release

The entire release process is four commands:

```bash
# 1. Bump the version in pyproject.toml
vim pyproject.toml   # change version = "1.0.3" to "1.0.4" (or whatever)

# 2. Commit
git add pyproject.toml CHANGELOG.md
git commit -m "chore(release): v1.0.4"

# 3. Tag
git tag v1.0.4

# 4. Push the tag
git push origin v1.0.4
```

Everything else is automatic.

---

## What Happens Automatically

```
git push origin vX.Y.Z
        │
        ▼
.github/workflows/release.yml triggered
        │
        ├── Stage 1: Build & verify
        │       ├── pip install build twine
        │       ├── Assert pyproject.toml version == tag
        │       ├── python -m build
        │       ├── twine check dist/*           ← fails here if metadata broken
        │       ├── Assert wheel contains:
        │       │       data/SKILLS_GRAPH.json
        │       │       meta/GOAL_TAXONOMY.md
        │       │       benchmarks/INDEX.json
        │       └── Upload dist/ artifact
        │
        ├── Stage 2: Publish → PyPI  (needs Stage 1 to pass)
        │       └── pypa/gh-action-pypi-publish (OIDC, no token)
        │
        └── Stage 3: GitHub Release  (needs Stage 1 + Stage 2)
                ├── Extract release notes from CHANGELOG.md
                ├── Create GitHub Release (draft=false)
                └── Attach .whl + .tar.gz as release assets
```

If any stage fails, all downstream stages are skipped. The PyPI publish never runs if the build or quality gates fail.

---

## One-Time Setup: PyPI Trusted Publisher

This workflow uses **OIDC Trusted Publisher** — no API token or secret is needed. You must configure it once on PyPI.

### Step 1 — Log in to PyPI

Go to: https://pypi.org/manage/project/skills-tree/settings/publishing/

(If the project does not exist yet, create it first with a manual upload or `twine upload`.)

### Step 2 — Add a Trusted Publisher

Click **"Add a new publisher"** and fill in:

| Field | Value |
|---|---|
| PyPI Project Name | `skills-tree` |
| Owner | `SamoTech` |
| Repository name | `skills-tree` |
| Workflow filename | `release.yml` |
| Environment name | `pypi` |

### Step 3 — Create the GitHub Environment

In the repository: **Settings → Environments → New environment**

- Name: `pypi`
- Optional: add a required reviewer (e.g. yourself) for extra protection
- Optional: restrict to tag patterns `v*.*.*`

### Step 4 — Verify

Push a test tag (e.g. `v1.0.4-rc1`) and watch the workflow at:
https://github.com/SamoTech/skills-tree/actions/workflows/release.yml

---

## Workflow Permissions

```yaml
permissions:
  id-token: write   # required for OIDC token exchange with PyPI
  contents: write   # required to create GitHub Release and attach assets
```

These are declared at the top of `release.yml` and apply only to the release workflow. No repository-wide permission changes are needed.

---

## Version Mismatch Guard

The workflow asserts that `pyproject.toml version` == `git tag` before building. If they differ, the build fails immediately with a clear error:

```
ERROR: pyproject.toml version (1.0.3) != tag (1.0.4)
Bump the version in pyproject.toml and re-tag.
```

This prevents accidentally publishing the wrong version.

---

## Pre-release Tags

Tags containing `-rc`, `-beta`, or `-alpha` are automatically marked as **pre-release** on GitHub. They are still published to PyPI normally.

Examples:
- `v1.1.0-rc1` → GitHub pre-release, PyPI release
- `v1.1.0` → GitHub stable release, PyPI release

---

## Failure Modes

| Failure | Stage | Effect |
|---|---|---|
| `pyproject.toml` version ≠ tag | Build | Immediate exit 1; no publish |
| `python -m build` error | Build | Immediate exit 1; no publish |
| `twine check` fails | Build | Immediate exit 1; no publish |
| Required wheel asset missing | Build | Immediate exit 1; no publish |
| PyPI OIDC misconfigured | Publish | Build artifacts available, but not published |
| GitHub token issue | Release | Published to PyPI but no GitHub Release |

---

## Artifacts

Even if the GitHub Release step fails, the built `dist/` folder is available as a GitHub Actions artifact for 7 days under the name `dist`.

Download at:
```
https://github.com/SamoTech/skills-tree/actions/workflows/release.yml
```
