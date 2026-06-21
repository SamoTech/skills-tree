# Workflow Security Audit

**Date:** 2026-06-21  
**Scope:** CodeQL alert — _"Workflow does not contain permissions"_  
**Auditor:** Ossama Hashim  
**Principle:** Least-privilege. Default `permissions: contents: read`. Only escalate when a workflow action provably requires it.

---

## Background

GitHub Actions workflows without an explicit `permissions` block inherit the repository's default token scope, which in many configurations defaults to `read-write` for `contents`. This violates the principle of least privilege and triggers CodeQL's `actions/missing-permissions` query. An attacker who compromises a workflow (e.g., via a malicious dependency or a script injection) inherits whatever permissions the `GITHUB_TOKEN` carries.

The fix is to add an explicit `permissions:` block at the workflow (top) level for every file that lacked one.

---

## Affected Workflows

### 1. `test-coverage.yml` — Test & Coverage

**Actions used:**
| Action | Purpose |
|---|---|
| `actions/checkout@v4` | Clone repository |
| `actions/setup-python@v5` | Install Python |
| `actions/upload-artifact@v4` | Upload `coverage.xml` |
| `codecov/codecov-action@v4` | Push coverage to Codecov (uses `CODECOV_TOKEN` secret, not `GITHUB_TOKEN`) |

**Permission analysis:**  
- `actions/checkout` needs `contents: read` to clone.  
- `actions/upload-artifact` writes to GitHub Actions artifact storage, **not** to repository contents. It does not need `contents: write`.  
- `codecov/codecov-action` authenticates via the `CODECOV_TOKEN` repository secret, not the `GITHUB_TOKEN`. No additional GitHub permission scope is required.  
- No step modifies repository files, creates comments, or interacts with issues/PRs.

**Permissions applied:**
```yaml
permissions:
  contents: read
```

---

### 2. `build-and-verify.yml` — Build & Verify Wheel

**Actions used:**
| Action | Purpose |
|---|---|
| `actions/checkout@v4` | Clone repository |
| `actions/setup-python@v5` | Install Python |
| `actions/upload-artifact@v4` | Upload `dist/` artifacts |

**In-job steps (no third-party actions):**  
- `pip install build twine` — pure shell  
- `python -m build` — produces `dist/*.whl` in the runner workspace  
- `python -m zipfile` — reads the built wheel locally  
- `twine check dist/*` — validates metadata locally; does not upload to PyPI  
- `$GITHUB_STEP_SUMMARY` writes — writes to the special runner file, not to repository contents

**Permission analysis:**  
- No step pushes to the repository.  
- `twine check` validates only; it does not upload.  
- Artifact upload writes to GitHub's artifact store, not repository contents.  
- `$GITHUB_STEP_SUMMARY` is a GitHub-managed runner file; writing it does not require any `GITHUB_TOKEN` scope.

**Permissions applied:**
```yaml
permissions:
  contents: read
```

---

### 3. `clean-install-test.yml` — C-12.75 Clean Install Test

**Actions used:**
| Action | Purpose |
|---|---|
| `actions/checkout@v4` | Clone repository |
| `actions/setup-python@v5` | Install Python |
| `actions/upload-artifact@v4` | Upload test outputs (`/tmp/*.json`, logs) |

**In-job steps (no third-party actions):**  
- `pip install -e .` — installs from local checkout  
- `skills-tree validate|goals|skills|recommend|blueprint` — CLI reads bundled data files  
- `pytest tests/` — reads test files and source code  
- `FastAPI TestClient` — in-process HTTP test, no external network calls to GitHub

**Permission analysis:**  
- All file I/O is within the runner's temp filesystem.  
- No step writes back to the repository (no `git push`, no `gh` CLI calls, no REST API mutations).  
- `GITHUB_STEP_SUMMARY` writes are runner-local.  
- Artifact upload does not require `contents: write`.

**Permissions applied:**
```yaml
permissions:
  contents: read
```

---

### 4. `verify-taxonomy.yml` — Taxonomy Integration Verification

**Actions used:**
| Action | Purpose |
|---|---|
| `actions/checkout@v4` | Clone repository |
| `actions/setup-python@v4` | Install Python |
| `actions/upload-artifact@v4` | Upload verification output files |

**In-job steps:**  
- `python tools/verify_taxonomy.py` — reads JSON/YAML data from the checked-out repo; writes result files to the runner workspace (`verify_before.json`, `verify_after.json`, `verify_diff.txt`, `verify_result.txt`)  
- No `git push` or GitHub API calls observed in `tools/verify_taxonomy.py`

**Permission analysis:**  
- Script reads local files only.  
- Output files are captured as artifacts, not committed back to the repository.  
- No repository-mutation operations.

**Permissions applied:**
```yaml
permissions:
  contents: read
```

---

## Permission Escalation Reference

For future workflows that **do** require additional scopes, document the justification here before merging:

| Permission | When legitimately needed | Example workflow |
|---|---|---|
| `contents: write` | Committing generated files back to the repo | `update-skill-count.yml`, `inject-badge-links.yml` |
| `pull-requests: write` | Posting automated comments on PRs | `skill-upgrade-comment.yml` |
| `issues: write` | Creating or updating issues automatically | `stale.yml` |
| `packages: write` | Publishing to GitHub Packages / GHCR | Any container publish step |
| `id-token: write` | OIDC-based cloud provider authentication (Vault, AWS, GCP) | Deployment workflows |
| `pages: write` + `id-token: write` | GitHub Pages deployment | `deploy-pages.yml` |
| `statuses: write` | Posting commit status checks | Custom status reporters |
| `checks: write` | Creating check runs | Custom CI reporters |

**Rule:** If a workflow needs `contents: write`, that step must be explicitly justified in a comment adjacent to the `permissions:` block.

---

## CodeQL Findings Expected to Close

| Alert | Rule | File |
|---|---|---|
| Workflow does not contain permissions | `actions/missing-permissions` | `.github/workflows/test-coverage.yml` |
| Workflow does not contain permissions | `actions/missing-permissions` | `.github/workflows/build-and-verify.yml` |
| Workflow does not contain permissions | `actions/missing-permissions` | `.github/workflows/clean-install-test.yml` |
| Workflow does not contain permissions | `actions/missing-permissions` | `.github/workflows/verify-taxonomy.yml` |

All four alerts should auto-close on the next CodeQL scan after this commit is merged to `main`.

---

## Non-Targeted Workflows (Out of Scope)

Workflows not listed in the original task scope are **not** modified in this commit. They will require a separate audit pass. Workflows that already had explicit `permissions:` blocks are unchanged.

---

_This file is part of the repository's security posture documentation. Update it whenever workflow permissions change._
