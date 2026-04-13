#!/usr/bin/env python3
"""
inject_badge_links.py

Batch-injects live shields.io badge links into every skill Markdown file.
Run AFTER ast_sweep.py has generated the badge JSONs on the badge-data branch.

Usage:
    python tools/inject_badge_links.py [--skills-root skills] [--dry-run]
"""

import argparse
import glob
from pathlib import Path

BADGE_BASE_URL = "https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/{key}.json"
BADGE_ALT = "Dependency Status"
DRY_RUN_TAG = "[DRY RUN]"


def make_key(file_path: Path) -> str:
    """Convert a file path like skills/02-reasoning/chain-of-thought.md
    into a badge key like skills-02-reasoning-chain-of-thought."""
    return str(file_path).replace("\\", "/").replace("/", "-").replace(".md", "")


def inject_badge(path: Path, dry_run: bool = False) -> bool:
    """Inject badge into a single Markdown file after the frontmatter.
    Returns True if the file was (or would be) modified."""
    content = path.read_text(encoding="utf-8")

    # Skip if badge already present
    if f"![{BADGE_ALT}]" in content:
        return False

    key = make_key(path)
    badge_url = BADGE_BASE_URL.format(key=key)
    badge_md = f"![{BADGE_ALT}]({badge_url})\n\n"

    # Insert after YAML frontmatter (between the two '---' delimiters)
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            new_content = f"---{parts[1]}---\n\n{badge_md}{parts[2].lstrip()}"
        else:
            new_content = badge_md + content
    else:
        new_content = badge_md + content

    if not dry_run:
        path.write_text(new_content, encoding="utf-8")

    return True


def main():
    parser = argparse.ArgumentParser(description="Inject live badge links into skill Markdown files.")
    parser.add_argument("--skills-root", default="skills", help="Root directory containing skill .md files (default: skills)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing any files")
    args = parser.parse_args()

    skills_root = Path(args.skills_root)
    if not skills_root.exists():
        print(f"ERROR: skills root '{skills_root}' does not exist.")
        return

    md_files = sorted(skills_root.rglob("*.md"))
    if not md_files:
        print(f"No Markdown files found under '{skills_root}'.")
        return

    print(f"{'[DRY RUN] ' if args.dry_run else ''}Scanning {len(md_files)} Markdown files in '{skills_root}'...\n")

    injected = 0
    skipped = 0

    for file_path in md_files:
        modified = inject_badge(file_path, dry_run=args.dry_run)
        if modified:
            prefix = DRY_RUN_TAG + " " if args.dry_run else ""
            print(f"  {prefix}Injected → {file_path}")
            injected += 1
        else:
            skipped += 1

    print(f"\n{'─' * 50}")
    print(f"{'[DRY RUN] ' if args.dry_run else ''}Done.")
    print(f"  Injected : {injected} file(s)")
    print(f"  Skipped  : {skipped} file(s) (badge already present or no .md files)")
    if args.dry_run:
        print("\n  No files were written. Remove --dry-run to apply changes.")


if __name__ == "__main__":
    main()
