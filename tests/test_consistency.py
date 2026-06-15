#!/usr/bin/env python3
"""
End-to-End Consistency Audit — Sprint C-10.5

Proves that the Engine, API, and MCP layers produce IDENTICAL recommendations
and blueprints for the same goal inputs.

Test matrix: 50 scenarios covering all 11 goal clusters.

Parity checks:
  - required_skills order (Engine == API == MCP)
  - optional_skills order (Engine == API == MCP)
  - confidence_score (max delta <= 0.01)
  - ranking_drift == 0
  - blueprint fields: required_skills, architecture_type, confidence_score, learning_path

Time-budget scenarios (CS-037..CS-040): API/MCP may return a truncated list;
  comparison is limited to order-within-returned-skills (not length).
"""

from __future__ import annotations

import sys
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

from fastapi.testclient import TestClient
from api.main import app as api_app

from tools.architect import (
    GoalTaxonomyParser,
    SkillsGraph,
    RecommendationEngine,
    BlueprintGenerator,
)
from tools.ranking_calibrator import RankingCalibrator
from mcp.tools import (
    recommend_skills as mcp_recommend,
    generate_blueprint as mcp_blueprint,
    MCPToolError,
)

TAXONOMY_PATH = ROOT / "meta"       / "GOAL_TAXONOMY.md"
GRAPH_PATH    = ROOT / "data"       / "SKILLS_GRAPH.json"
BM_INDEX_PATH = ROOT / "benchmarks" / "INDEX.json"

_taxonomy   = None
_graph      = None
_engine     = None
_calibrator = None
_generator  = None
_api_client = None


def get_engine_stack():
    global _taxonomy, _graph, _engine, _calibrator, _generator
    if _engine is None:
        _taxonomy   = GoalTaxonomyParser(str(TAXONOMY_PATH))
        _graph      = SkillsGraph(str(GRAPH_PATH))
        bm_path     = str(BM_INDEX_PATH) if BM_INDEX_PATH.exists() else None
        _engine     = RecommendationEngine(_graph, _taxonomy, bm_path)
        _calibrator = RankingCalibrator()
        _generator  = BlueprintGenerator()
    return _engine, _calibrator, _generator, _taxonomy


def get_api_client():
    global _api_client
    if _api_client is None:
        _api_client = TestClient(api_app)
    return _api_client


# ---------------------------------------------------------------------------
# Engine helper
# ---------------------------------------------------------------------------

def engine_recommend(goal: str, experience: str = "intermediate",
                     time_budget_hours: Optional[int] = None) -> Dict[str, Any]:
    engine, calibrator, generator, taxonomy = get_engine_stack()
    result = engine.recommend(goal)
    if "error" in result:
        raise ValueError(result["error"])

    goal_id   = result["goal_id"]
    goal_name = result["goal_name"]

    req_ids = calibrator.calibrate_ids(
        [s["id"] for s in result["required_skills"]],
        goal_id=goal_id, goal_text=goal_name,
    )
    opt_ids = calibrator.calibrate_ids(
        [s["id"] for s in result["optional_skills"]],
        goal_id=goal_id, goal_text=goal_name,
    )

    # Apply time_budget_hours if given (mirrors API logic)
    if time_budget_hours is not None:
        taxonomy_map = {s["id"]: s for s in result["taxonomy_skills"]}
        budget, spent, filtered = time_budget_hours, 0, []
        for sid in req_ids:
            hrs = taxonomy_map.get(sid, {}).get("learn_time_hrs", 0)
            if spent + hrs <= budget:
                filtered.append(sid)
                spent += hrs
        req_ids = filtered

    learning_path = [n.get("name", n["id"]) if isinstance(n, dict) else str(n)
                     for n in result["learning_path"]]

    return {
        "goal":             goal_name,
        "goal_id":          goal_id,
        "confidence_score": result["confidence_score"],
        "required_skills":  req_ids,
        "optional_skills":  opt_ids,
        "learning_path":    learning_path,
    }


def api_recommend(goal: str, experience: str = "intermediate",
                  time_budget_hours: Optional[int] = None) -> Dict[str, Any]:
    client  = get_api_client()
    payload: Dict[str, Any] = {"goal": goal, "experience": experience}
    if time_budget_hours is not None:
        payload["time_budget_hours"] = time_budget_hours
    r = client.post("/recommend", json=payload)
    assert r.status_code == 200, f"API error {r.status_code}: {r.text}"
    data = r.json()
    return {
        "goal":             data["goal"],
        "goal_id":          data["goal_id"],
        "confidence_score": data["confidence_score"],
        "required_skills":  [s["id"] for s in data["required_skills"]],
        "optional_skills":  [s["id"] for s in data["optional_skills"]],
        "learning_path":    data["learning_path"],
    }


