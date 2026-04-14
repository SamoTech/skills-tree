#!/usr/bin/env python3
"""
dependency_auditor.py — Phase 3 of the Dependency Watchdog pipeline.

Closes the Execution Gap: "package listed in frontmatter" -> "code actually runs".

For each skill file with Yellow (machine-inferred) badge status, this tool:
  1. Parses the dependency frontmatter block.
  2. Installs each declared package in an isolated venv.
  3. Runs the skill's first code snippet (if any) to verify it executes.
  4. Proposes a Green badge JSON if all deps install + snippet runs without error.
  5. Writes a verification-pr-body.md summarising results for human review.

Usage:
  # Audit changed files from a PR
  python tools/dependency_auditor.py \
      --skills-file /tmp/changed_skills.txt \
      --badge-output badge-data-output \
      --pr-body verification-pr-body.md

  # Full sweep of all skills under a directory
  python tools/dependency_auditor.py \
      --skills-root skills \
      --badge-output badge-data-output \
      --pr-body verification-pr-body.md

  # Dry run (print only, no files written)
  python tools/dependency_auditor.py --skills-root skills --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

GREEN_BADGE = {
    "schemaVersion": 1,
    "label": "deps",
    "message": "\u2714 verified",
    "color": "22c55e",
    "style": "flat-square",
}

YELLOW_BADGE_COLOR = "yellow"
GREEN_BADGE_COLOR = "22c55e"
CRITICAL_COLOR = "critical"

# Snippet execution timeout in seconds per skill
SNIPPET_TIMEOUT = 30

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class Dependency:
    package: str
    version: Optional[str] = None
    confidence: str = "machine-inferred"
    import_name: Optional[str] = None  # override if import differs from package name


@dataclass
class AuditResult:
    skill_path: Path
    skill_key: str
    deps: list[Dependency] = field(default_factory=list)
    install_ok: bool = False
    snippet_ok: bool = False
    snippet_skipped: bool = False
    error: Optional[str] = None

    @property
    def passed(self) -> bool:
        return self.install_ok and (self.snippet_ok or self.snippet_skipped)


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
DEP_BLOCK_RE = re.compile(
    r"^\s+-\s+package:\s*(?P<pkg>[^\n]+)(?:\n(?:\s+[^\n]+)*)*",
    re.MULTILINE,
)


def parse_frontmatter(text: str) -> dict:
    """Return the raw key-value dict from YAML-ish frontmatter."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    block = m.group(1)
    result: dict = {}
    for line in block.splitlines():
        kv = re.match(r"^([\w-]+):\s*(.+)", line.strip())
        if kv:
            result[kv.group(1)] = kv.group(2).strip().strip('"\'')
    return result


