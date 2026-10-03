#!/usr/bin/env python3
"""Detect low-information, placeholder, and marketing-style skill content."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

PLACEHOLDER_PATTERNS = (
    re.compile(r"\b(?:TODO|TBD|WIP|FIXME)\b", re.I),
    re.compile(r"lorem ipsum", re.I),
    re.compile(r"\bcoming soon\b", re.I),
    re.compile(r"\b(?:insert|add)\s+(?:your|the)\s+[^\n]{0,60}\s+here\b", re.I),
    re.compile(r"\[\s*(?:your|insert|add)\s+[^\]]{1,80}\]", re.I),
)

MARKETING_PATTERNS = (
    re.compile(r"\bgame[- ]changing\b", re.I),
    re.compile(r"\b(?:revolutionary|groundbreaking|cutting[- ]edge)\b", re.I),
    re.compile(r"\bstate[- ]of[- ]the[- ]art\b", re.I),
    re.compile(r"\bseamlessly\b", re.I),
    re.compile(r"\bunparalleled\b", re.I),
    re.compile(r"\b(?:powerful|robust|scalable)\s+and\s+(?:easy|simple|seamless)\b", re.I),
)

UNSUPPORTED_ABSOLUTES = (
    re.compile(r"\bguarantees?\b", re.I),
    re.compile(r"\b100\s*%\b", re.I),
    re.compile(r"\bzero\s+risk\b", re.I),
    re.compile(r"\bnever\s+(?:fails?|breaks?|errors?)\b", re.I),
)

GENERIC_SENTENCE = re.compile(
    r"^(?:this|the)\s+(?:skill|approach|method|solution|system|tool)\s+"
    r"(?:provides|enables|helps|allows|offers|delivers)\s+"
    r"(?:a|an|the)\s+(?:powerful|robust|simple|effective|comprehensive)\b",
    re.I,
)

CODE_MARK = chr(96)
CODE_RE = re.compile(re.escape(CODE_MARK) + r"{3}.*?" + re.escape(CODE_MARK) + r"{3}", re.S)
FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.S)


def iter_skill_files() -> list[Path]:
    return [p for p in sorted(SKILLS_DIR.rglob("*.md")) if p.name.lower() != "readme.md"]


def prose(text: str) -> str:
    return CODE_RE.sub("", FRONTMATTER_RE.sub("", text))


def findings_for(path: Path) -> list[tuple[str, int, str]]:
    body = prose(path.read_text(encoding="utf-8"))
    findings: list[tuple[str, int, str]] = []
    for pattern in PLACEHOLDER_PATTERNS:
        for match in pattern.finditer(body):
            line = body.count("\n", 0, match.start()) + 1
            findings.append(("ERROR", line, f"placeholder language: {match.group(0)!r}"))
    for pattern in MARKETING_PATTERNS:
        for match in pattern.finditer(body):
            line = body.count("\n", 0, match.start()) + 1
            findings.append(("ERROR", line, f"marketing filler: {match.group(0)!r}"))
    for pattern in UNSUPPORTED_ABSOLUTES:
        for match in pattern.finditer(body):
            line = body.count("\n", 0, match.start()) + 1
            findings.append(("WARN", line, f"absolute claim requires explicit evidence review: {match.group(0)!r}"))
    for lineno, line_text in enumerate(body.splitlines(), 1):
        if GENERIC_SENTENCE.match(line_text.strip()):
            findings.append(("WARN", lineno, "generic value statement; replace with a concrete capability, constraint, or procedure"))
    return findings


def changed_skill_files(base: str) -> list[Path]:
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", "--diff-filter=AM", f"{base}...HEAD"],
            cwd=REPO_ROOT,
            text=True,
        )
    except subprocess.CalledProcessError:
        return []
    return [REPO_ROOT / line for line in out.splitlines()
            if line.startswith("skills/") and line.endswith(".md") and (REPO_ROOT / line).exists()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--changed-only", action="store_true")
    parser.add_argument("--strict-warnings", action="store_true")
    args = parser.parse_args()

    paths = changed_skill_files(args.base) if args.changed_only else iter_skill_files()
    errors = warnings = 0
    for path in paths:
        for severity, line, message in findings_for(path):
            print(f"{severity}: {path.relative_to(REPO_ROOT)}:{line}: {message}")
            if severity == "ERROR":
                errors += 1
            else:
                warnings += 1

    print(f"Anti-slop summary: files={len(paths)} errors={errors} warnings={warnings}")
    return 1 if errors or (args.strict_warnings and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