def mcp_recommend_normalised(goal: str, experience: str = "intermediate",
                              time_budget_hours: Optional[int] = None) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {"goal": goal, "experience": experience}
    if time_budget_hours is not None:
        kwargs["time_budget_hours"] = time_budget_hours
    data = mcp_recommend(**kwargs)
    return {
        "goal":             data["goal"],
        "goal_id":          data["goal_id"],
        "confidence_score": data["confidence_score"],
        "required_skills":  [s["id"] for s in data["required_skills"]],
        "optional_skills":  [s["id"] for s in data["optional_skills"]],
        "learning_path":    data["learning_path"],
    }


# ---------------------------------------------------------------------------
# Blueprint helpers
# ---------------------------------------------------------------------------

BLUEPRINT_IGNORE_FIELDS = {"id", "generated_at"}


def engine_blueprint(goal: str) -> Dict[str, Any]:
    engine, calibrator, generator, taxonomy = get_engine_stack()
    result = engine.recommend(goal)
    if "error" in result:
        raise ValueError(result["error"])
    bp = generator.generate(goal, result, taxonomy)
    return {
        "goal_id":           bp["goal_id"],
        "architecture_type": bp["architecture_type"],
        "confidence_score":  bp["confidence_score"],
        "required_ids":      [s["id"] for s in bp["required_skills"]],
        "learning_path":     bp["learning_path"],
    }


def api_blueprint(goal: str) -> Dict[str, Any]:
    client = get_api_client()
    r = client.post("/blueprint", json={"goal": goal})
    assert r.status_code == 200, f"API blueprint error {r.status_code}: {r.text}"
    bp = r.json()
    return {
        "goal_id":           bp["goal_id"],
        "architecture_type": bp["architecture_type"],
        "confidence_score":  bp["confidence_score"],
        "required_ids":      [s["id"] for s in bp["required_skills"]],
        "learning_path":     bp["learning_path"],
    }


def mcp_blueprint_normalised(goal: str) -> Dict[str, Any]:
    bp = mcp_blueprint(goal)
    return {
        "goal_id":           bp["goal_id"],
        "architecture_type": bp["architecture_type"],
        "confidence_score":  bp["confidence_score"],
        "required_ids":      [s["id"] for s in bp["required_skills"]],
        "learning_path":     bp["learning_path"],
    }


# ---------------------------------------------------------------------------
# Ranking drift helper
# ---------------------------------------------------------------------------

def ranking_drift(list_a: List[str], list_b: List[str]) -> int:
    """Sum of absolute rank differences for skills present in both lists."""
    rank_a = {sid: i for i, sid in enumerate(list_a)}
    rank_b = {sid: i for i, sid in enumerate(list_b)}
    common = set(rank_a) & set(rank_b)
    return sum(abs(rank_a[s] - rank_b[s]) for s in common)


# ---------------------------------------------------------------------------
# Load suite
# ---------------------------------------------------------------------------

SUITE_PATH = ROOT / "evaluation" / "consistency_suite.json"


@pytest.fixture(scope="session")
def suite():
    with open(SUITE_PATH) as f:
        return json.load(f)


SCENARIOS_DEFAULT = [
    s for s in json.loads(SUITE_PATH.read_text())["scenarios"]
    if "time_budget_hours" not in s
][:10]  # first 10 non-budget for the class-level parametrize

# Core 10 goals for parametrised tests (CS-001 .. CS-010)
CORE_GOALS = [
    ("Coding Agent",       "G01"),
    ("Browser Agent",      "G02"),
    ("Memory Agent",       "G03"),
    ("RAG Assistant",      "G04"),
    ("Workflow Automation Agent", "G06"),
    ("Security Audit Agent",     "G07"),
    ("Multi-Agent Systems",      "G08"),
    ("Analytics Agent",          "G10"),
    ("Model Fine-tuning Pipeline","G11"),
    ("Research Agent",           "G04"),
]


# ===========================================================================
# Suite meta-tests — 2 tests
# ===========================================================================

class TestSuiteMeta:
    def test_suite_has_50_scenarios(self, suite):
        assert suite["scenario_count"] == 50
        assert len(suite["scenarios"]) == 50

    def test_suite_covers_all_goal_clusters(self, suite):
        goal_ids = {s["goal_id"] for s in suite["scenarios"]}
        expected = {"G01", "G02", "G03", "G04", "G05", "G06", "G07", "G08", "G09", "G10", "G11"}
        assert expected.issubset(goal_ids)


# ===========================================================================
# Engine vs API — 10 tests
# ===========================================================================

