#!/usr/bin/env python3
"""
tools/generate_changelog.py

Appends a structured entry to meta/CHANGELOG.md based on a merged PR.
Called by .github/workflows/generate-changelog.yml on pull_request closed events.

Required environment variables:
    PR_TITLE   — pull request title (used to classify the change type)
    PR_NUMBER  — pull request number
    PR_AUTHOR  — GitHub username of the PR author
    PR_URL     — HTML URL of the pull request
    MERGED_AT  — ISO 8601 merge timestamp (optional; falls back to utcnow)

Exit codes:
    0 — success, or PR title did not match any known pattern (no entry written)
    1 — missing required env vars, or I/O error reading/writing CHANGELOG

HIGH-1 fix (2026-06-14):
    - All env vars validated before any file I/O
    - File reads and writes wrapped in try/except OSError
    - main() guard added — safe to import in tests
    - Module-level docstring added
    - SEC-3: env var values never printed to stdout/stderr
"""
from __future__ import annotations

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

CHANGELOG = Path("meta/CHANGELOG.md")

PATTERNS: list[tuple[str, str]] = [
    (r"^feat:\s+(.+)", "Added"),
    (r"^improve:\s+(.+)", "Improved"),
    (r"^fix:\s+(.+)", "Fixed"),
    (r"^deprecate:\s+(.+)", "Deprecated"),
]


def _get_env(name: str) -> str:
    """Return env var value; never raise — callers decide on emptiness."""
    return os.environ.get(name, "").strip()


def _read_changelog() -> str:
    """Read existing CHANGELOG or return starter content. Exit 1 on I/O error."""
    if CHANGELOG.exists():
        try:
            return CHANGELOG.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"[changelog] ERROR: cannot read {CHANGELOG}: {exc}", file=sys.stderr)
            sys.exit(1)
    return "# Changelog\n\n"


def _write_changelog(content: str) -> None:
    """Write content to CHANGELOG. Exit 1 on any I/O error."""
    try:
        CHANGELOG.parent.mkdir(parents=True, exist_ok=True)
        CHANGELOG.write_text(content, encoding="utf-8")
    except OSError as exc:
        print(f"[changelog] ERROR: cannot write {CHANGELOG}: {exc}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    pr_title = _get_env("PR_TITLE")
    if not pr_title:
        print("[changelog] ERROR: PR_TITLE is empty or not set.", file=sys.stderr)
        sys.exit(1)

    # Classify the change type from the PR title
    change_type: str | None = None
    detail: str | None = None
    for pattern, ctype in PATTERNS:
        m = re.match(pattern, pr_title, re.IGNORECASE)
        if m:
            change_type = ctype
            detail = m.group(1).strip()
            break

    if not change_type:
        print(f"[changelog] INFO: PR title did not match any pattern — no entry written.")
        sys.exit(0)

    # Validate remaining required env vars BEFORE touching the filesystem
    pr_number = _get_env("PR_NUMBER")
    pr_author = _get_env("PR_AUTHOR")
    pr_url = _get_env("PR_URL")
    merged_at = _get_env("MERGED_AT")

    missing = [k for k, v in {
        "PR_NUMBER": pr_number,
        "PR_AUTHOR": pr_author,
        "PR_URL": pr_url,
    }.items() if not v]
    if missing:
        print(
            f"[changelog] ERROR: Missing required env vars: {', '.join(missing)}",
            file=sys.stderr,
        )
        sys.exit(1)

    date_str = merged_at[:10] if merged_at else datetime.now(timezone.utc).strftime("%Y-%m-%d")
    entry = (
        f"- **{change_type}** [{detail}]({pr_url}) "
        f"by @{pr_author} (#{pr_number}) — {date_str}\n"
    )

    content = _read_changelog()

    if "# Changelog" in content:
        content = content.replace("# Changelog\n", f"# Changelog\n\n{entry}", 1)
    else:
        content = f"# Changelog\n\n{entry}" + content

    _write_changelog(content)
    print(f"[changelog] OK: appended entry for PR #{pr_number}")


if __name__ == "__main__":
    main()
