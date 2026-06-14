"""Version Stats — Counts skill version tags and updates meta/VERSIONING.md.

Called by .github/workflows/version-stats.yml.
No environment variables required.
"""
import re
import glob
import sys
from pathlib import Path


def main() -> None:
    counts = {"v1": 0, "v2": 0, "v3": 0, "none": 0}

    for filepath in glob.glob("skills/**/*.md", recursive=True):
        try:
            with open(filepath) as fh:
                content = fh.read()
        except OSError as exc:
            print(f"[version-stats] WARNING: Cannot read {filepath}: {exc}")
            continue
        m = re.search(r'\*\*Version:\*\*\s*`?(v\d+)`?', content, re.IGNORECASE)
        if m:
            v = m.group(1).lower()
            if v in counts:
                counts[v] += 1
            else:
                counts["none"] += 1
        else:
            counts["none"] += 1

    total = sum(counts.values())

    def pct(n: int) -> str:
        return f"{(n / total * 100):.1f}%" if total else "0%"

    table = (
        "| Version | Count | % of Total |\n"
        "|---|---|---|\n"
        f"| v1 (Stub) | {counts['v1']} | {pct(counts['v1'])} |\n"
        f"| v2 (Expanded) | {counts['v2']} | {pct(counts['v2'])} |\n"
        f"| v3 (Battle-Tested) | {counts['v3']} | {pct(counts['v3'])} |\n"
        f"| No version tag | {counts['none']} | {pct(counts['none'])} |"
    )

    versioning_path = Path("meta/VERSIONING.md")
    if not versioning_path.exists():
        print(f"[version-stats] ERROR: {versioning_path} not found.")
        sys.exit(1)

    try:
        doc = versioning_path.read_text()
    except OSError as exc:
        print(f"[version-stats] ERROR: Cannot read {versioning_path}: {exc}")
        sys.exit(1)

    new_doc = re.sub(
        r'(## Current Version Distribution\n>.*?\n\n)\|.*?(?=\n---)',
        lambda m: m.group(1) + table,
        doc,
        flags=re.DOTALL,
    )

    if new_doc != doc:
        try:
            versioning_path.write_text(new_doc)
        except OSError as exc:
            print(f"[version-stats] ERROR: Cannot write {versioning_path}: {exc}")
            sys.exit(1)
        print(
            f"[version-stats] Updated: v1={counts['v1']} v2={counts['v2']} "
            f"v3={counts['v3']} none={counts['none']}"
        )
    else:
        print("[version-stats] No change needed.")


if __name__ == "__main__":
    main()