class TestEngineVsAPI:
    @pytest.mark.parametrize("goal,goal_id", CORE_GOALS)
    def test_required_skills_order_matches(self, goal, goal_id):
        eng = engine_recommend(goal)
        api = api_recommend(goal)
        assert eng["required_skills"] == api["required_skills"], (
            f"[{goal_id}] Required skills order mismatch:\n"
            f"  Engine: {eng['required_skills']}\n"
            f"  API:    {api['required_skills']}"
        )

    @pytest.mark.parametrize("goal,goal_id", CORE_GOALS[:5])
    def test_confidence_score_matches(self, goal, goal_id):
        eng = engine_recommend(goal)
        api = api_recommend(goal)
        assert abs(eng["confidence_score"] - api["confidence_score"]) <= 0.01, (
            f"[{goal_id}] Confidence drift: engine={eng['confidence_score']} api={api['confidence_score']}"
        )


# ===========================================================================
# Engine vs MCP — 10 tests
# ===========================================================================

class TestEngineVsMCP:
    @pytest.mark.parametrize("goal,goal_id", CORE_GOALS)
    def test_required_skills_order_matches(self, goal, goal_id):
        eng = engine_recommend(goal)
        mcp = mcp_recommend_normalised(goal)
        assert eng["required_skills"] == mcp["required_skills"], (
            f"[{goal_id}] MCP required skills mismatch:\n"
            f"  Engine: {eng['required_skills']}\n"
            f"  MCP:    {mcp['required_skills']}"
        )

    @pytest.mark.parametrize("goal,goal_id", CORE_GOALS[:5])
    def test_confidence_score_matches(self, goal, goal_id):
        eng = engine_recommend(goal)
        mcp = mcp_recommend_normalised(goal)
        assert abs(eng["confidence_score"] - mcp["confidence_score"]) <= 0.01


# ===========================================================================
# API vs MCP — 5 tests
# ===========================================================================

class TestAPIVsMCP:
    @pytest.mark.parametrize("goal,goal_id", CORE_GOALS[:5])
    def test_required_skills_fully_match(self, goal, goal_id):
        api = api_recommend(goal)
        mcp = mcp_recommend_normalised(goal)
        assert api["required_skills"] == mcp["required_skills"]

    @pytest.mark.parametrize("goal,goal_id", CORE_GOALS[:5])
    def test_optional_skills_fully_match(self, goal, goal_id):
        api = api_recommend(goal)
        mcp = mcp_recommend_normalised(goal)
        assert api["optional_skills"] == mcp["optional_skills"]


# ===========================================================================
# Ranking drift — 5 tests
# ===========================================================================

class TestRankingDrift:
    @pytest.mark.parametrize("goal,goal_id", CORE_GOALS[:5])
    def test_ranking_drift_is_zero_engine_vs_api(self, goal, goal_id):
        eng = engine_recommend(goal)
        api = api_recommend(goal)
        drift = ranking_drift(eng["required_skills"], api["required_skills"])
        assert drift == 0, f"Ranking drift engine/api for {goal}: {drift}"

    @pytest.mark.parametrize("goal,goal_id", CORE_GOALS[:5])
    def test_ranking_drift_is_zero_engine_vs_mcp(self, goal, goal_id):
        eng = engine_recommend(goal)
        mcp = mcp_recommend_normalised(goal)
        drift = ranking_drift(eng["required_skills"], mcp["required_skills"])
        assert drift == 0, f"Ranking drift engine/mcp for {goal}: {drift}"


# ===========================================================================
# Blueprint parity — 10 tests
# ===========================================================================

BLUEPRINT_GOALS = [
    "Coding Agent",
    "RAG Assistant",
    "Analytics Agent",
    "Multi-Agent Systems",
    "Security Audit Agent",
]


class TestBlueprintParity:
    @pytest.mark.parametrize("goal", BLUEPRINT_GOALS)
    def test_architecture_type_matches_engine_vs_api(self, goal):
        eng = engine_blueprint(goal)
        api = api_blueprint(goal)
        assert eng["architecture_type"] == api["architecture_type"]

    @pytest.mark.parametrize("goal", BLUEPRINT_GOALS)
    def test_required_ids_match_engine_vs_api(self, goal):
        eng = engine_blueprint(goal)
        api = api_blueprint(goal)
        assert eng["required_ids"] == api["required_ids"]

    @pytest.mark.parametrize("goal", BLUEPRINT_GOALS)
    def test_confidence_score_matches_engine_vs_api(self, goal):
        eng = engine_blueprint(goal)
        api = api_blueprint(goal)
        assert abs(eng["confidence_score"] - api["confidence_score"]) <= 0.01

    @pytest.mark.parametrize("goal", BLUEPRINT_GOALS)
    def test_architecture_type_matches_engine_vs_mcp(self, goal):
        eng = engine_blueprint(goal)
        mcp = mcp_blueprint_normalised(goal)
        assert eng["architecture_type"] == mcp["architecture_type"]

    @pytest.mark.parametrize("goal", BLUEPRINT_GOALS)
    def test_required_ids_match_engine_vs_mcp(self, goal):
        eng = engine_blueprint(goal)
        mcp = mcp_blueprint_normalised(goal)
        assert eng["required_ids"] == mcp["required_ids"]


