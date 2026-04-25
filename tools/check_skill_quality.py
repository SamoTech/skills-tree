#!/usr/bin/env python3
"""Skill quality auditor.

Scans every file in `skills/**/*.md` and classifies it into one of:

  battle_tested  — has a non-stub description, a runnable code example,
                   typed I/O or failure-modes table, and >= 60 content lines.
  enriched       — non-stub description + runnable example.
  stub           — placeholder description ("Apply X in AI agent workflows.")
                   OR no code example.
  invalid        — missing required frontmatter (title, category).

Outputs a deterministic Markdown report at `meta/QUALITY-REPORT.md` and prints
a summary. Exits 0 always so it can run informationally; CI gates are
implemented separately by inspecting the produced report or by passing
`--enforce-new-stubs` (which fails if the diff vs origin/main introduces a new
stub).

Run from repo root:

    python3 tools/check_skill_quality.py [--enforce-new-stubs]

This script has no third-party dependencies; it shells out to `git` only when
`--enforce-new-stubs` is passed.
"""

from __future__ import annotations

import argparse
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
REPORT_PATH = REPO_ROOT / "meta" / "QUALITY-REPORT.md"

# Patterns whose presence in `description` makes a skill a stub regardless of
# everything else. The historical placeholder was "Apply X in AI agent
# workflows." — we also catch obvious near-clones so swapping a synonym
# doesn't silently bypass the gate (audit finding #10).
STUB_DESCRIPTION_PATTERNS = [
    re.compile(r'^\s*Apply\s.+?\s(?:in\s)?AI\s+agent\s+workflows?\.?\s*$', re.IGNORECASE),
    re.compile(r'^\s*Apply\s.+?\sin\s+agentic\s+(?:pipelines?|workflows?)\.?\s*$', re.IGNORECASE),
    re.compile(r'^\s*Use\s.+?\sin\s+AI\s+(?:agent|agentic)\s+(?:workflows?|pipelines?)\.?\s*$', re.IGNORECASE),
    re.compile(r'^\s*TODO\.?\s*$', re.IGNORECASE),
    re.compile(r'^\s*WIP\.?\s*$', re.IGNORECASE),
]
MIN_DESCRIPTION_CHARS = 30

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
CODE_BLOCK_RE = re.compile(r"```[a-zA-Z0-9_-]*\n.*?\n```", re.DOTALL)
TABLE_RE = re.compile(r"^\|.+\|.+\n\|[-: |]+\|", re.MULTILINE)


@dataclass
class SkillReport:
    path: Path
    category: str
    title: str
    classification: str
    reasons: list[str] = field(default_factory=list)
    line_count: int = 0


