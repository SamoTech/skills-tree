#!/usr/bin/env python3
"""Sync skill counts in README.md with the filesystem.

Runs idempotently. Updates four things in README.md:

1. The `Skills` shields.io badge URL (`Skills-<N>%2B-`).
2. The hero blockquote text in the form
   `**<TOTAL> skills across <CATS> categories. ...`.
3. The battle-tested / stub split (`**<X> skills are battle-tested today.**`)
   and the matching `**<Y> are stubs**`. Values come from
   `tools/check_skill_quality.py`.
4. The per-category table under `## 🗂️ The 17 Skill Categories` (if present).
   Each row's third column (Skills count) is updated to the live count.

Run from repo root:

    python3 tools/update_readme_counts.py

Exits 0 with no diff if everything is already in sync.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
SKILLS_DIR = REPO_ROOT / "skills"

# Reuse classifier to count battle-tested vs stubs.
sys.path.insert(0, str(REPO_ROOT / "tools"))
from check_skill_quality import classify, iter_skill_files  # noqa: E402


def gather_counts() -> dict:
    by_cat: dict[str, int] = {}
    total = 0
    bt = 0
    stub = 0
    for p in SKILLS_DIR.iterdir():
        if not p.is_dir():
            continue
        n = sum(1 for f in p.glob("*.md") if f.name.lower() != "readme.md")
        if n:
            by_cat[p.name] = n
            total += n
    for p in iter_skill_files():
        c = classify(p).classification
        if c == "battle_tested":
            bt += 1
        elif c == "stub":
            stub += 1
    return {
        "total": total,
        "categories": len(by_cat),
        "by_cat": by_cat,
        "battle_tested": bt,
        "stub": stub,
    }


def patch_text(text: str, counts: dict) -> str:
    total = counts["total"]
    cats = counts["categories"]
    bt = counts["battle_tested"]
    stub = counts["stub"]

    text = re.sub(
        r"Skills-\d+%2B-",
        f"Skills-{total}%2B-",
        text,
    )
    text = re.sub(
        r"skills/\s+→ \d+ atomic skill files \(\d+ battle-tested, \d+ stubs awaiting upgrade\)",
        f"skills/          → {total} atomic skill files ({bt} battle-tested, {stub} stubs awaiting upgrade)",
        text,
    )
    text = re.sub(
        r"\*\*\d+ skills across \d+ categories\.",
        f"**{total} skills across {cats} categories.",
        text,
    )
    text = re.sub(
        r"\*\*\d+ skills are battle-tested today\.\*\*",
        f"**{bt} skills are battle-tested today.**",
        text,
    )
    text = re.sub(
        r"\*\*\d+ are stubs\*\*",
        f"**{stub} are stubs**",
        text,
    )

    # Patch the per-category table. We look for rows of the shape
    # `| 01 | ...Perception... | <num> | ... |`
    # and rewrite the count column based on directory prefix.
    def repl_row(m: re.Match) -> str:
        prefix = m.group("prefix")
        # Find directory whose name starts with this prefix.
        target_dir = None
        for cat in counts["by_cat"]:
            if cat.startswith(prefix + "-"):
                target_dir = cat
                break
        if target_dir is None:
            return m.group(0)
        n = counts["by_cat"][target_dir]
        return f"{m.group('head')} {n} {m.group('tail')}"

    text = re.sub(
        r"(?P<head>\|\s*(?P<prefix>\d{2})\s*\|[^|]+\|)\s*\d+\s*(?P<tail>\|[^\n]*)",
        repl_row,
        text,
    )
    return text


def main() -> int:
    counts = gather_counts()
    src = README.read_text(encoding="utf-8")
    out = patch_text(src, counts)
    if out == src:
        print("README.md already in sync.")
        return 0
    README.write_text(out, encoding="utf-8")
    print(
        f"Updated README.md → {counts['total']} skills, {counts['categories']} categories, "
        f"{counts['battle_tested']} battle-tested, {counts['stub']} stubs."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
