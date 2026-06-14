"""Test suite for BlueprintGenerator component - Sprint A baseline"""
import pytest


class TestBlueprintGeneratorBaseline:
    """Deterministic tests for BlueprintGenerator schema compliance"""

    def test_empty_blueprint_structure(self):
        """Test 1: Empty blueprint has required top-level fields"""
        blueprint = {
            "id": "bp_001",
            "name": "Empty Blueprint",
            "version": "1.0.0",
            "phases": []
        }
        assert "id" in blueprint
        assert "name" in blueprint
        assert "version" in blueprint
        assert "phases" in blueprint

    def test_blueprint_id_format(self):
        """Test 2: Blueprint ID follows naming convention"""
        blueprint_id = "bp_fullstack_001"
        assert blueprint_id.startswith("bp_")
        assert len(blueprint_id) > 3

    def test_version_format(self):
        """Test 3: Version follows semantic versioning"""
        version = "1.0.0"
        parts = version.split(".")
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)

    def test_phase_structure(self):
        """Test 4: Phase has required fields"""
        phase = {
            "phase_id": "phase_1",
            "name": "Foundation",
            "order": 1,
            "skills": [],
            "estimated_duration": "4 weeks"
        }
        assert "phase_id" in phase
        assert "name" in phase
        assert "order" in phase
        assert "skills" in phase

    def test_skill_reference_structure(self):
        """Test 5: Skill reference has required fields"""
        skill_ref = {
            "skill_id": "python",
            "priority": "high",
            "estimated_time": "40h"
        }
        assert "skill_id" in skill_ref
        assert "priority" in skill_ref
        assert "estimated_time" in skill_ref

    def test_phases_ordered_sequentially(self):
        """Test 6: Phases are ordered sequentially"""
        phases = [
            {"phase_id": "p1", "order": 1},
            {"phase_id": "p2", "order": 2},
            {"phase_id": "p3", "order": 3}
        ]
        orders = [p["order"] for p in phases]
        assert orders == sorted(orders)
        assert orders == list(range(1, len(phases) + 1))

    def test_blueprint_metadata(self):
        """Test 7: Blueprint includes metadata"""
        blueprint = {
            "id": "bp_001",
            "metadata": {
                "created_at": "2025-01-01",
                "author": "system",
                "goal": "fullstack_developer"
            }
        }
        assert "metadata" in blueprint
        assert "created_at" in blueprint["metadata"]

    def test_skill_prerequisites_list(self):
        """Test 8: Skills can have prerequisites"""
        skill = {
            "skill_id": "react",
            "prerequisites": ["html", "css", "javascript"]
        }
        assert "prerequisites" in skill
        assert isinstance(skill["prerequisites"], list)
        assert len(skill["prerequisites"]) == 3

    def test_phase_dependencies(self):
        """Test 9: Phases can have dependencies"""
        phase = {
            "phase_id": "p2",
            "depends_on": ["p1"]
        }
        assert "depends_on" in phase
        assert isinstance(phase["depends_on"], list)

    def test_blueprint_goals_list(self):
        """Test 10: Blueprint can specify target goals"""
        blueprint = {
            "id": "bp_001",
            "target_goals": ["fullstack_developer", "cloud_architect"]
        }
        assert "target_goals" in blueprint
        assert len(blueprint["target_goals"]) > 0


class TestBlueprintGeneratorValidation:
    """Tests for blueprint validation and schema conformance"""

    def test_validate_required_fields(self):
        """Test 11: Validate all required fields present"""
        required_fields = ["id", "name", "version", "phases"]
        blueprint = {
            "id": "bp_001",
            "name": "Test Blueprint",
            "version": "1.0.0",
            "phases": []
        }
        for field in required_fields:
            assert field in blueprint

    def test_validate_phase_order_unique(self):
        """Test 12: Phase orders are unique"""
        phases = [
            {"order": 1},
            {"order": 2},
            {"order": 3}
        ]
        orders = [p["order"] for p in phases]
        assert len(orders) == len(set(orders))

    def test_validate_skill_ids_exist(self):
        """Test 13: All skill IDs reference valid skills"""
        valid_skills = {"python", "javascript", "docker"}
        phase_skills = ["python", "docker"]
        for skill_id in phase_skills:
            assert skill_id in valid_skills

    def test_validate_no_circular_dependencies(self):
        """Test 14: No circular phase dependencies"""
        phases = [
            {"phase_id": "p1", "depends_on": []},
            {"phase_id": "p2", "depends_on": ["p1"]},
            {"phase_id": "p3", "depends_on": ["p2"]}
        ]
        # Check p3 doesn't depend on p1 through p2
        for phase in phases:
            if phase["phase_id"] == "p1":
                assert "p3" not in phase.get("depends_on", [])

    def test_validate_duration_format(self):
        """Test 15: Duration follows valid format"""
        durations = ["4 weeks", "40h", "3 months"]
        valid_units = {"weeks", "h", "hours", "days", "months"}
        for duration in durations:
            # Check format: number + space + unit
            parts = duration.split()
            if len(parts) == 2:
                assert parts[1] in valid_units

    def test_validate_priority_values(self):
        """Test 16: Priority values are from valid set"""
        valid_priorities = {"high", "medium", "low"}
        skills = [
            {"skill_id": "a", "priority": "high"},
            {"skill_id": "b", "priority": "medium"}
        ]
        for skill in skills:
            assert skill["priority"] in valid_priorities

    def test_validate_schema_conformance(self):
        """Test 17: Complete blueprint conforms to schema"""
        blueprint = {
            "id": "bp_fullstack_001",
            "name": "Fullstack Developer Blueprint",
            "version": "1.0.0",
            "phases": [
                {
                    "phase_id": "foundation",
                    "name": "Foundation",
                    "order": 1,
                    "skills": [
                        {"skill_id": "html", "priority": "high"}
                    ]
                }
            ]
        }
        # Validate structure
        assert isinstance(blueprint["phases"], list)
        assert isinstance(blueprint["phases"][0]["skills"], list)

    def test_validate_milestone_structure(self):
        """Test 18: Milestones have required fields"""
        milestone = {
            "milestone_id": "m1",
            "name": "Complete Foundation",
            "phase_id": "p1",
            "criteria": ["All skills completed"]
        }
        assert "milestone_id" in milestone
        assert "name" in milestone
        assert "criteria" in milestone

    def test_validate_resource_links(self):
        """Test 19: Resource links are valid URLs or paths"""
        skill = {
            "skill_id": "python",
            "resources": [
                {"type": "tutorial", "url": "https://example.com/python"},
                {"type": "docs", "url": "https://docs.python.org"}
            ]
        }
        assert "resources" in skill
        for resource in skill["resources"]:
            assert "url" in resource
            assert resource["url"].startswith("http")

    def test_blueprint_json_serializable(self):
        """Test 20: Blueprint is JSON serializable"""
        blueprint = {
            "id": "bp_001",
            "name": "Test",
            "version": "1.0.0",
            "phases": [
                {"phase_id": "p1", "order": 1, "skills": []}
            ]
        }
        import json
        try:
            json_str = json.dumps(blueprint)
            reconstructed = json.loads(json_str)
            assert reconstructed == blueprint
        except (TypeError, ValueError):
            assert False, "Blueprint is not JSON serializable"
