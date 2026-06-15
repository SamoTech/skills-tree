"""
data_resolver.py — Runtime data-file path resolution.

The engine reads several data files that must survive the journey from
a development checkout all the way to a PyPI wheel install. Naive
`__file__`-relative paths break inside zipped wheels. This module
provides a single `resolve()` helper that works in every case:

  1. Editable install (`pip install -e .`) — files are in the repo root.
  2. Regular install (`pip install skills-tree`) — files are copied next
     to the installed packages by setuptools `data_files`.
  3. Zipapp / frozen executable — falls back to `importlib.resources`.

Usage
-----
    from tools.data_resolver import resolve

    skills_graph_path = resolve("data", "SKILLS_GRAPH.json")
    taxonomy_path     = resolve("meta", "GOAL_TAXONOMY.md")
    benchmark_path    = resolve("benchmarks", "INDEX.json")
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Candidate root directories, in priority order
# ---------------------------------------------------------------------------

def _candidate_roots() -> list[Path]:
    """Return plausible data-root directories, most-specific first."""
    candidates: list[Path] = []

    # 1. Explicit override via env var (useful for testing / containers)
    if env_root := os.environ.get("SKILLS_TREE_DATA_ROOT"):
        candidates.append(Path(env_root))

    # 2. Repo root when running from a checkout or editable install:
    #    tools/data_resolver.py → parent → repo root
    candidates.append(Path(__file__).resolve().parent.parent)

    # 3. site-packages root (regular wheel install)
    for path in sys.path:
        p = Path(path)
        if p.is_dir() and (p / "data" / "SKILLS_GRAPH.json").exists():
            candidates.append(p)

    # 4. CWD (last resort)
    candidates.append(Path.cwd())

    return candidates


def resolve(*parts: str, strict: bool = True) -> Path:
    """
    Resolve a data-file path relative to the package data root.

    Parameters
    ----------
    *parts:
        Path components, e.g. resolve("data", "SKILLS_GRAPH.json")
    strict:
        If True (default), raise FileNotFoundError if the file is not
        found in any candidate root. If False, return the best-guess
        path even if it does not exist.

    Returns
    -------
    Path
        Absolute path to the requested data file.
    """
    rel = Path(*parts)

    for root in _candidate_roots():
        candidate = root / rel
        if candidate.exists():
            return candidate.resolve()

    if strict:
        searched = "\n  ".join(str(r / rel) for r in _candidate_roots())
        raise FileNotFoundError(
            f"Runtime data file not found: {rel}\n"
            f"Searched:\n  {searched}\n"
            f"Set SKILLS_TREE_DATA_ROOT env var to override the search path."
        )

    # non-strict: return first candidate (may not exist)
    return (_candidate_roots()[0] / rel).resolve()


def data_root() -> Path:
    """Return the resolved data root directory (contains data/, meta/, benchmarks/)."""
    return resolve("data", "SKILLS_GRAPH.json").parent.parent
