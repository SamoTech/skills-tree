# Automated Release Process

Repository: **SamoTech/skills-tree** | Mode: **Zero-touch, single pipeline**

---

## Architecture

### Before (two-workflow chain)

```
push to main
  │
  ▼
semantic-release.yml
  └─ creates tag
        │
        ▼  (tag push event)
      release.yml
        └─ build → PyPI → GitHub Release
```

**Problem:** GitHub Actions does not re-trigger workflows from pushes made
by `GITHUB_TOKEN`. The tag created by `semantic-release.yml` never fired
`release.yml`, so PyPI never received v1.1.0 or v1.1.1.

### After (single pipeline)

```
push to main
  │
  ▼
zero-touch-release.yml
  ├─ Job 1: semantic-release
  │       ├─ scan commits since last tag
  │       ├─ no releasable commits? → STOP (jobs 2–4 skipped)
  │       └─ releasable commits found:
  │               ├─ bump version in pyproject.toml
  │               ├─ update CHANGELOG.md
  │               ├─ commit "chore(release): vX.Y.Z [skip ci]"
  │               └─ push tag vX.Y.Z
  │
  ├─ Job 2: Build & Verify  (only if released=true)
  │       ├─ checkout tag
  │       ├─ assert pyproject version == tag
  │       ├─ python -m build
  │       ├─ twine check dist/*
  │       ├─ assert wheel assets present
  │       └─ upload dist/ artifact
  │
  ├─ Job 3: Publish → PyPI  (only if released=true)
  │       ├─ id-token:write at job level (OIDC scoping correct)
  │       ├─ environment: pypi
  │       └─ pypa/gh-action-pypi-publish (OIDC, no token)
  │
  └─ Job 4: Attach Release Assets  (only if released=true)
          ├─ softprops/action-gh-release
          └─ attach .whl + .tar.gz to GitHub Release
```

---

## Active Workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| `zero-touch-release.yml` | push to `main` | **Active** — full release pipeline |
| `release.yml` | `workflow_dispatch` only | Manual recovery for pre-existing tags |
| `semantic-release.yml` | `workflow_dispatch` only | Debug / manual override |
| `build-and-verify.yml` | push to `main` + PRs | Packaging sanity check (independent) |
| `clean-install-test.yml` | push to `main` + PRs | Clean environment test |

---

## PyPI Trusted Publisher — IMPORTANT UPDATE

Because the active workflow is now `zero-touch-release.yml`, you must update
the PyPI Trusted Publisher configuration to match the new workflow filename.

Go to: https://pypi.org/manage/project/skills-tree/settings/publishing/

| Field | Value |
|---|---|
| PyPI Project Name | `skills-tree` |
| Owner | `SamoTech` |
| Repository name | `skills-tree` |
| Workflow filename | **`zero-touch-release.yml`** |
| Environment name | `pypi` |

The old entry with `release.yml` should be **kept** for manual recovery runs.
Add a second entry for `zero-touch-release.yml`.

---

## One-Time Setup

1. **Update PyPI Trusted Publisher** (above) — add entry for `zero-touch-release.yml`.
2. **GitHub Environment** — `pypi` environment must exist:
   Repository → Settings → Environments → `pypi`.
   Optional: restrict to tags `v*.*.*`.
3. **No PAT required** — `GITHUB_TOKEN` is sufficient because build/publish
   runs in the same workflow run as semantic-release (not a separate triggered workflow).

---

## Developer Daily Workflow

```bash
# Write code. Use Conventional Commits. Push.
git commit -m "fix(api): improve ranking"
git push origin main
```

That is the complete developer action. The pipeline does the rest:

1. Scans commits → detects `fix:` → patch bump
2. Bumps `pyproject.toml` version (e.g. 1.1.1 → 1.1.2)
3. Updates `CHANGELOG.md`
4. Commits `chore(release): v1.1.2 [skip ci]`
5. Pushes tag `v1.1.2`
6. Builds wheel + sdist
7. Publishes to PyPI
8. Attaches assets to GitHub Release

**No manual version edit. No manual tag. No manual changelog.**

---

## Bump Rules

| Commit prefix | Bump | Example |
|---|---|---|
| `fix:` / `perf:` / `refactor:` | patch | `fix(api): improve ranking` |
| `feat:` | minor | `feat(cli): add dry-run flag` |
| `feat!:` / `BREAKING CHANGE` | major | `feat!: redesign API` |
| `docs:` / `chore:` / `ci:` / `test:` | none | `docs: update README` |

---

## Manual Recovery (v1.1.0, v1.1.1)

To publish tags that were created before this pipeline existed:

1. Go to Actions → **"Release → PyPI (manual recovery only)"**
2. Click **Run workflow**
3. Enter tag: `v1.1.0` → Run
4. Repeat with `v1.1.1`

Expected PyPI state after recovery: latest = `1.1.1`.