def parse_frontmatter(text: str) -> dict:
    """Parse the YAML frontmatter block at the top of a skill file.

    Uses ``yaml.safe_load`` when PyYAML is available so multi-line lists,
    nested mappings and quoted values with colons are handled correctly.
    Falls back to a tiny line parser (top-level scalar keys only) if PyYAML
    is not installed in the runtime — sufficient for the title/category
    checks this script makes today.
    """
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
            pass  # fall through to line parser
    fm: dict[str, str] = {}
    for line in block.splitlines():
        if not line or line.startswith((" ", "\t", "-")) or ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def _description_value(fm: dict, text: str) -> str:
    """Best-effort fetch the `description` field from the frontmatter."""
    desc = fm.get("description")
    if isinstance(desc, str):
        return desc.strip()
    # Frontmatter may not parse cleanly — grep the raw block for description.
    m = re.search(r'^description:\s*"?([^"\n]+?)"?\s*$', text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def stub_description_reason(description: str, title: str) -> str | None:
    """Return a human-readable reason if `description` is a stub, else None.

    Rules (audit finding #10):
    1. matches a known placeholder template (Apply X in AI agent workflows, …)
    2. shorter than MIN_DESCRIPTION_CHARS — too thin to be useful
    3. equals the skill title (with case/punctuation normalised)
    """
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
    if norm_title and norm_desc == norm_title:
        return "description is identical to the title"
    return None


def has_runnable_example(text: str) -> bool:
    """Heuristic: at least one fenced python/bash code block of >= 3 non-blank lines."""
    for block in CODE_BLOCK_RE.findall(text):
        lines = [ln for ln in block.splitlines()[1:-1] if ln.strip()]
        if len(lines) >= 3:
            return True
    return False


def has_table(text: str) -> bool:
    return bool(TABLE_RE.search(text))


def classify(path: Path) -> SkillReport:
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    category = path.parent.name
    title = (fm.get("title") if isinstance(fm.get("title"), str) else None) \
        or path.stem.replace("-", " ").title()
    line_count = text.count("\n")
    reasons: list[str] = []

    if "title" not in fm or "category" not in fm:
        reasons.append("missing required frontmatter (title/category)")
        return SkillReport(path, category, title, "invalid", reasons, line_count)

    description = _description_value(fm, text)
    stub_desc_reason = stub_description_reason(description, title)
    runnable = has_runnable_example(text)
    tabled = has_table(text)

    if stub_desc_reason:
        reasons.append(stub_desc_reason)
    if not runnable:
        reasons.append("no fenced runnable code example (>=3 non-blank lines)")
    if not tabled:
        reasons.append("no inputs/outputs/failure-modes table")

    if stub_desc_reason or not runnable:
        return SkillReport(path, category, title, "stub", reasons, line_count)
    if line_count >= 60 and tabled:
        return SkillReport(path, category, title, "battle_tested", reasons, line_count)
    return SkillReport(path, category, title, "enriched", reasons, line_count)


def iter_skill_files() -> Iterable[Path]:
    for p in sorted(SKILLS_DIR.rglob("*.md")):
        if p.name.lower() == "readme.md":
            continue
        yield p


def render_report(reports: list[SkillReport]) -> str:
    by_class: dict[str, list[SkillReport]] = defaultdict(list)
    for r in reports:
        by_class[r.classification].append(r)

    total = len(reports)
    n_stub = len(by_class["stub"])
    n_enriched = len(by_class["enriched"])
    n_bt = len(by_class["battle_tested"])
    n_invalid = len(by_class["invalid"])

    lines: list[str] = []
    lines.append("# Skill Quality Report")
    lines.append("")
    lines.append(
        "> Auto-generated by `tools/check_skill_quality.py`. Do not edit by hand. "
        "Open a PR that turns a stub into a runnable, typed, failure-mode-aware "
        "skill — that's the highest-impact contribution to this repo."
    )
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total skill files:** {total}")
    lines.append(f"- 🟢 **Battle-tested** (rich content + tables + >=60 lines): {n_bt}")
    lines.append(f"- 🟡 **Enriched** (real description + runnable code): {n_enriched}")
    lines.append(f"- ⚪ **Stub** (placeholder description or no runnable code): {n_stub}")
    lines.append(f"- ❌ **Invalid** (frontmatter problems): {n_invalid}")
    lines.append("")

    lines.append("## Per-category breakdown")
    lines.append("")
    lines.append("| Category | Total | 🟢 Battle-tested | 🟡 Enriched | ⚪ Stub | ❌ Invalid |")
    lines.append("|---|---|---|---|---|---|")
    cats: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in reports:
        cats[r.category]["total"] += 1
        cats[r.category][r.classification] += 1
    for cat in sorted(cats):
        c = cats[cat]
        lines.append(
            f"| `{cat}` | {c['total']} | {c['battle_tested']} | "
            f"{c['enriched']} | {c['stub']} | {c['invalid']} |"
        )
    lines.append("")

    lines.append("## 🟢 Battle-tested skills (start here as a user)")
    lines.append("")
    if not by_class["battle_tested"]:
        lines.append("_None yet — be the first to upgrade a skill to battle-tested._")
    else:
        for r in sorted(by_class["battle_tested"], key=lambda x: (x.category, x.path.name)):
            rel = r.path.relative_to(REPO_ROOT)
            lines.append(f"- [`{rel}`]({rel}) — {r.title}")
    lines.append("")

    lines.append("## 🟡 Enriched skills (almost there — add a table or +60 lines of context)")
    lines.append("")
    if not by_class["enriched"]:
        lines.append("_None — every skill is either a stub or fully battle-tested._")
    else:
        lines.append(
            "These skills have a real description and a runnable code example, "
            "but are missing one of: an inputs/outputs/failure-modes **table**, "
            "or **>=60 lines** of total content. The smallest possible PR "
            "upgrades them to battle-tested."
        )
        lines.append("")
        by_cat_e: dict[str, list[SkillReport]] = defaultdict(list)
        for r in by_class["enriched"]:
            by_cat_e[r.category].append(r)
        for cat in sorted(by_cat_e):
            lines.append(f"### `{cat}` ({len(by_cat_e[cat])})")
            lines.append("")
            for r in sorted(by_cat_e[cat], key=lambda x: x.path.name):
                rel = r.path.relative_to(REPO_ROOT)
                why = "; ".join(r.reasons) or "missing table or <60 lines"
                lines.append(f"- [`{rel.name}`]({rel}) — {why}")
            lines.append("")

    lines.append("## ⚪ Stubs (good first PRs)")
    lines.append("")
    lines.append(
        "Each entry below is a real, claimed skill that currently has no runnable "
        "example or a placeholder description. Pick one, follow "
        "[`meta/skill-template.md`](skill-template.md), and open a PR titled "
        "`improve: <skill-name> — v1→v2`."
    )
    lines.append("")
    by_cat: dict[str, list[SkillReport]] = defaultdict(list)
    for r in by_class["stub"]:
        by_cat[r.category].append(r)
    for cat in sorted(by_cat):
        lines.append(f"### `{cat}` ({len(by_cat[cat])})")
        lines.append("")
        for r in sorted(by_cat[cat], key=lambda x: x.path.name):
            rel = r.path.relative_to(REPO_ROOT)
            why = "; ".join(r.reasons) or "stub"
            lines.append(f"- [`{rel.name}`]({rel}) — {why}")
        lines.append("")

    if by_class["invalid"]:
        lines.append("## ❌ Invalid (frontmatter must be fixed)")
        lines.append("")
        for r in sorted(by_class["invalid"], key=lambda x: (x.category, x.path.name)):
            rel = r.path.relative_to(REPO_ROOT)
            why = "; ".join(r.reasons)
            lines.append(f"- [`{rel}`]({rel}) — {why}")
        lines.append("")

    lines.append("## Definitions")
    lines.append("")
    lines.append(
        "- **Battle-tested**: real description, fenced runnable code (>=3 lines), at "
        "least one Markdown table (I/O or failure modes), and >=60 lines of content."
    )
    lines.append("- **Enriched**: real description and a fenced runnable code block.")
    lines.append(
        "- **Stub**: description is the boilerplate `Apply X in AI agent workflows.` "
        "or no fenced runnable code block exists."
    )
    lines.append("- **Invalid**: frontmatter is missing required keys.")
    lines.append("")
    return "\n".join(lines) + "\n"


def changed_skill_files_against(base: str, *, diff_filter: str = "AM") -> list[Path]:
    """Return added or modified skill files since ``base``.

    ``diff_filter='A'`` -> only newly-added files (legacy behaviour).
    ``diff_filter='AM'`` -> added + modified files (default; lets the gate
    catch regressions — audit finding #4).
    """
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", f"--diff-filter={diff_filter}", f"{base}...HEAD"],
            cwd=REPO_ROOT,
            text=True,
        )
    except subprocess.CalledProcessError:
        return []
    paths: list[Path] = []
    for line in out.splitlines():
        if line.startswith("skills/") and line.endswith(".md") and not line.endswith("README.md"):
            p = REPO_ROOT / line
            if p.exists():
                paths.append(p)
    return paths


