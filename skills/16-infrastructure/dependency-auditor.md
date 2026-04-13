---
title: "Dependency Auditor"
category: infrastructure
phase: 3
stability: stable
added: "2025-03"
level: advanced
tags:
  - dependency-management
  - badge-pipeline
  - execution-gap
  - security
  - devops
  - ci-cd
  - venv
  - sbom
deps:
  - httpx
  - packaging
badge: machine-inferred · 2 pkgs
badge_key: skills-16-infrastructure-dependency-auditor
description: >
  Closes the Execution Gap between "package exists on PyPI" (Yellow badge)
  and "code actually runs" (Green badge). Spins up an isolated venv per skill,
  installs its declared dependencies, executes the skill's Python snippets,
  and proposes a human-reviewed PR to promote the badge from Yellow → Green.
  Implements the Human-in-the-Loop contract: the badge never promotes itself.
author: "@SamoTech"
updated: "2026-04-13"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-infrastructure-dependency-auditor.json)

# Dependency Auditor

> **Phase 3 of the Dependency Watchdog pipeline.**
> Closes the gap between *Package Exists* (🟡 Yellow) and *Code Runs* (🟢 Green).

## The Execution Gap

The AST Sweep (Phase 1) confirms that a skill's declared packages exist on PyPI
and are free of known CVEs. But existence ≠ execution. A package might:

- Have breaking API changes in its latest release
- Require a native system dependency (e.g. `libssl`, `libpq`) absent from the runner
- Conflict with another skill's dependencies when installed together
- Simply have a typo in its import path in the code example

The Dependency Auditor solves this by **running the code**, not just scanning it.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  dependency-auditor.yml  (GitHub Actions)                       │
│                                                                 │
│  trigger: PR touching skills/**/*.md  OR  weekly cron           │
│                                                                 │
│  1. Find skill files with Yellow badges (machine-inferred)      │
│  2. For each skill:                                             │
│     a. Create tempfile.TemporaryDirectory()                     │
│     b. venv.create(tmp_dir, clear=True, with_pip=True)          │
│     c. pip install <declared deps>                              │
│     d. Extract Python snippets from the skill Markdown          │
│     e. subprocess.run(snippet, venv python, timeout=30s)        │
│     f. Emit verdict: "pass" | "fail" | "skip"                   │
│  3. Write badge JSONs for passing skills                        │
│  4. Open a verification PR for human sign-off (Yellow → Green)  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Isolation Strategy

Each skill runs in a **completely independent virtual environment**.
This prevents dependency bleed between skills — Skill A's `numpy==1.26`
cannot shadow Skill B's `numpy==2.1`.

```python
import venv
import tempfile
import subprocess
import sys
from pathlib import Path

def create_isolated_env(deps: list[str]) -> Path:
    """
    Create a throw-away venv, install deps, return the python executable path.
    The TemporaryDirectory is managed by the caller's context manager.
    """
    tmp = tempfile.mkdtemp(prefix="skill-audit-")
    env_path = Path(tmp) / "env"

    # clear=True: nuke any existing env at that path (idempotent)
    # with_pip=True: bootstrap pip inside the venv automatically
    venv.create(str(env_path), clear=True, with_pip=True)

    python = env_path / "bin" / "python"  # Linux/macOS
    if not python.exists():
        python = env_path / "Scripts" / "python.exe"  # Windows

    if deps:
        subprocess.run(
            [str(python), "-m", "pip", "install", "--quiet", *deps],
            check=True,
            timeout=120,
        )

    return python
```

> **Why not a single shared venv for all skills?**
> Because conflicts between skill deps would produce false results.
> Skill A might pass *only because* Skill B's dep happened to satisfy its import.
> Isolation ensures every Green badge is independently earned.

---

## Verdict Logic

The auditor distinguishes three outcomes. The distinction between `skip` and `fail`
is the single most important design decision — it keeps the CI signal clean.

| Verdict | Condition | Badge Action |
|---|---|---|
| `pass` | Snippet exits 0, no ImportError/RuntimeError | Promote Yellow → 🟢 Green (via PR) |
| `fail` | Snippet exits non-zero, or raises on import | Stays Yellow, opens issue with traceback |
| `skip` | No Python snippets found, or skill has no deps declared | No badge change, not flagged as broken |

```python
from dataclasses import dataclass, field
from enum import Enum

class Verdict(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"

@dataclass
class AuditResult:
    skill_path: str
    verdict: Verdict
    deps: list[str] = field(default_factory=list)
    snippets_run: int = 0
    error: str = ""
    duration_ms: float = 0.0

def run_snippet(python: str, snippet: str, timeout: int = 30) -> tuple[bool, str]:
    """
    Execute a Python snippet in the isolated environment.
    Returns (success, stderr_output).
    """
    import subprocess
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False
    ) as f:
        f.write(snippet)
        tmp_path = f.name

    try:
        result = subprocess.run(
            [python, tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode == 0, result.stderr
    except subprocess.TimeoutExpired:
        return False, f"Snippet timed out after {timeout}s"
    finally:
        os.unlink(tmp_path)

def audit_skill(skill_path: str, deps: list[str], snippets: list[str]) -> AuditResult:
    """Full audit lifecycle for a single skill."""
    if not snippets or not deps:
        return AuditResult(skill_path=skill_path, verdict=Verdict.SKIP)

    try:
        python = str(create_isolated_env(deps))
    except subprocess.CalledProcessError as e:
        return AuditResult(
            skill_path=skill_path,
            verdict=Verdict.FAIL,
            deps=deps,
            error=f"pip install failed: {e}",
        )

    for i, snippet in enumerate(snippets):
        success, stderr = run_snippet(python, snippet)
        if not success:
            return AuditResult(
                skill_path=skill_path,
                verdict=Verdict.FAIL,
                deps=deps,
                snippets_run=i,
                error=stderr[:500],
            )

    return AuditResult(
        skill_path=skill_path,
        verdict=Verdict.PASS,
        deps=deps,
        snippets_run=len(snippets),
    )
```