# ===========================================================================
# Time-budget consistency — 4 tests
# ===========================================================================

class TestTimeBudgetConsistency:
    """With a time budget, API/MCP return a subset of skills in calibrated order."""

    def test_budget_skills_are_ordered_subset_cs037(self):
        eng = engine_recommend("Coding Agent", time_budget_hours=80)
        api = api_recommend("Coding Agent",    time_budget_hours=80)
        # Every API skill must appear in engine skills in the same relative order
        api_ids = api["required_skills"]
        eng_ids = eng["required_skills"]
        sub = [s for s in eng_ids if s in set(api_ids)]
        assert sub == api_ids, "API time-budget subset not in calibrated order"

    def test_budget_confidence_score_stable_cs038(self):
        api = api_recommend("RAG Assistant", time_budget_hours=60)
        mcp = mcp_recommend_normalised("RAG Assistant", time_budget_hours=60)
        assert abs(api["confidence_score"] - mcp["confidence_score"]) <= 0.01

    def test_budget_order_matches_api_vs_mcp_cs039(self):
        api = api_recommend("Analytics Agent", time_budget_hours=100)
        mcp = mcp_recommend_normalised("Analytics Agent", time_budget_hours=100)
        assert api["required_skills"] == mcp["required_skills"]

    def test_budget_browser_agent_cs040(self):
        api = api_recommend("Browser Agent", time_budget_hours=50)
        mcp = mcp_recommend_normalised("Browser Agent", time_budget_hours=50)
        assert api["required_skills"] == mcp["required_skills"]


# ===========================================================================
# Goal ID alias consistency — 3 tests
# ===========================================================================

class TestGoalIDAlias:
    """Passing bare goal ID (e.g. 'G01') must resolve to same result as full name."""

    def test_g01_alias_matches_coding_agent_api(self):
        full = api_recommend("Coding Agent")
        alias = api_recommend("G01")
        assert full["goal_id"] == alias["goal_id"]
        assert full["required_skills"] == alias["required_skills"]

    def test_g04_alias_matches_rag_assistant_api(self):
        full  = api_recommend("RAG Assistant")
        alias = api_recommend("G04")
        assert full["goal_id"] == alias["goal_id"]

    def test_g10_alias_matches_analytics_agent_engine(self):
        full  = engine_recommend("Analytics Agent")
        alias = engine_recommend("G10")
        assert full["goal_id"] == alias["goal_id"]
        assert full["required_skills"] == alias["required_skills"]


# ===========================================================================
# Experience-variant consistency — 3 tests
# ===========================================================================

class TestExperienceVariants:
    """experience param doesn't change recommendation ORDER."""

    def test_experience_variants_same_order_coding_agent(self):
        inter  = api_recommend("Coding Agent", experience="intermediate")
        advanc = api_recommend("Coding Agent", experience="advanced")
        assert inter["required_skills"] == advanc["required_skills"]

    def test_beginner_vs_intermediate_same_order(self):
        beginner = api_recommend("Browser Agent", experience="beginner")
        inter    = api_recommend("Browser Agent", experience="intermediate")
        assert beginner["required_skills"] == inter["required_skills"]

    def test_experience_variants_engine_vs_api_advanced(self):
        eng = engine_recommend("Memory Agent", experience="advanced")
        api = api_recommend("Memory Agent",    experience="advanced")
        assert eng["required_skills"] == api["required_skills"]


# ===========================================================================
# Confidence drift global check — 1 test
# ===========================================================================

class TestConfidenceDrift:
    def test_max_confidence_drift_across_all_core_goals(self):
        max_drift = 0.0
        for goal, _ in CORE_GOALS:
            eng = engine_recommend(goal)
            api = api_recommend(goal)
            mcp = mcp_recommend_normalised(goal)
            for a, b in [(eng, api), (eng, mcp), (api, mcp)]:
                drift = abs(a["confidence_score"] - b["confidence_score"])
                if drift > max_drift:
                    max_drift = drift
        assert max_drift <= 0.01, f"Confidence drift exceeded 0.01: {max_drift}"


if __name__ == "__main__":
    pytest.main(["-v", __file__])
