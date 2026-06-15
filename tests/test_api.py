#!/usr/bin/env python3
"""
API tests for Architect API v1 — Sprint C-09.
25 tests covering all 5 endpoints:
  - GET /health          (3 tests)
  - GET /goals           (4 tests)
  - GET /skills          (4 tests)
  - POST /recommend      (8 tests)
  - POST /blueprint      (6 tests)

Run:
    pytest tests/test_api.py -v
"""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


# ===========================================================================
# GET /health — 3 tests
# ===========================================================================

class TestHealth:
    def test_health_status_200(self):
        r = client.get("/health")
        assert r.status_code == 200

    def test_health_status_ok(self):
        r = client.get("/health")
        data = r.json()
        assert data["status"] == "ok"

    def test_health_version(self):
        r = client.get("/health")
        data = r.json()
        assert data["version"] == "1.0"


# ===========================================================================
# GET /goals — 4 tests
# ===========================================================================

class TestGoals:
    def test_goals_status_200(self):
        r = client.get("/goals")
        assert r.status_code == 200

    def test_goals_has_total_field(self):
        r = client.get("/goals")
        data = r.json()
        assert "total" in data
        assert isinstance(data["total"], int)
        assert data["total"] > 0

    def test_goals_has_goals_list(self):
        r = client.get("/goals")
        data = r.json()
        assert "goals" in data
        assert isinstance(data["goals"], list)
        assert len(data["goals"]) == data["total"]

    def test_goals_each_has_id_and_name(self):
        r = client.get("/goals")
        data = r.json()
        for goal in data["goals"]:
            assert "id" in goal, f"Missing 'id' in goal: {goal}"
            assert "name" in goal, f"Missing 'name' in goal: {goal}"
            assert goal["id"].startswith("G"), f"Unexpected goal id format: {goal['id']}"


# ===========================================================================
# GET /skills — 4 tests
# ===========================================================================

class TestSkills:
    def test_skills_status_200(self):
        r = client.get("/skills")
        assert r.status_code == 200

    def test_skills_has_total_and_list(self):
        r = client.get("/skills")
        data = r.json()
        assert "total" in data
        assert "skills" in data
        assert data["total"] > 0
        assert len(data["skills"]) == data["total"]

    def test_skills_each_has_id_and_name(self):
        r = client.get("/skills")
        data = r.json()
        for skill in data["skills"]:
            assert "id" in skill
            assert "name" in skill

    def test_skills_sorted_by_id(self):
        r = client.get("/skills")
        data = r.json()
        ids = [s["id"] for s in data["skills"]]
        assert ids == sorted(ids), "Skills list should be sorted by id"


# ===========================================================================
# POST /recommend — 8 tests
# ===========================================================================

class TestRecommend:
    def test_recommend_valid_goal(self):
        r = client.post("/recommend", json={"goal": "Coding Agent"})
        assert r.status_code == 200

    def test_recommend_response_shape(self):
        r = client.post("/recommend", json={"goal": "Coding Agent"})
        data = r.json()
        assert "goal" in data
        assert "goal_id" in data
        assert "confidence_score" in data
        assert "required_skills" in data
        assert "optional_skills" in data
        assert "learning_path" in data
        assert "calibration_applied" in data

    def test_recommend_calibration_applied(self):
        r = client.post("/recommend", json={"goal": "Coding Agent"})
        data = r.json()
        assert data["calibration_applied"] is True

    def test_recommend_confidence_score_range(self):
        r = client.post("/recommend", json={"goal": "Coding Agent"})
        data = r.json()
        assert 0.0 <= data["confidence_score"] <= 1.0

    def test_recommend_required_skills_nonempty(self):
        r = client.post("/recommend", json={"goal": "Coding Agent"})
        data = r.json()
        assert len(data["required_skills"]) > 0

    def test_recommend_unknown_goal_returns_404(self):
        r = client.post("/recommend", json={"goal": "ZZZ Unknown Nonexistent Goal 999"})
        assert r.status_code == 404

    def test_recommend_invalid_experience_returns_422(self):
        r = client.post("/recommend", json={"goal": "Coding Agent", "experience": "guru"})
        assert r.status_code == 422

    def test_recommend_with_time_budget(self):
        r = client.post(
            "/recommend",
            json={"goal": "Coding Agent", "experience": "beginner", "time_budget_hours": 40},
        )
        assert r.status_code == 200
        data = r.json()
        # With time budget, we still get a valid response
        assert "required_skills" in data


# ===========================================================================
# POST /blueprint — 6 tests
# ===========================================================================

class TestBlueprint:
    def test_blueprint_valid_goal(self):
        r = client.post("/blueprint", json={"goal": "Coding Agent"})
        assert r.status_code == 200

    def test_blueprint_response_shape(self):
        r = client.post("/blueprint", json={"goal": "Coding Agent"})
        data = r.json()
        assert "id" in data
        assert "title" in data
        assert "goal" in data
        assert "goal_id" in data
        assert "confidence_score" in data
        assert "architecture_type" in data
        assert "required_skills" in data
        assert "learning_path" in data

    def test_blueprint_id_format(self):
        r = client.post("/blueprint", json={"goal": "Coding Agent"})
        data = r.json()
        assert data["id"].startswith("blueprint-")

    def test_blueprint_confidence_range(self):
        r = client.post("/blueprint", json={"goal": "Coding Agent"})
        data = r.json()
        assert 0.0 <= data["confidence_score"] <= 1.0

    def test_blueprint_unknown_goal_returns_404(self):
        r = client.post("/blueprint", json={"goal": "Nonexistent Agent XYZ 999"})
        assert r.status_code == 404

    def test_blueprint_required_skills_have_rank(self):
        r = client.post("/blueprint", json={"goal": "RAG Assistant"})
        data = r.json()
        assert len(data["required_skills"]) > 0
        for skill in data["required_skills"]:
            assert "rank" in skill, f"Missing rank in skill: {skill.get('id')}"


# ===========================================================================
# Bonus: root endpoint & OpenAPI
# ===========================================================================

class TestMeta:
    def test_root_returns_200(self):
        r = client.get("/")
        assert r.status_code == 200

    def test_openapi_json_available(self):
        r = client.get("/openapi.json")
        assert r.status_code == 200
        data = r.json()
        assert "openapi" in data
        assert "paths" in data

    def test_swagger_ui_available(self):
        r = client.get("/docs")
        assert r.status_code == 200


if __name__ == "__main__":
    pytest.main(["-v", __file__])
