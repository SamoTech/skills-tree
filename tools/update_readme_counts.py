#!/usr/bin/env python3
"""Sync skill counts in README.md with the filesystem.

Runs idempotently. Updates five README.md anchors, each patched loudly
(a missing or duplicated anchor raises instead of silently leaving the
README drifted):

1. The hero stat strip "| <N> Public Skills | <M> Graph Edges | ...".
   The edge count comes from data/SKILLS_GRAPH.json.
2. The comparison-table row "✅ <N> public skills".
3. The What's-Inside tree line "→ <N> public skills (<N+1>
   quality-corpus files including one sandbox fixture)".
4. The category heading "## 🗂️ The <N> Skill Categories".
5. The per-category table. Each row's third column (Skills count) is
   updated to the live count.

Battle-tested and stub totals are still gathered from
tools/check_skill_quality.py and reported by main().

Run from repo root:

    python3 tools/update_readme_counts.py

Exits 0 with no diff if everything is already in sync.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
SKILLS_DIR = REPO_ROOT / "skills"
GRAPH = REPO_ROOT / "data" / "SKILLS_GRAPH.json"

# Reuse classifier to count battle-tested vs stubs.
sys.path.insert(0, str(REPO_ROOT / "tools"))
from check_skill_quality import classify, iter_skill_files  # noqa: E402


def _graph_edges() -> int:
    with GRAPH.open(encoding="utf-8") as fh:
        graph = json.load(fh)
    edges = graph.get("edges")
    if isinstance(edges, list):
        return len(edges)
    meta = graph.get("meta")
    if isinstance(meta, dict) and isinstance(meta.get("edge_count"), int):
        return meta["edge_count"]
    raise RuntimeError(
        "data/SKILLS_GRAPH.json has neither an 'edges' list nor a "
        "meta.edge_count integer; cannot determine the graph-edge "
        "count for README.md."
    )


def gather_counts() -> dict:
    by_cat: dict[str, int] = {}
    total = 0
    bt = 0
    stub = 0
    for p in SKILLS_DIR.iterdir():
        if not p.is_dir() or p.name == "00-sandbox":
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
        "graph_edges": _graph_edges(),
        "by_cat": by_cat,
        "battle_tested": bt,
        "stub": stub,
    }


def _patch_once(text: str, label: str, pattern: str, repl: str, flags: int = 0) -> str:
    new_text, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise RuntimeError(
            f"README.md {label} anchor ({pattern}) matched {n} times, "
            "expected exactly 1. Update README.md or "
            "tools/update_readme_counts.py so the anchor matches once."
        )
    return new_text


def patch_text(text: str, counts: dict) -> str:
    total = counts["total"]
    cats = counts["categories"]
    edges = counts["graph_edges"]

    # 1. Hero stat strip.
    text = _patch_once(
        text,
        "hero stat strip",
        r"\| \d+ Public Skills \| \d+ Graph Edges \|",
        f"| {total} Public Skills | {edges} Graph Edges |",
    )
    # 2. Comparison-table row.
    text = _patch_once(
        text,
        "comparison-table row",
        r"✅ \d+ public skills",
        f"✅ {total} public skills",
    )
    # 3. What's-Inside tree line.
    text = _patch_once(
        text,
        "What's-Inside skills line",
        r"→ \d+ public skills \(\d+ quality-corpus files including one sandbox fixture\)",
        f"→ {total} public skills ({total + 1} quality-corpus files including one sandbox fixture)",
    )
    # 4. Category heading.
    text = _patch_once(
        text,
        "category heading",
        r"^## 🗂️ The \d+ Skill Categories$",
        f"## 🗂️ The {cats} Skill Categories",
        flags=re.MULTILINE,
    )

    # 5. Per-category table, patched line-by-line. Each row of the form
    #   | 01 | <category> | <count> | <description> |
    # gets its third cell rewritten to match the live count for the
    # 01-* category directory. Failures here are loud (raises) so we
    # don't silently accept a drifted README. (Audit finding #9.)
    text = _patch_category_table(text, counts["by_cat"])
    return text


_ROW_RE = re.compile(
    r"^(?P<head>\|\s*(?P<prefix>\d{2})\s*\|[^|]+\|)\s*(?P<count>\d+)\s*(?P<tail>\|.*)$"
)


def _patch_category_table(text: str, by_cat: dict[str, int]) -> str:
    out_lines: list[str] = []
    seen_prefixes: set[str] = set()
    for line in text.splitlines(keepends=True):
        m = _ROW_RE.match(line.rstrip("\n"))
        if not m:
            out_lines.append(line)
            continue
        prefix = m.group("prefix")
        target_dir = next((c for c in by_cat if c.startswith(prefix + "-")), None)
        if target_dir is None:
            out_lines.append(line)
            continue
        seen_prefixes.add(prefix)
        n = by_cat[target_dir]
        new_line = f"{m.group('head')} {n} {m.group('tail')}\n"
        out_lines.append(new_line)
    # Sanity check: every skill-bearing category must have been seen in the table.
    expected = {c.split("-", 1)[0] for c in by_cat}
    missing = sorted(expected - seen_prefixes)
    if missing:
        raise RuntimeError(
            f"per-category table in README.md is missing rows for: "
            f"{missing}. Update the table or update_readme_counts.py."
        )
    return "".join(out_lines)


def main() -> int:
    counts = gather_counts()
    src = README.read_text(encoding="utf-8")
    out = patch_text(src, counts)
    if out == src:
        print("README.md already in sync.")
        return 0
    README.write_text(out, encoding="utf-8")
    print(
        f"Updated README.md → {counts['total']} skills, {counts['categories']} "
        f"categories, {counts['graph_edges']} graph edges, "
        f"{counts['battle_tested']} battle-tested, {counts['stub']} stubs."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
