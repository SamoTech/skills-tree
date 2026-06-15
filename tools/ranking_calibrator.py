#!/usr/bin/env python3
"""
RankingCalibrator — Sprint C-08

Calibrates the Skills Tree architect recommendation ranking using
empirical signal from evaluation/results.json (Sprint C-07).

Three calibration layers (applied in order):
  1. Global penalties — demote chronically over-recommended skills
  2. Global boosts    — promote chronically under-recommended skills
  3. Goal-specific    — cluster-level adjustments (G01, G03, G07, G10, G11)
  4. Keyword layer    — goal-text keyword detection for fine-grained sub-goal tuning

Usage:
    from tools.ranking_calibrator import RankingCalibrator
    cal = RankingCalibrator()
    ranked_skills = cal.calibrate(ranked_skills, goal_id="G10", goal_text="Analytics Agent")
"""

from __future__ import annotations
from typing import Dict, List, Tuple, Optional


# ---------------------------------------------------------------------------
# Calibration tables — derived from C-07 evaluation/results.json
# ---------------------------------------------------------------------------

# Global: incorrect_count / 50  (scaled to score space *10 internally)
GLOBAL_PENALTIES: Dict[str, float] = {
    "skill:llm-orchestration":  -0.16,
    "skill:context-management": -0.08,
    "skill:api-integration":    -0.06,
    "skill:function-calling":   -0.06,
    "skill:web-scraping":       -0.10,
}

# Global: missing_count / 50  (scaled to score space *10 internally)
GLOBAL_BOOSTS: Dict[str, float] = {
    "skill:prompt-engineering":  +0.18,
    "skill:rag-retrieval":       +0.14,
    "skill:browser-automation":  +0.10,
    "skill:embedding-generation":+0.10,
    "skill:workflow-automation": +0.06,
}

# Goal-cluster level fine-tuning
GOAL_ADJUSTMENTS: Dict[str, Dict[str, float]] = {
    "G01": {
        "skill:llm-orchestration": -0.18,
    },
    "G03": {
        "skill:llm-orchestration":  -0.15,
        "skill:api-integration":    -0.12,
        "skill:function-calling":   -0.08,
        "skill:rag-retrieval":      +0.10,
        "skill:prompt-engineering": +0.10,
    },
    "G07": {
        "skill:browser-automation": +0.20,
        "skill:web-scraping":       +0.12,
        "skill:llm-orchestration":  -0.10,
        "skill:context-management": -0.08,
    },
    "G10": {
        "skill:rag-retrieval":        +0.25,
        "skill:prompt-engineering":   +0.20,
        "skill:context-management":   +0.10,
        "skill:embedding-generation": +0.10,
        "skill:data-extraction":      -0.03,
        "skill:web-scraping":         -0.08,
    },
    "G11": {
        "skill:web-scraping":        -0.20,
        "skill:browser-automation":  -0.10,
        "skill:prompt-engineering":  +0.15,
        "skill:code-generation":     +0.12,
        "skill:llm-orchestration":   +0.08,
    },
}

# Keyword layer — goal-text sub-goal detection
KEYWORD_ADJUSTMENTS: Dict[str, Dict[str, float]] = {
    "memory":          {"skill:context-management": +0.30, "skill:embedding-generation": +0.15,
                        "skill:web-scraping": -0.30, "skill:data-extraction": -0.20},
    "assistant":       {"skill:context-management": +0.20, "skill:rag-retrieval": +0.15},
    "analytics":       {"skill:prompt-engineering": +0.25, "skill:context-management": +0.20,
                        "skill:rag-retrieval": +0.20, "skill:web-scraping": -0.20},
    "report":          {"skill:prompt-engineering": +0.25, "skill:context-management": +0.20,
                        "skill:rag-retrieval": +0.20, "skill:web-scraping": -0.20},
    "financial":       {"skill:prompt-engineering": +0.20, "skill:rag-retrieval": +0.25,
                        "skill:context-management": +0.20, "skill:web-scraping": -0.25},
    "etl":             {"skill:data-extraction": +0.10, "skill:workflow-automation": +0.15,
                        "skill:rag-retrieval": -0.10, "skill:embedding-generation": -0.05},
    "security":        {"skill:browser-automation": +0.35, "skill:web-scraping": +0.20,
                        "skill:api-integration": -0.30, "skill:context-management": -0.20,
                        "skill:llm-orchestration": -0.25},
    "audit":           {"skill:browser-automation": +0.35, "skill:web-scraping": +0.20,
                        "skill:api-integration": -0.30, "skill:context-management": -0.20},
    "social":          {"skill:prompt-engineering": +0.20, "skill:api-integration": +0.20,
                        "skill:browser-automation": -0.05, "skill:context-management": -0.15},
    "collection":      {"skill:api-integration": +0.20, "skill:browser-automation": -0.10},
    "aggregator":      {"skill:embedding-generation": +0.25, "skill:context-management": +0.20,
                        "skill:browser-automation": -0.15},
    "content creation":{"skill:rag-retrieval": +0.30, "skill:embedding-generation": +0.20,
                        "skill:function-calling": -0.20, "skill:error-recovery": -0.15},
    "sales":           {"skill:rag-retrieval": +0.30, "skill:context-management": +0.20,
                        "skill:code-generation": -0.25, "skill:error-recovery": -0.10},
    "slack":           {"skill:function-calling": +0.10, "skill:workflow-automation": -0.25,
                        "skill:llm-orchestration": -0.20},
    "fine-tun":        {"skill:data-extraction": +0.15, "skill:embedding-generation": +0.15,
                        "skill:api-integration": -0.20, "skill:context-management": -0.10},
    "pipeline":        {"skill:data-extraction": +0.10, "skill:workflow-automation": +0.15},
}


