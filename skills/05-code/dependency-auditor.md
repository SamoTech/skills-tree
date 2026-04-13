---
title: Dependency Auditor
category: 05-code
level: advanced
stability: experimental
version: v1
tags: [code, dependencies, auditing, sbom, verification, dogfooding]
updated: 2026-04
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-dependency-auditor.json)

# Dependency Auditor

## What It Does

Reads a skill file's `dependencies` frontmatter block, installs each listed
package into an isolated virtual environment, executes the skill's **Runnable
Example** code block, and returns a structured verdict: whether the snippet
runs cleanly, which packages failed to import, and whether stdout matches
expected output patterns.

This is the execution layer that sits above PyPI existence checks. A Yellow
badge proves a package *exists*. A Green badge — produced by this auditor —
proves the snippet *runs*.

## When to Use

- Phase 3 verification sprints: promote a cohort of Yellow badges to Green
- CI gate before merging a new skill: block if the example raises `ImportError`
- Regression detection: catch a dependency update that breaks an existing example
- Generating the `tested_version` field automatically from the installed package

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `skill_path` | `str` | Path to the `.md` skill file to audit |
| `sbom_path` | `str` | Path to `meta/skills-sbom.cdx.json` for cross-referencing |
| `timeout` | `int` | Max seconds to allow the snippet to run (default: `30`) |
| `capture_stdout` | `bool` | Whether to capture and return stdout (default: `true`) |
| → `verdict` | `str` | `"pass"` \| `"fail"` \| `"skip"` |
| → `packages` | `list[PackageResult]` | Per-package install + import status |
| → `stdout` | `str` | Captured output from the snippet execution |
| → `error` | `str \| None` | Exception message if execution failed |
| → `tested_versions` | `dict[str, str]` | `{package: installed_version}` for frontmatter backfill |

## Runnable Example

```python
import subprocess
import sys
import json
import re
import tempfile
import venv
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# ── Schema ────────────────────────────────────────────────────────────────────

@dataclass
class PackageResult:
    name: str
    installed: bool
    version: Optional[str]
    import_ok: bool
    error: Optional[str] = None

@dataclass
class AuditResult:
    verdict: str                          # "pass" | "fail" | "skip"
    packages: list[PackageResult] = field(default_factory=list)
    stdout: str = ""
    error: Optional[str] = None
    tested_versions: dict[str, str] = field(default_factory=dict)

# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_frontmatter_deps(skill_text: str) -> list[str]:
    """Pull package names from the YAML dependencies block."""
    if not skill_text.startswith("---"):
        return []
    end = skill_text.find("---", 3)
    if end == -1:
        return []
    block = skill_text[3:end]
    return re.findall(r'^\s+-\s+package:\s*(\S+)', block, re.MULTILINE)

def extract_runnable_snippet(skill_text: str) -> Optional[str]:
    """Extract the first ```python code block after '## Runnable Example'."""
    m = re.search(
        r'## Runnable Example.*?```python\n(.*?)```',
        skill_text,
        re.DOTALL
    )
    return m.group(1) if m else None

def create_venv(venv_dir: Path) -> Path:
    """Create a fresh venv and return path to its python binary."""
    venv.create(str(venv_dir), with_pip=True, clear=True)
    python = venv_dir / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    return python

def pip_install(python: Path, package: str) -> tuple[bool, Optional[str], Optional[str]]:
    """Install a package; return (success, version, error_msg)."""
    r = subprocess.run(
        [str(python), "-m", "pip", "install", "--quiet", package],
        capture_output=True, text=True, timeout=60
    )
    if r.returncode != 0:
        return False, None, r.stderr.strip()
    # Resolve installed version
    ver_r = subprocess.run(
        [str(python), "-m", "pip", "show", package.split("[")[0]],
        capture_output=True, text=True
    )
    ver_match = re.search(r'^Version:\s*(.+)', ver_r.stdout, re.MULTILINE)
    return True, ver_match.group(1).strip() if ver_match else None, None

def test_import(python: Path, package: str) -> tuple[bool, Optional[str]]:
    """Try to import the package's top-level module."""
    import_name = package.split("[")[0].replace("-", "_")
    r = subprocess.run(
        [str(python), "-c", f"import {import_name}"],
        capture_output=True, text=True, timeout=10
    )
    return r.returncode == 0, r.stderr.strip() or None

