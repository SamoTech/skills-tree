# Automated Release Process

Repository: **SamoTech/skills-tree** | Mode: **Zero-touch, single pipeline**

---

## Is Any Manual Action Required?

### One-time setup (humans required once, never again after)

| Action | Where | When |
|---|---|---|
| Add PyPI Trusted Publisher entry | pypi.org | Once, before first release |
| Create `pypi` GitHub Environment | GitHub repo settings | Once |

### Per-release actions (humans required: zero)

| Action | Automated by |
|---|---|
| Version bump | semantic-release |
| CHANGELOG update | semantic-release |
| Git tag creation | semantic-release |
| Build sdist + wheel | zero-touch-release.yml Job 2 |
| PyPI publish | zero-touch-release.yml Job 3 |
| GitHub Release creation | semantic-release |
| Release asset attachment | zero-touch-release.yml Job 4 |

**After one-time setup: git commit + git push = full release. Nothing else.**

---

## Final Architecture

```
git commit -m "fix(api): improve ranking"
git push origin main
        │
        ▼
zero-touch-release.yml  (triggered by push to main)
        │
        ├─── Job 1: Semantic Release
        │         ├─ scan commits since last tag
        │         ├─ no releasable commits? → STOP (jobs 2–4 skipped via if-gate)
        │         └─ releasable commits found:
        │                 ├─ bump version in pyproject.toml
        │                 ├─ update CHANGELOG.md
        │                 ├─ commit "chore(release): vX.Y.Z [skip ci]"
        │                 └─ push tag vX.Y.Z
        │                   outputs: released=true, version=X.Y.Z, tag=vX.Y.Z
        │
        ├─── Job 2: Build & Verify          (skipped if released=false)
        │         ├─ checkout tag vX.Y.Z
        │         ├─ assert pyproject version == tag
        │         ├─ python -m build
        │         ├─ twine check dist/*
        │         ├─ assert data/SKILLS_GRAPH.json in wheel
        │         ├─ assert meta/GOAL_TAXONOMY.md in wheel
        │         ├─ assert benchmarks/INDEX.json in wheel
        │         └─ upload dist/ artifact
        │
        ├─── Job 3: Publish → PyPI          (skipped if released=false)
        │         ├─ id-token:write at job level
        │         ├─ environment: pypi
        │         ├─ OIDC pre-flight check:
        │         │     ├─ print repository, workflow, environment
        │         │     └─ fail with actionable error if mismatch
        │         └─ pypa/gh-action-pypi-publish (OIDC, no token, no secret)
        │
        └─── Job 4: Attach Release Assets   (skipped if released=false)
                  ├─ softprops/action-gh-release
                  └─ attach .whl + .tar.gz to GitHub Release
```

---

## Active Workflows

| Workflow | Trigger | Role |
|---|---|---|
| `zero-touch-release.yml` | push to `main` | ✅ **Production release pipeline** |
| `build-and-verify.yml` | push to `main` + PRs | ✅ Packaging sanity check |
| `clean-install-test.yml` | push to `main` + PRs | ✅ Environment test |
| `release.yml` | `workflow_dispatch` only | 🔧 Manual recovery for old tags |
| `semantic-release.yml` | `workflow_dispatch` only | 🔧 Debug override |

---

## One-Time Setup (do once, never repeat)

### 1. PyPI Trusted Publisher

URL: https://pypi.org/manage/project/skills-tree/settings/publishing/

Add entry:

| Field | Value |
|---|---|
| PyPI project name | `skills-tree` |
| Owner | `SamoTech` |
| Repository name | `skills-tree` |
| **Workflow filename** | **`zero-touch-release.yml`** |
| **Environment name** | **`pypi`** |

Also keep the existing `release.yml` entry for manual recovery.

### 2. GitHub Environment

Repository → Settings → Environments → New environment

- Name: `pypi`
- Optional deployment protection: restrict to tags `v*.*.*`

### 3. No secrets required

`GITHUB_TOKEN` is sufficient. No `RELEASE_PAT`, no `PYPI_API_TOKEN`.

---

## OIDC Pre-flight Validation

The `publish-pypi` job runs a shell validation step before calling
`pypa/gh-action-pypi-publish`. It prints the three values PyPI
validates and fails with a clear error if they do not match:

```
=== OIDC Trusted Publisher pre-flight ===

  Repository : SamoTech/skills-tree
  Workflow   : zero-touch-release.yml
  Environment: pypi

  ✅ repository matches
  ✅ workflow filename matches
  ✅ environment: pypi

=== OIDC pre-flight PASSED — proceeding to publish ===
```

If there is a mismatch (e.g. workflow was renamed), the step fails with:

```
  ERROR: workflow filename mismatch
         got      : new-name.yml
         expected : zero-touch-release.yml
  Fix: update the Workflow filename field in the Trusted Publisher.

Required PyPI Trusted Publisher settings:
  PyPI project name : skills-tree
  Owner             : SamoTech
  Repository        : skills-tree
  Workflow filename : zero-touch-release.yml
  Environment       : pypi
```

---

## Developer Daily Workflow

```bash
git commit -m "fix(api): improve ranking"
git push origin main
# Done. PyPI release in ~3 minutes.
```

### What happens automatically

1. `fix:` prefix → patch bump (e.g. 1.1.1 → 1.1.2)
2. `pyproject.toml` version updated
3. `CHANGELOG.md` updated
4. Commit `chore(release): v1.1.2 [skip ci]` pushed
5. Tag `v1.1.2` pushed
6. Wheel + sdist built and verified
7. Published to PyPI (`pip install skills-tree` returns `1.1.2`)
8. `.whl` + `.tar.gz` attached to GitHub Release

---

## Bump Rules (Conventional Commits)

| Prefix | Bump | Example |
|---|---|---|
| `fix:` / `perf:` / `refactor:` | patch | `fix(api): improve ranking` |
| `feat:` | minor | `feat(cli): add dry-run` |
| `feat!:` or `BREAKING CHANGE` | major | `feat!: redesign API` |
| `docs:` / `chore:` / `ci:` / `test:` | none (no release) | `docs: update README` |

---

## Manual Recovery (v1.1.0, v1.1.1)

For tags created before zero-touch-release.yml existed:

1. Actions → **"Release → PyPI (manual recovery only)"**
2. Run workflow → enter tag `v1.1.0` → Run
3. Repeat with `v1.1.1`

Expected PyPI state after recovery: latest = `1.1.1`.

---

## Human Actions Required Per Timeframe

| Timeframe | Required human action |
|---|---|
| Per release | **Zero** |
| Per month | **Zero** |
| Per year | **Zero** |
| On repo creation | One-time PyPI Trusted Publisher + GitHub Environment setup |
| On workflow rename | Update PyPI Trusted Publisher workflow filename field |