---

## The Human-in-the-Loop Contract

The badge **never promotes itself**. A passing audit produces a *patch* — a
proposed frontmatter diff — which is committed to a new branch and opened as
a Pull Request. A maintainer must review and merge it.

This is the critical security feature. Without it, a snippet that passes due
to a flaky network call or a temporary PyPI outage could silently award a
Green badge that isn't earned.

```python
import json
from pathlib import Path
from datetime import datetime, timezone

def generate_verified_frontmatter_patch(result: AuditResult) -> dict:
    """
    Return a badge JSON representing the Green (verified) state.

    This is a PROPOSAL, not a write. The caller (the GitHub Actions workflow)
    commits this to a branch and opens a PR. A human merges the PR.
    The badge never writes itself to Green.
    """
    assert result.verdict == Verdict.PASS, "Only PASS results can become Green"

    return {
        "schemaVersion": 1,
        "label": "deps",
        "message": "\u2714 verified",
        "color": "22c55e",
        "style": "flat-square",
        "namedLogo": "checkmarx",
        "_meta": {
            "promoted_by": "dependency-auditor",
            "promoted_at": datetime.now(timezone.utc).isoformat(),
            "deps_installed": result.deps,
            "snippets_verified": result.snippets_run,
            "requires_human_merge": True,
        },
    }

def write_verification_pr_body(results: list[AuditResult]) -> str:
    """Generate the PR description for a batch of Green promotions."""
    passing = [r for r in results if r.verdict == Verdict.PASS]
    failing = [r for r in results if r.verdict == Verdict.FAIL]

    lines = [
        "# \U0001f7e2 Dependency Auditor — Verification PR",
        "",
        "> This PR was opened automatically by `dependency-auditor.yml`.",
        "> A maintainer must review and merge to promote badges from Yellow \u2192 Green.",
        "> **Do not merge** if any skill listed here has changed since this PR was opened.",
        "",
        "## Proposed Promotions (Yellow \u2192 \U0001f7e2 Green)",
        "",
    ]

    for r in passing:
        lines.append(f"- `{r.skill_path}` — {len(r.deps)} dep(s) installed, "
                     f"{r.snippets_run} snippet(s) executed successfully")

    if failing:
        lines += [
            "",
            "## \u26a0\ufe0f Failing Skills (NOT promoted, kept Yellow)",
            "",
        ]
        for r in failing:
            lines.append(f"- `{r.skill_path}` — `{r.error[:120]}`")

    lines += [
        "",
        "---",
        f"*Generated by `tools/dependency_auditor.py` on "
        f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*",
    ]

    return "\n".join(lines)
```

---

## Recursive Dogfooding

This skill (`dependency-auditor.md`) is itself subject to the badge pipeline it describes.

- Its own `httpx` and `packaging` imports are scanned by the AST Sweep → Yellow badge
- The Dependency Auditor runs its own snippets in an isolated venv
- If they pass → a verification PR is opened → a maintainer merges → Green badge

The tool that audits the repository is audited by the repository.
This is the self-healing property of the infrastructure.

---

## Security: Network Constraint Model

> See [`SECURITY.md`](../../SECURITY.md#phase-3-execution-gap--network-constraints) for the full threat model.

The short version:

| Risk Level | Scenario | Mitigation |
|---|---|---|
| Low (current) | Trusted contributor PRs, reviewed before merge | Ephemeral GH runner (discarded after job) |
| Medium (community PRs) | Unreviewed code execution in audit | Require maintainer approval before audit workflow runs |
| High (if abuse detected) | Adversarial snippet exfiltration | Docker `--network=none` container for execution |

For the current scope — a curated, maintainer-reviewed repository — the
ephemeral runner model is the primary and sufficient containment strategy.

---

## Related Infrastructure

| Component | Role |
|---|---|
| [`tools/ast_sweep.py`](../../tools/ast_sweep.py) | Phase 1: Extract imports, validate PyPI, write Yellow badges |
| [`tools/osv_check.py`](../../tools/osv_check.py) | Phase 2: Poll OSV CVE database every 15 min |
| [`tools/write_badge.py`](../../tools/write_badge.py) | Manual badge state transitions |
| [`tools/common.py`](../../tools/common.py) | Shared `skill_path_to_badge_key` utility |
| [`.github/workflows/dependency-auditor.yml`](../../.github/workflows/dependency-auditor.yml) | Phase 3: CI runner for this auditor |
| [`meta/badge-states.md`](../../meta/badge-states.md) | Badge state machine reference |
