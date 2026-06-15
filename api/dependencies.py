#!/usr/bin/env python3
"""
FastAPI dependency-injection providers.
Instances are created once at app startup and reused across requests.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

# ---------------------------------------------------------------------------
# Path resolution — works whether run from repo root, api/, or tests/
# ---------------------------------------------------------------------------

def _repo_root() -> Path:
    """Walk up from this file until we find the repo root (has 'tools/' dir)."""
    here = Path(__file__).resolve().parent
    for candidate in [here, here.parent, here.parent.parent]:
        if (candidate / "tools" / "architect.py").exists():
            return candidate
    return here.parent  # fallback


ROOT = _repo_root()
TAXONOMY_PATH    = ROOT / "meta"       / "GOAL_TAXONOMY.md"
GRAPH_PATH       = ROOT / "data"       / "SKILLS_GRAPH.json"
BM_INDEX_PATH    = ROOT / "benchmarks" / "INDEX.json"


# ---------------------------------------------------------------------------
# Import architect classes (add repo root to sys.path once)
# ---------------------------------------------------------------------------

import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.architect import (
    GoalTaxonomyParser,
    SkillsGraph,
    RecommendationEngine,
    BlueprintGenerator,
)
from tools.ranking_calibrator import RankingCalibrator


# ---------------------------------------------------------------------------
# Singleton factories (cached for the process lifetime)
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_taxonomy() -> GoalTaxonomyParser:
    if not TAXONOMY_PATH.exists():
        raise FileNotFoundError(f"GOAL_TAXONOMY.md not found at {TAXONOMY_PATH}")
    return GoalTaxonomyParser(str(TAXONOMY_PATH))


@lru_cache(maxsize=1)
def get_graph() -> SkillsGraph:
    if not GRAPH_PATH.exists():
        raise FileNotFoundError(f"SKILLS_GRAPH.json not found at {GRAPH_PATH}")
    return SkillsGraph(str(GRAPH_PATH))


@lru_cache(maxsize=1)
def get_engine() -> RecommendationEngine:
    bm_path = str(BM_INDEX_PATH) if BM_INDEX_PATH.exists() else None
    return RecommendationEngine(get_graph(), get_taxonomy(), bm_path)


@lru_cache(maxsize=1)
def get_calibrator() -> RankingCalibrator:
    return RankingCalibrator()


@lru_cache(maxsize=1)
def get_blueprint_generator() -> BlueprintGenerator:
    return BlueprintGenerator()
