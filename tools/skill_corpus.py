"""Shared canonical/public skill corpus boundary helpers.

The quality corpus may contain test fixtures. Public projections must consume
only the production/public canonical corpus.
"""
from __future__ import annotations

from pathlib import Path

PUBLIC_EXCLUDED_CATEGORIES = frozenset({"00-sandbox"})


def is_public_category(category: str) -> bool:
    return category not in PUBLIC_EXCLUDED_CATEGORIES


def is_public_skill_path(path: Path, skills_root: Path) -> bool:
    try:
        relative = path.resolve().relative_to(skills_root.resolve())
    except ValueError:
        return False
    return bool(relative.parts) and is_public_category(relative.parts[0])


def iter_public_skill_files(skills_root: Path) -> list[Path]:
    return sorted(
        path
        for path in skills_root.rglob("*.md")
        if path.name.lower() != "readme.md"
        and is_public_skill_path(path, skills_root)
    )
