#!/usr/bin/env python3
"""Verify every intra-repo `[label](path.md)` link in skills/ resolves.

Walks every `skills/**/*.md` file, extracts each Markdown link of the form
`[..](relative/path.md)` (including ones with `#anchor` fragments), and
verifies the target file exists on disk. Skips http/https/mailto links.

Exits 0 if all links resolve, 1 otherwise. Designed to run in CI as a
guardrail against the broken-link issues called out in the project's own
CONTRIBUTING.md "Must Not Have: ❌ Broken internal links".

Run from repo root:

    python3 tools/check_broken_links.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+\.md)(?:#[^)]*)?\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "//")


def iter_markdown(root: Path):
    for p in sorted(root.rglob("*.md")):
        yield p


def find_broken_links(root: Path) -> list[tuple[Path, str, str, Path]]:
    broken: list[tuple[Path, str, str, Path]] = []
    for src in iter_markdown(root):
        text = src.read_text(encoding="utf-8")
        for m in LINK_RE.finditer(text):
            label, href = m.group(1), m.group(2)
            if href.startswith(EXTERNAL_PREFIXES):
                continue
            target = (src.parent / href).resolve()
            if not target.exists():
                broken.append((src, label, href, target))
    return broken


def main(argv: list[str]) -> int:
    root = SKILLS_DIR
    if len(argv) > 1:
        root = (REPO_ROOT / argv[1]).resolve()
    broken = find_broken_links(root)
    if not broken:
        print(f"OK: all .md links under {root.relative_to(REPO_ROOT)} resolve.")
        return 0

    print(f"ERROR: {len(broken)} broken intra-repo .md link(s):", file=sys.stderr)
    for src, label, href, target in broken:
        rel_src = src.relative_to(REPO_ROOT)
        try:
            rel_tgt = target.relative_to(REPO_ROOT)
            tgt_display = str(rel_tgt)
        except ValueError:
            tgt_display = str(target)
        print(
            f"  {rel_src}: [{label}]({href}) -> missing {tgt_display}",
            file=sys.stderr,
        )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
