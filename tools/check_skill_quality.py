#!/usr/bin/env python3
"""Deterministic skill-quality auditor driven by the authoritative JSON schema."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
SCHEMA_PATH = REPO_ROOT / "meta" / "skill-schema.json"
REPORT_PATH = REPO_ROOT / "meta" / "QUALITY-REPORT.md"
STUB_DESCRIPTION_PATTERNS = [
    re.compile(r'^\s*Apply\s.+?\s(?:in\s)?AI\s+agent\s+workflows?\.?\s*$', re.I),
    re.compile(r'^\s*Apply\s.+?\sin\s+agentic\s+(?:pipelines?|workflows?)\.?\s*$', re.I),
    re.compile(r'^\s*Use\s.+?\sin\s+AI\s+(?:agent|agentic)\s+(?:workflows?|pipelines?)\.?\s*$', re.I),
    re.compile(r'^\s*TODO\.?\s*$', re.I),
    re.compile(r'^\s*WIP\.?\s*$', re.I),
]
MIN_DESCRIPTION_CHARS = 30
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
CODE_BLOCK_RE = re.compile(r"```[a-zA-Z0-9_-]*\n.*?\n```", re.S)
TABLE_RE = re.compile(r"^\|.+\|.+\n\|[-: |]+\|", re.M)

@dataclass
class SkillReport:
    path: Path
    category: str
    title: str
    classification: str
    reasons: list[str] = field(default_factory=list)
    line_count: int = 0


def schema_enums() -> tuple[set[str], set[str], re.Pattern[str] | None]:
    """Load level/stability/version constraints from meta/skill-schema.json."""
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    props = schema["properties"]
    levels = set(props["level"].get("enum", []))
    stability = set(props["stability"].get("enum", []))
    version_pattern = props.get("version", {}).get("pattern")
    return levels, stability, re.compile(version_pattern) if version_pattern else None


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    block = m.group(1)
    if yaml is not None:
        try:
            data = yaml.safe_load(block)
            if isinstance(data, dict):
                return data
        except yaml.YAMLError:
            pass
    fm: dict[str, str] = {}
    for line in block.splitlines():
        if not line or line.startswith((" ", "\t", "-")) or ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def description_value(fm: dict, text: str) -> str:
    desc = fm.get("description")
    if isinstance(desc, str):
        return desc.strip()
    m = re.search(r'^description:\s*"?([^"\n]+?)"?\s*$', text, re.M)
    return m.group(1).strip() if m else ""

# Backward-compatible alias for corpus-audit tooling and external callers.
_description_value = description_value


def stub_description_reason(description: str, title: str) -> str | None:
    desc = (description or "").strip().rstrip(".")
    if not desc:
        return "description is empty"
    for pat in STUB_DESCRIPTION_PATTERNS:
        if pat.match(desc):
            return f'description matches placeholder pattern: {desc!r}'
    if len(desc) < MIN_DESCRIPTION_CHARS:
        return f"description too short ({len(desc)} < {MIN_DESCRIPTION_CHARS} chars)"
    norm_desc = re.sub(r"[^a-z0-9]+", "", desc.lower())
    norm_title = re.sub(r"[^a-z0-9]+", "", (title or "").lower())
    return "description is identical to the title" if norm_title and norm_desc == norm_title else None


def has_runnable_example(text: str) -> bool:
    for block in CODE_BLOCK_RE.findall(text):
        if len([ln for ln in block.splitlines()[1:-1] if ln.strip()]) >= 3:
            return True
    return False


def has_table(text: str) -> bool:
    return bool(TABLE_RE.search(text))


def classify(path: Path) -> SkillReport:
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    category = path.parent.name
    title = fm.get("title") if isinstance(fm.get("title"), str) else path.stem.replace("-", " ").title()
    lines = text.count("\n")
    reasons: list[str] = []
    if "title" not in fm or "category" not in fm:
        return SkillReport(path, category, title, "invalid", ["missing required frontmatter (title/category)"], lines)

    levels, stability, version_re = schema_enums()
    checks = (("level", levels), ("stability", stability))
    for key, allowed in checks:
        val = fm.get(key)
        if isinstance(val, str) and allowed and val not in allowed:
            reasons.append(f"frontmatter `{key}: {val}` not allowed by meta/skill-schema.json: {sorted(allowed)}")
    version = fm.get("version")
    if isinstance(version, str) and version_re and not version_re.fullmatch(version):
        reasons.append(f"frontmatter `version: {version}` does not match schema pattern {version_re.pattern!r}")
    if reasons:
        return SkillReport(path, category, title, "invalid", reasons, lines)

    stub_reason = stub_description_reason(description_value(fm, text), title)
    runnable = has_runnable_example(text)
    tabled = has_table(text)
    if stub_reason:
        reasons.append(stub_reason)
    if not runnable:
        reasons.append("no fenced runnable code example (>=3 non-blank lines)")
    if not tabled:
        reasons.append("no inputs/outputs/failure-modes table")
    if stub_reason or not runnable:
        return SkillReport(path, category, title, "stub", reasons, lines)
    return SkillReport(path, category, title, "battle_tested" if lines >= 60 and tabled else "enriched", reasons, lines)


def iter_skill_files() -> Iterable[Path]:
    return (p for p in sorted(SKILLS_DIR.rglob("*.md")) if p.name.lower() != "readme.md")


def render_report(reports: list[SkillReport]) -> str:
    by_class: dict[str, list[SkillReport]] = defaultdict(list)
    for r in reports:
        by_class[r.classification].append(r)
    lines = ["# Skill Quality Report", "", "> Auto-generated by `tools/check_skill_quality.py`. Do not edit by hand.", "", "## Summary", ""]
    counts = {k: len(by_class[k]) for k in ("battle_tested", "enriched", "stub", "invalid")}
    lines += [f"- **Total skill files:** {len(reports)}", f"- 🟢 **Battle-tested** (rich content + tables + >=60 lines): {counts['battle_tested']}", f"- 🟡 **Enriched** (real description + runnable code): {counts['enriched']}", f"- ⚪ **Stub** (placeholder description or no runnable code): {counts['stub']}", f"- ❌ **Invalid** (schema/frontmatter problems): {counts['invalid']}", "", "## Per-category breakdown", "", "| Category | Total | 🟢 Battle-tested | 🟡 Enriched | ⚪ Stub | ❌ Invalid |", "|---|---|---|---|---|---|"]
    cats: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in reports:
        cats[r.category]["total"] += 1
        cats[r.category][r.classification] += 1
    for cat in sorted(cats):
        c = cats[cat]
        lines.append(f"| `{cat}` | {c['total']} | {c['battle_tested']} | {c['enriched']} | {c['stub']} | {c['invalid']} |")
    lines += ["", "## 🟢 Battle-tested skills (start here as a user)", ""]
    lines += [f"- [`{r.path.relative_to(REPO_ROOT)}`]({r.path.relative_to(REPO_ROOT)}) — {r.title}" for r in sorted(by_class["battle_tested"], key=lambda x:(x.category,x.path.name))] or ["_None yet._"]
    lines += ["", "## 🟡 Enriched skills", ""]
    lines += [f"- [`{r.path.relative_to(REPO_ROOT)}`]({r.path.relative_to(REPO_ROOT)}) — {'; '.join(r.reasons) or 'missing table or <60 lines'}" for r in sorted(by_class["enriched"], key=lambda x:(x.category,x.path.name))] or ["_None._"]
    lines += ["", "## ⚪ Stubs", ""]
    lines += [f"- [`{r.path.relative_to(REPO_ROOT)}`]({r.path.relative_to(REPO_ROOT)}) — {'; '.join(r.reasons) or 'stub'}" for r in sorted(by_class["stub"], key=lambda x:(x.category,x.path.name))]
    if by_class["invalid"]:
        lines += ["", "## ❌ Invalid", ""]
        lines += [f"- [`{r.path.relative_to(REPO_ROOT)}`]({r.path.relative_to(REPO_ROOT)}) — {'; '.join(r.reasons)}" for r in sorted(by_class["invalid"], key=lambda x:(x.category,x.path.name))]
    lines += ["", "## Definitions", "", "- **Battle-tested**: real description, fenced runnable code (>=3 lines), a Markdown table, and >=60 lines.", "- **Enriched**: real description and a fenced runnable code block.", "- **Stub**: placeholder/empty/too-short description or no runnable code.", "- **Invalid**: missing required frontmatter or metadata violates the authoritative schema enums/patterns.", ""]
    return "\n".join(lines)


def changed_skill_files_against(base: str) -> list[Path]:
    try:
        out = subprocess.check_output(["git", "diff", "--name-only", "--diff-filter=AM", f"{base}...HEAD"], cwd=REPO_ROOT, text=True)
    except subprocess.CalledProcessError:
        return []
    return [REPO_ROOT / line for line in out.splitlines() if line.startswith("skills/") and line.endswith(".md") and not line.endswith("README.md") and (REPO_ROOT / line).exists()]


def classify_text(text: str) -> str:
    fm = parse_frontmatter(text)
    if "title" not in fm or "category" not in fm:
        return "invalid"
    levels, stability, version_re = schema_enums()
    if isinstance(fm.get("level"), str) and fm["level"] not in levels:
        return "invalid"
    if isinstance(fm.get("stability"), str) and fm["stability"] not in stability:
        return "invalid"
    if isinstance(fm.get("version"), str) and version_re and not version_re.fullmatch(fm["version"]):
        return "invalid"
    title = fm.get("title") if isinstance(fm.get("title"), str) else ""
    if stub_description_reason(description_value(fm, text), title) or not has_runnable_example(text):
        return "stub"
    return "battle_tested" if text.count("\n") >= 60 and has_table(text) else "enriched"


def classify_at_revision(rev: str, rel: str) -> str | None:
    try:
        text = subprocess.check_output(["git", "show", f"{rev}:{rel}"], cwd=REPO_ROOT, text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return None
    return classify_text(text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--enforce-new-stubs", action="store_true")
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    reports = [classify(p) for p in iter_skill_files()]
    if not args.no_write:
        REPORT_PATH.write_text(render_report(reports), encoding="utf-8")
        print(f"Wrote {REPORT_PATH.relative_to(REPO_ROOT)}")
    summary = {k: sum(r.classification == k for r in reports) for k in ("battle_tested", "enriched", "stub", "invalid")}
    print("Summary:", summary)
    if args.enforce_new_stubs:
        offenders = []
        for p in changed_skill_files_against(args.base):
            current = classify(p)
            if current not in {"stub", "invalid"}:
                continue
            rel = str(p.relative_to(REPO_ROOT))
            base = classify_at_revision(args.base, rel)
            if base == current:
                continue
            kind = f"new {current} added" if base is None else f"regression: was '{base}' on {args.base}, now '{current}'"
            offenders.append((p, kind, current))
        if offenders:
            print(f"ERROR: {len(offenders)} skill file(s) failed the quality gate:", file=sys.stderr)
            for p, kind, current in offenders:
                print(f"  - {p.relative_to(REPO_ROOT)} [{kind}]", file=sys.stderr)
            return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