class RankingCalibrator:
    """
    Applies C-08 calibration weights to a pre-scored skill list.

    Accepts either:
      (a) a list of skill-id strings (assumes equal positional scores)
      (b) a list of (skill_id, score) tuples

    Returns a re-ranked list of (skill_id, calibrated_score) tuples,
    sorted descending by calibrated score.
    """

    def __init__(
        self,
        global_penalties: Optional[Dict[str, float]] = None,
        global_boosts:    Optional[Dict[str, float]] = None,
        goal_adjustments: Optional[Dict[str, Dict[str, float]]] = None,
        keyword_adjustments: Optional[Dict[str, Dict[str, float]]] = None,
    ):
        self._penalties = global_penalties  or GLOBAL_PENALTIES
        self._boosts    = global_boosts     or GLOBAL_BOOSTS
        self._goal_adj  = goal_adjustments  or GOAL_ADJUSTMENTS
        self._kw_adj    = keyword_adjustments or KEYWORD_ADJUSTMENTS

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def calibrate(
        self,
        skills: List,
        goal_id: str = "",
        goal_text: str = "",
    ) -> List[Tuple[str, float]]:
        """
        Re-rank skills using calibration weights.

        Parameters
        ----------
        skills    : list of skill-id strings or (skill_id, base_score) tuples
        goal_id   : canonical goal cluster ID (e.g. "G10")
        goal_text : free-text goal name used for keyword matching

        Returns
        -------
        list of (skill_id, calibrated_score) sorted descending
        """
        scored = self._normalise_input(skills)
        calibrated = self._apply_weights(scored, goal_id, goal_text)
        return sorted(calibrated.items(), key=lambda x: -x[1])

    def calibrate_ids(self, skills: List, goal_id: str = "", goal_text: str = "") -> List[str]:
        """Like calibrate() but returns only skill IDs (no scores)."""
        return [sid for sid, _ in self.calibrate(skills, goal_id, goal_text)]

    def describe_adjustments(self, goal_id: str = "", goal_text: str = "") -> Dict:
        """Return the full set of adjustments that would be applied for diagnostic purposes."""
        adjustments: Dict[str, float] = {}
        for sid, delta in self._penalties.items():
            adjustments[sid] = adjustments.get(sid, 0.0) + delta * 10
        for sid, delta in self._boosts.items():
            adjustments[sid] = adjustments.get(sid, 0.0) + delta * 10
        for sid, delta in self._goal_adj.get(goal_id, {}).items():
            adjustments[sid] = adjustments.get(sid, 0.0) + delta * 10
        if goal_text:
            for kw, kw_boosts in self._kw_adj.items():
                if kw in goal_text.lower():
                    for sid, delta in kw_boosts.items():
                        adjustments[sid] = adjustments.get(sid, 0.0) + delta * 10
        return adjustments

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _normalise_input(skills: List) -> Dict[str, float]:
        """Accept strings or (id, score) tuples; return {id: score} dict."""
        scored: Dict[str, float] = {}
        for i, item in enumerate(skills):
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                sid, base = item[0], float(item[1])
            else:
                sid, base = str(item), 10.0 - i
            scored[sid] = base
        return scored

    def _apply_weights(
        self,
        scores: Dict[str, float],
        goal_id: str,
        goal_text: str,
    ) -> Dict[str, float]:
        out = dict(scores)
        for sid, delta in self._penalties.items():
            if sid in out: out[sid] += delta * 10
        for sid, delta in self._boosts.items():
            if sid in out: out[sid] += delta * 10
        for sid, delta in self._goal_adj.get(goal_id, {}).items():
            if sid in out: out[sid] += delta * 10
        if goal_text:
            goal_lower = goal_text.lower()
            for kw, kw_boosts in self._kw_adj.items():
                if kw in goal_lower:
                    for sid, delta in kw_boosts.items():
                        if sid in out: out[sid] += delta * 10
        return out