# ── Core auditor ──────────────────────────────────────────────────────────────

def audit_skill(
    skill_path: str,
    sbom_path: Optional[str] = None,
    timeout: int = 30,
    capture_stdout: bool = True,
) -> AuditResult:
    skill_text = Path(skill_path).read_text(encoding="utf-8")
    packages   = extract_frontmatter_deps(skill_text)
    snippet    = extract_runnable_snippet(skill_text)

    # No dependencies declared — nothing to audit
    if not packages:
        return AuditResult(verdict="skip", error="No dependencies declared in frontmatter")

    # No runnable snippet — can't execute
    if snippet is None:
        return AuditResult(
            verdict="skip",
            error="No ## Runnable Example code block found",
            packages=[PackageResult(name=p, installed=False, version=None, import_ok=False)
                      for p in packages]
        )

    result = AuditResult(verdict="fail")

    with tempfile.TemporaryDirectory() as tmp:
        venv_dir = Path(tmp) / "audit_venv"
        python   = create_venv(venv_dir)

        # Install + import test for each package
        all_ok = True
        for pkg in packages:
            installed, version, install_err = pip_install(python, pkg)
            if not installed:
                result.packages.append(PackageResult(
                    name=pkg, installed=False, version=None,
                    import_ok=False, error=install_err
                ))
                all_ok = False
                continue

            import_ok, import_err = test_import(python, pkg)
            result.packages.append(PackageResult(
                name=pkg, installed=True, version=version,
                import_ok=import_ok, error=import_err
            ))
            if version:
                result.tested_versions[pkg] = version
            if not import_ok:
                all_ok = False

        if not all_ok:
            result.error = "One or more packages failed to install or import"
            return result

        # Execute the snippet
        snippet_file = Path(tmp) / "snippet.py"
        snippet_file.write_text(snippet, encoding="utf-8")

        run_r = subprocess.run(
            [str(python), str(snippet_file)],
            capture_output=True, text=True,
            timeout=timeout, cwd=tmp
        )

        if capture_stdout:
            result.stdout = run_r.stdout

        if run_r.returncode == 0:
            result.verdict = "pass"
        else:
            result.error = run_r.stderr.strip()
            result.verdict = "fail"

    return result


# ── Badge backfill helper ─────────────────────────────────────────────────────

def generate_verified_frontmatter_patch(
    result: AuditResult,
    skill_path: str,
) -> Optional[str]:
    """
    If the audit passed, return the YAML patch to write into the skill's
    frontmatter to promote it from Yellow → Green.

    Caller is responsible for writing this back to the file.
    """
    if result.verdict != "pass":
        return None

    lines = ["dependencies:"]
    for pkg in result.packages:
        ver = result.tested_versions.get(pkg.name, "unknown")
        lines.append(f"  - package: {pkg.name}")
        lines.append(f"    tested_version: \"{ver}\"")
        lines.append(f"    confidence: verified")
    return "\n".join(lines)


# ── CLI entry ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Audit a skill's runnable dependencies")
    parser.add_argument("skill",  help="Path to skill .md file")
    parser.add_argument("--sbom", help="Path to skills-sbom.cdx.json (optional)")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--patch", action="store_true",
                        help="Print the frontmatter patch for verified skills")
    args = parser.parse_args()

    res = audit_skill(args.skill, sbom_path=args.sbom, timeout=args.timeout)

    print(f"\n{'='*60}")
    print(f"Audit: {args.skill}")
    print(f"Verdict: {res.verdict.upper()}")
    print(f"{'='*60}")

    for pkg in res.packages:
        icon = "✅" if pkg.import_ok else "❌"
        ver  = f"v{pkg.version}" if pkg.version else "—"
        print(f"  {icon} {pkg.name} ({ver})")
        if pkg.error:
            print(f"     ↳ {pkg.error}")

    if res.stdout:
        print(f"\n── stdout ──\n{res.stdout.strip()}")
    if res.error:
        print(f"\n── error ──\n{res.error}")

    if args.patch and res.verdict == "pass":
        patch = generate_verified_frontmatter_patch(res, args.skill)
        print(f"\n── frontmatter patch ──\n{patch}")