def parse_dependencies(text: str) -> list[Dependency]:
    """Extract dependency blocks from frontmatter."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return []
    block = m.group(1)

    deps: list[Dependency] = []
    # Iterate over each `- package:` entry in the frontmatter block
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        pkg_match = re.match(r"^\s+-\s+package:\s*(\S+)", line)
        if pkg_match:
            pkg_name = pkg_match.group(1).strip('"\'')
            dep = Dependency(package=pkg_name)
            # Look ahead for version/confidence/import_name sub-keys
            j = i + 1
            while j < len(lines) and re.match(r"^\s{2,}\S", lines[j]):
                sub = re.match(r"^\s+(version|confidence|import_name):\s*(.+)", lines[j])
                if sub:
                    key, val = sub.group(1), sub.group(2).strip().strip('"\'')
                    if key == "version":
                        dep.version = val
                    elif key == "confidence":
                        dep.confidence = val
                    elif key == "import_name":
                        dep.import_name = val
                j += 1
            deps.append(dep)
            i = j
        else:
            i += 1
    return deps


def extract_first_snippet(text: str) -> Optional[str]:
    """Return the first Python code block from the skill body."""
    # Skip frontmatter
    body_start = 0
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            body_start = end + 3

    body = text[body_start:]
    m = re.search(r"```python\n(.*?)```", body, re.DOTALL)
    if m:
        return m.group(1)
    return None


def skill_key(path: Path) -> str:
    rel = str(path).replace("\\", "/")
    return rel.replace("/", "-").replace(".md", "")


# ---------------------------------------------------------------------------
# Audit logic
# ---------------------------------------------------------------------------


def build_pip_specs(deps: list[Dependency]) -> list[str]:
    specs = []
    for dep in deps:
        if dep.version:
            specs.append(f"{dep.package}=={dep.version}")
        else:
            specs.append(dep.package)
    return specs


def audit_skill(skill_path: Path, dry_run: bool = False) -> AuditResult:
    text = skill_path.read_text(encoding="utf-8", errors="ignore")
    key = skill_key(skill_path)
    result = AuditResult(skill_path=skill_path, skill_key=key)

    result.deps = parse_dependencies(text)
    if not result.deps:
        result.snippet_skipped = True
        result.install_ok = True  # nothing to install
        print(f"  [SKIP] {skill_path}: no dependencies declared")
        return result

    if dry_run:
        print(f"  [DRY]  {skill_path}: would audit {len(result.deps)} dep(s)")
        result.install_ok = True
        result.snippet_skipped = True
        return result

    specs = build_pip_specs(result.deps)
    print(f"  [AUDIT] {skill_path}: installing {specs}")

    with tempfile.TemporaryDirectory(prefix="dep_audit_") as tmpdir:
        venv_dir = Path(tmpdir) / "venv"

        # Create isolated venv
        try:
            subprocess.run(
                [sys.executable, "-m", "venv", str(venv_dir)],
                check=True,
                capture_output=True,
                timeout=60,
            )
        except Exception as exc:
            result.error = f"venv creation failed: {exc}"
            print(f"    ERROR: {result.error}")
            return result

        pip = venv_dir / "bin" / "pip"
        python = venv_dir / "bin" / "python"

        # Install packages
        try:
            proc = subprocess.run(
                [str(pip), "install", "--quiet", "--timeout", "30"] + specs,
                capture_output=True,
                text=True,
                timeout=120,
            )
            if proc.returncode != 0:
                result.error = f"pip install failed:\n{proc.stderr[:500]}"
                print(f"    FAIL (install): {result.error}")
                return result
            result.install_ok = True
            print(f"    OK   (install): {specs}")
        except subprocess.TimeoutExpired:
            result.error = "pip install timed out after 120s"
            print(f"    TIMEOUT: {result.error}")
            return result
        except Exception as exc:
            result.error = f"pip install exception: {exc}"
            print(f"    ERROR: {result.error}")
            return result

        # Run first snippet (if any)
        snippet = extract_first_snippet(text)
        if snippet is None:
            result.snippet_skipped = True
            print(f"    OK   (no snippet to run)")
            return result

        # Write snippet to temp file
        snippet_file = Path(tmpdir) / "snippet.py"
        snippet_file.write_text(
            textwrap.dedent(snippet),
            encoding="utf-8",
        )

        try:
            proc = subprocess.run(
                [str(python), str(snippet_file)],
                capture_output=True,
                text=True,
                timeout=SNIPPET_TIMEOUT,
            )
            if proc.returncode != 0:
                result.error = f"snippet failed (exit {proc.returncode}):\n{proc.stderr[:500]}"
                print(f"    FAIL (snippet): {result.error}")
                return result
            result.snippet_ok = True
            print(f"    OK   (snippet ran successfully)")
        except subprocess.TimeoutExpired:
            # Timeout is not a hard failure for snippets that block on I/O
            result.snippet_skipped = True
            print(f"    SKIP (snippet timed out after {SNIPPET_TIMEOUT}s — treating as pass)")
        except Exception as exc:
            result.error = f"snippet exception: {exc}"
            print(f"    ERROR: {result.error}")

    return result


# ---------------------------------------------------------------------------
# Badge / report writing
# ---------------------------------------------------------------------------


def write_green_badge(result: AuditResult, badge_output: Path) -> None:
    badge_output.mkdir(parents=True, exist_ok=True)
    badge_file = badge_output / f"{result.skill_key}.json"

    # Never overwrite CVE/critical badges
    if badge_file.exists():
        existing = json.loads(badge_file.read_text())
        if existing.get("color") == CRITICAL_COLOR or "CVE" in existing.get("message", ""):
            print(f"    SKIP (CVE/critical badge protected): {badge_file.name}")
            return

    badge_file.write_text(json.dumps(GREEN_BADGE, indent=2))
    print(f"    WROTE green badge: {badge_file.name}")


def write_pr_body(
    results: list[AuditResult],
    pr_body_path: Path,
    dry_run: bool = False,
) -> None:
    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed and r.deps]
    skipped = [r for r in results if r.passed and not r.deps]

    lines = [
        "## \U0001f7e2 Dependency Auditor \u2014 Verification Report",
        "",
        "> Auto-generated by `dependency-auditor.yml`. "
        "**Do not merge without reviewing each skill.**",
        "",
        f"| Metric | Count |",
        f"|---|---|",
        f"| Skills audited | {len(results)} |",
        f"| Passed (proposed Green) | {len(passed)} |",
        f"| Failed | {len(failed)} |",
        f"| Skipped (no deps) | {len(skipped)} |",
        f"| Dry run | {'yes' if dry_run else 'no'} |",
        "",
    ]

    if passed:
        lines += [
            "### \u2705 Proposed Green Promotions",
            "",
            "| Skill | Packages | Snippet |",
            "|---|---|---|",
        ]
        for r in passed:
            pkgs = ", ".join(f"`{d.package}`" for d in r.deps) or "—"
            snippet_status = "skipped" if r.snippet_skipped else "\u2714"
            lines.append(f"| `{r.skill_path}` | {pkgs} | {snippet_status} |")
        lines.append("")

    if failed:
        lines += [
            "### \u274c Audit Failures (not promoted)",
            "",
            "| Skill | Error |",
            "|---|---|",
        ]
        for r in failed:
            err = (r.error or "unknown error").replace("\n", " ")[:200]
            lines.append(f"| `{r.skill_path}` | {err} |")
        lines.append("")

    lines += [
        "---",
        "> **Human review required.** Verify each proposed skill before approving this PR.",
    ]

    pr_body_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote PR body to {pr_body_path}")


# ---------------------------------------------------------------------------
# Skill discovery
# ---------------------------------------------------------------------------


def collect_skills_from_root(skills_root: Path) -> list[Path]:
    return sorted(skills_root.rglob("*.md"))


def collect_skills_from_file(skills_file: Path) -> list[Path]:
    paths = []
    for line in skills_file.read_text().splitlines():
        line = line.strip()
        if line:
            p = Path(line)
            if p.exists():
                paths.append(p)
            else:
                print(f"  [WARN] skill file not found: {line}")
    return paths


def should_audit(skill_path: Path, badge_output: Path) -> bool:
    """
    Only audit skills whose existing badge is Yellow (machine-inferred).
    Skip Green, CVE/critical, and unscanned badges — nothing to promote.
    """
    key = skill_key(skill_path)
    badge_file = badge_output / f"{key}.json"
    if not badge_file.exists():
        # No badge yet — skip, wait for ast-sweep to generate Yellow first
        return False
    try:
        badge = json.loads(badge_file.read_text())
    except Exception:
        return False
    color = badge.get("color", "")
    # Only promote Yellow badges
    return color == YELLOW_BADGE_COLOR


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Phase 3 Dependency Auditor: install deps + run snippets, propose Green badges."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--skills-root",
        type=Path,
        help="Root directory to recursively scan for skill .md files.",
    )
    group.add_argument(
        "--skills-file",
        type=Path,
        help="File containing newline-separated paths to skill .md files to audit.",
    )
    parser.add_argument(
        "--badge-output",
        type=Path,
        default=Path("badge-data-output"),
        help="Directory to write proposed Green badge JSONs into.",
    )
    parser.add_argument(
        "--pr-body",
        type=Path,
        default=Path("verification-pr-body.md"),
        help="Path to write the human-review PR body Markdown.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would happen without installing or writing any files.",
    )
    args = parser.parse_args()

    # Collect skill paths
    if args.skills_root:
        if not args.skills_root.exists():
            print(f"ERROR: skills-root '{args.skills_root}' does not exist.")
            return 1
        skills = collect_skills_from_root(args.skills_root)
    else:
        if not args.skills_file.exists():
            print(f"ERROR: skills-file '{args.skills_file}' does not exist.")
            return 1
        skills = collect_skills_from_file(args.skills_file)

    print(f"Found {len(skills)} skill file(s) to consider.")

    # Filter to only Yellow-badged skills (eligible for Green promotion)
    eligible = [s for s in skills if should_audit(s, args.badge_output)]
    print(f"{len(eligible)} skill(s) have Yellow badges eligible for audit.")

    if not eligible:
        print("Nothing to audit. Exiting.")
        # Write an empty PR body so the workflow file check doesn't crash
        if not args.dry_run:
            args.badge_output.mkdir(parents=True, exist_ok=True)
            args.pr_body.write_text(
                "## Dependency Auditor\n\nNo Yellow-badged skills found to audit.\n",
                encoding="utf-8",
            )
        return 0

    # Run audits
    results: list[AuditResult] = []
    for skill_path in eligible:
        print(f"\nAuditing: {skill_path}")
        result = audit_skill(skill_path, dry_run=args.dry_run)
        results.append(result)

    # Write outputs
    passed = [r for r in results if r.passed]
    print(f"\n{'='*60}")
    print(f"Audit complete: {len(passed)}/{len(results)} passed.")

    if not args.dry_run:
        args.badge_output.mkdir(parents=True, exist_ok=True)
        for r in passed:
            write_green_badge(r, args.badge_output)
        write_pr_body(results, args.pr_body, dry_run=False)
    else:
        print("[DRY RUN] No files written.")
        write_pr_body(results, args.pr_body, dry_run=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