def _classify_at_revision(rev: str, rel_path: str) -> str | None:
    """Classify the skill at a git revision. Returns None if file didn't exist."""
    try:
        text = subprocess.check_output(
            ["git", "show", f"{rev}:{rel_path}"],
            cwd=REPO_ROOT, text=True, stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return None
    fm = parse_frontmatter(text)
    if "title" not in fm or "category" not in fm:
        return "invalid"
    description = _description_value(fm, text)
    title = fm.get("title") if isinstance(fm.get("title"), str) else ""
    stub_reason = stub_description_reason(description, title)
    runnable = has_runnable_example(text)
    tabled = has_table(text)
    if stub_reason or not runnable:
        return "stub"
    if text.count("\n") >= 60 and tabled:
        return "battle_tested"
    return "enriched"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--enforce-new-stubs",
        action="store_true",
        help="Fail if any skill file added in this branch is classified as stub.",
    )
    parser.add_argument(
        "--base",
        default="origin/main",
        help="Base ref to diff against when --enforce-new-stubs is set.",
    )
    parser.add_argument(
        "--no-write",
        action="store_true",
        help="Do not write QUALITY-REPORT.md; just print summary.",
    )
    args = parser.parse_args()

    reports = [classify(p) for p in iter_skill_files()]
    text = render_report(reports)

    if not args.no_write:
        REPORT_PATH.write_text(text, encoding="utf-8")
        print(f"Wrote {REPORT_PATH.relative_to(REPO_ROOT)}")

    summary = {r.classification: 0 for r in reports}
    for r in reports:
        summary[r.classification] = summary.get(r.classification, 0) + 1
    print("Summary:", summary)

    if args.enforce_new_stubs:
        # Audit finding #4: also check modified files, but only fail if the
        # modification *introduces* stub status (regressed from the base ref).
        changed = changed_skill_files_against(args.base, diff_filter="AM")
        offenders: list[tuple[SkillReport, str]] = []
        for p in changed:
            r = classify(p)
            if r.classification != "stub":
                continue
            rel = str(p.relative_to(REPO_ROOT))
            base_class = _classify_at_revision(args.base, rel)
            if base_class == "stub":
                continue  # already a stub on base; not this PR's regression
            kind = "new stub added" if base_class is None else \
                f"regression: was '{base_class}' on {args.base}, now 'stub'"
            offenders.append((r, kind))
        if offenders:
            print(
                f"\nERROR: {len(offenders)} skill file(s) failed the quality gate. "
                f"Either keep them out of stub status or restore them to their previous "
                f"classification before merging:",
                file=sys.stderr,
            )
            for r, kind in offenders:
                print(
                    f"  - {r.path.relative_to(REPO_ROOT)} [{kind}]: {'; '.join(r.reasons)}",
                    file=sys.stderr,
                )
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