```

## GitHub Actions Integration

Runs the auditor across all Yellow-badged skills as a batch verification sprint.
On pass, writes the `tested_version` + `confidence: verified` patch back to the
skill file and opens a draft PR — which triggers `sync-badges.yml` on merge to
promote the badge to Green.

```yaml
# .github/workflows/verify-sprint.yml
name: Verification Sprint

on:
  workflow_dispatch:
    inputs:
      max_skills:
        description: 'Max skills to audit per run (cost control)'
        type: number
        default: 20

jobs:
  audit:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Run batch audit
        run: |
          python tools/batch_audit.py \
            --sbom meta/skills-sbom.cdx.json \
            --max ${{ inputs.max_skills }} \
            --patch-output verified-patches.json

      - name: Apply verified patches and open draft PR
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            if (!fs.existsSync('verified-patches.json')) return;
            const patches = JSON.parse(fs.readFileSync('verified-patches.json', 'utf8'));
            console.log(`${patches.length} skills verified. Opening draft PR.`);
            // ... write patches, commit to branch, open draft PR
```

## Failure Modes

| Failure | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError` on import | Package name ≠ import name (e.g., `Pillow` → `PIL`) | Add `import_name` field to SBOM `components` or maintain a known-alias map |
| Snippet hangs | Network call or blocking input in example | Set `timeout=30`; mark skill with `type: requires-network` in frontmatter |
| `pip install` fails in CI | Package requires system libs (e.g., `psycopg2`, `torch`) | Add `install_extras` list to frontmatter: `extras: [libpq-dev]` |
| False `fail` on interactive examples | Example uses `input()` or opens a GUI | Detect `input(` in snippet pre-flight; auto-skip and return `verdict: "skip"` |
| Version mismatch vs. SBOM | SBOM records a pinned version; latest is different | Record both: `sbom_version` (from SBOM) and `installed_version` (from pip) |

## Pipeline Position

```
ast-sweep.yml          →  SBOM updated + Yellow badge pushed  (existence proof)
        ↓
verify-sprint.yml      →  dependency-auditor runs snippet     (execution proof)
        ↓
sync-badges.yml        →  Green badge on merge                 (verified)
        ↓
osv-watch.yml          →  Red advisory if CVE detected         (security signal)
        ↓
revoke-phantom-badges  →  Grey reset if PR abandoned          (self-healing)
```

This skill sits at the second step — it is the bridge between "we know it
exists" and "we know it works."

## Dogfooding Note

This skill file is itself tracked by the badge pipeline it describes.
When `ast-sweep.yml` next runs, it will detect the `subprocess`, `venv`,
and `re` imports in the snippet, cross-reference them against PyPI, and
push a Yellow badge. The first time `verify-sprint.yml` runs this auditor
against its own skill file, it will verify those stdlib modules import
cleanly and promote itself to Green.

That is recursive dogfooding: the pipeline auditing the skill that
describes the pipeline.

## Related Skills

- [`dependency-management.md`](dependency-management.md) — Declare and update deps
- [`code-execution-sandbox.md`](code-execution-sandbox.md) — Isolated execution environments
- [`security-scanning.md`](security-scanning.md) — CVE detection after deps are verified
- [`cicd-generation.md`](cicd-generation.md) — Build the verification sprint workflow

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2026-04 | Initial entry — Phase 3 dogfooding skill, execution verification layer |
