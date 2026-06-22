#!/usr/bin/env python3
"""
tools/quality_score.py — INITIATIVE-001 Phase E

Skill quality scorer for skills-tree.

Score dimensions (0-100 total):
  examples           20 pts  — code blocks or numbered examples present
  exercises          15 pts  — exercises/practice section present
  references         10 pts  — external links or references section
  implementation     20 pts  — implementation guidance (patterns, code, usage)
  related_skills     10 pts  — Related Skills section with 2+ links
  completeness       25 pts  — full description, I/O table or equivalent, changelog

Usage:
  python tools/quality_score.py                    # score all skills
  python tools/quality_score.py --category 02-reasoning
  python tools/quality_score.py --min-score 0      # show all (default: 0)
  python tools/quality_score.py --output meta/SKILL_QUALITY_INDEX.md
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
META_DIR = REPO_ROOT / "meta"


# ---------------------------------------------------------------------------
# Scoring heuristics
# ---------------------------------------------------------------------------
def score_file(md_path: Path) -> dict:
    """Score a single skill markdown file. Returns score dict."""
    try:
        text = md_path.read_text(encoding="utf-8")
    except Exception:
        return None

    word_count = len(text.split())
    scores = {}

    # examples (20 pts): code blocks or numbered example sections
    code_blocks = len(re.findall(r"```", text)) // 2
    has_example_section = bool(re.search(r"##\s+(example|usage)", text, re.IGNORECASE))
    scores["examples"] = min(20, code_blocks * 8 + (5 if has_example_section else 0))

    # exercises (15 pts): exercises / practice section
    has_exercises = bool(re.search(r"##\s+(exercise|practice|challenge|try it)", text, re.IGNORECASE))
    scores["exercises"] = 15 if has_exercises else 0

    # references (10 pts): external links or references section
    external_links = len(re.findall(r"https?://", text))
    has_refs_section = bool(re.search(r"##\s+(reference|further reading|resources)", text, re.IGNORECASE))
    scores["references"] = min(10, external_links * 2 + (3 if has_refs_section else 0))

    # implementation (20 pts): implementation guidance
    has_impl_section = bool(re.search(
        r"##\s+(implementation|pattern|prompt pattern|advanced|technique)",
        text, re.IGNORECASE
    ))
    has_io_table = bool(re.search(r"\|.*input.*\|.*type.*\|", text, re.IGNORECASE))
    scores["implementation"] = (
        (10 if has_impl_section else 0) +
        (7 if code_blocks >= 1 else 0) +
        (3 if has_io_table else 0)
    )

    # related_skills (10 pts)
    related_section = re.search(r"##\s+Related Skills?\s*\n(.*?)(?=\n##|\Z)", text, re.DOTALL | re.IGNORECASE)
    related_links = len(re.findall(r"\[[^\]]+\]\([^)]+\.md\)", related_section.group(1) if related_section else ""))
    scores["related_skills"] = min(10, related_links * 3)

    # completeness (25 pts)
    has_description = bool(re.search(r"##\s+description", text, re.IGNORECASE))
    has_frontmatter = text.startswith("---")
    has_changelog = bool(re.search(r"##\s+changelog", text, re.IGNORECASE))
    is_stub = word_count < 150
    scores["completeness"] = (
        (8 if has_description else 0) +
        (7 if has_frontmatter else 0) +
        (5 if has_changelog else 0) +
        (5 if not is_stub else 0)
    )

    total = sum(scores.values())
    return {
        "path": str(md_path.relative_to(REPO_ROOT)),
        "skill_id": f"{md_path.parent.name}/{md_path.stem}",
        "total": total,
        "word_count": word_count,
        "is_stub": is_stub,
        **scores,
    }


def grade(score: int) -> str:
    if score >= 80: return "A"
    if score >= 65: return "B"
    if score >= 45: return "C"
    if score >= 25: return "D"
    return "F"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Score skill quality across the repository.")
    parser.add_argument("--category", help="Score only this category.")
    parser.add_argument("--min-score", type=int, default=0, help="Only show skills with score >= N.")
    parser.add_argument("--output", default=str(META_DIR / "SKILL_QUALITY_INDEX.md"))
    args = parser.parse_args()

    results = []
    categories = []

    if args.category:
        cat_dir = SKILLS_DIR / args.category
        if not cat_dir.is_dir():
            print(f"ERROR: {cat_dir} not found", file=sys.stderr)
            sys.exit(1)
        categories = [cat_dir]
    else:
        categories = sorted(
            d for d in SKILLS_DIR.iterdir()
            if d.is_dir() and re.match(r"^[0-9]{2}-", d.name)
        )

    for cat_dir in categories:
        for md_file in sorted(cat_dir.glob("*.md")):
            if md_file.name == "README.md":
                continue
            result = score_file(md_file)
            if result and result["total"] >= args.min_score:
                results.append(result)

    results.sort(key=lambda r: r["total"], reverse=True)

    ts = datetime.now(timezone.utc).isoformat()
    avg = sum(r["total"] for r in results) / len(results) if results else 0
    stubs = sum(1 for r in results if r["is_stub"])

    lines = [
        "# Skill Quality Index",
        "",
        f"**Generated:** {ts}  ",
        f"**Total skills scored:** {len(results)}  ",
        f"**Average score:** {avg:.1f}/100  ",
        f"**Stub files (< 150 words):** {stubs}  ",
        "",
        "## Score Distribution",
        "",
        f"| Grade | Range | Count |",
        f"|---|---|---|",
    ]
    grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for r in results:
        grade_counts[grade(r["total"])] += 1
    grade_ranges = {"A": "80-100", "B": "65-79", "C": "45-64", "D": "25-44", "F": "0-24"}
    for g in ["A", "B", "C", "D", "F"]:
        lines.append(f"| {g} | {grade_ranges[g]} | {grade_counts[g]} |")

    lines += [
        "",
        "## Full Registry",
        "",
        "| Skill | Score | Grade | Examples | Exercises | References | Implementation | Related | Completeness | Words |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        stub_tag = " 🔴" if r["is_stub"] else ""
        lines.append(
            f"| `{r['skill_id']}`{stub_tag} "
            f"| {r['total']} | {grade(r['total'])} "
            f"| {r['examples']} | {r['exercises']} | {r['references']} "
            f"| {r['implementation']} | {r['related_skills']} | {r['completeness']} "
            f"| {r['word_count']} |"
        )

    output = "\n".join(lines)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"[quality_score] Scored {len(results)} skills. Average: {avg:.1f}. Written to {args.output}")


if __name__ == "__main__":
    main()
