#!/usr/bin/env python3
"""
CLI tests — Sprint C-11

Validates all 5 skills-tree commands using Typer's CliRunner,
which exercises the full code path: CLI arg parsing → API layer → engine.

30 tests across 7 test classes.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from typer.testing import CliRunner

from cli.main import app

runner = CliRunner(mix_stderr=False)


# ===========================================================================
# recommend — 10 tests
# ===========================================================================

class TestRecommendCommand:
    def test_recommend_basic_exit_zero(self):
        result = runner.invoke(app, ["recommend", "--goal", "Coding Agent"])
        assert result.exit_code == 0, result.output

    def test_recommend_output_is_valid_json(self):
        result = runner.invoke(app, ["recommend", "--goal", "Coding Agent"])
        data = json.loads(result.output)
        assert isinstance(data, dict)

    def test_recommend_contains_goal_id(self):
        result = runner.invoke(app, ["recommend", "--goal", "Coding Agent"])
        data = json.loads(result.output)
        assert "goal_id" in data
        assert data["goal_id"].startswith("G")

    def test_recommend_contains_required_skills(self):
        result = runner.invoke(app, ["recommend", "--goal", "RAG Assistant"])
        data = json.loads(result.output)
        assert "required_skills" in data
        assert len(data["required_skills"]) > 0

    def test_recommend_confidence_in_range(self):
        result = runner.invoke(app, ["recommend", "--goal", "Coding Agent"])
        data = json.loads(result.output)
        assert 0.0 <= data["confidence_score"] <= 1.0

    def test_recommend_with_experience_beginner(self):
        result = runner.invoke(app, ["recommend", "--goal", "Browser Agent",
                                     "--experience", "beginner"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "goal_id" in data

    def test_recommend_with_experience_advanced(self):
        result = runner.invoke(app, ["recommend", "--goal", "Browser Agent",
                                     "--experience", "advanced"])
        assert result.exit_code == 0

    def test_recommend_with_time_budget(self):
        result = runner.invoke(app, ["recommend", "--goal", "Coding Agent",
                                     "--time-budget", "80"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "required_skills" in data

    def test_recommend_unknown_goal_exits_nonzero(self):
        result = runner.invoke(app, ["recommend", "--goal", "NonExistentGoalXYZ999"])
        assert result.exit_code != 0

    def test_recommend_short_flags(self):
        result = runner.invoke(app, ["recommend", "-g", "RAG Assistant", "-e", "intermediate"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "goal_id" in data


# ===========================================================================
# blueprint — 7 tests
# ===========================================================================

class TestBlueprintCommand:
    def test_blueprint_exit_zero(self):
        result = runner.invoke(app, ["blueprint", "--goal", "Coding Agent"])
        assert result.exit_code == 0, result.output

    def test_blueprint_valid_json(self):
        result = runner.invoke(app, ["blueprint", "--goal", "Coding Agent"])
        data = json.loads(result.output)
        assert isinstance(data, dict)

    def test_blueprint_has_architecture_type(self):
        result = runner.invoke(app, ["blueprint", "--goal", "Coding Agent"])
        data = json.loads(result.output)
        assert "architecture_type" in data

    def test_blueprint_has_goal_id(self):
        result = runner.invoke(app, ["blueprint", "--goal", "RAG Assistant"])
        data = json.loads(result.output)
        assert data["goal_id"].startswith("G")

    def test_blueprint_confidence_range(self):
        result = runner.invoke(app, ["blueprint", "--goal", "Analytics Agent"])
        data = json.loads(result.output)
        assert 0.0 <= data["confidence_score"] <= 1.0

    def test_blueprint_has_required_skills(self):
        result = runner.invoke(app, ["blueprint", "--goal", "Multi-Agent Systems"])
        data = json.loads(result.output)
        assert len(data["required_skills"]) > 0

    def test_blueprint_unknown_goal_exits_nonzero(self):
        result = runner.invoke(app, ["blueprint", "--goal", "NotAGoal999XYZ"])
        assert result.exit_code != 0


# ===========================================================================
# goals — 4 tests
# ===========================================================================

class TestGoalsCommand:
    def test_goals_exit_zero(self):
        result = runner.invoke(app, ["goals"])
        assert result.exit_code == 0

    def test_goals_returns_list(self):
        result = runner.invoke(app, ["goals"])
        data = json.loads(result.output)
        assert isinstance(data, list)
        assert len(data) > 0

    def test_goals_items_have_id_and_name(self):
        result = runner.invoke(app, ["goals"])
        data = json.loads(result.output)
        item = data[0]
        assert "id" in item
        assert "name" in item

    def test_goals_table_format(self):
        result = runner.invoke(app, ["goals", "--format", "table"])
        assert result.exit_code == 0
        assert "id" in result.output or "name" in result.output


# ===========================================================================
# skills — 4 tests
# ===========================================================================

class TestSkillsCommand:
    def test_skills_exit_zero(self):
        result = runner.invoke(app, ["skills"])
        assert result.exit_code == 0

    def test_skills_returns_list(self):
        result = runner.invoke(app, ["skills"])
        data = json.loads(result.output)
        assert isinstance(data, list)
        assert len(data) > 0

    def test_skills_items_have_id_and_name(self):
        result = runner.invoke(app, ["skills"])
        data = json.loads(result.output)
        item = data[0]
        assert "id" in item
        assert "name" in item

    def test_skills_table_format(self):
        result = runner.invoke(app, ["skills", "-f", "table"])
        assert result.exit_code == 0


# ===========================================================================
# validate — 6 tests
# ===========================================================================

class TestValidateCommand:
    def test_validate_no_goal_exit_zero(self):
        result = runner.invoke(app, ["validate"])
        assert result.exit_code == 0

    def test_validate_no_goal_all_pass(self):
        result = runner.invoke(app, ["validate"])
        data = json.loads(result.output)
        assert data["all_pass"] is True

    def test_validate_includes_health_check(self):
        result = runner.invoke(app, ["validate"])
        data = json.loads(result.output)
        assert "health" in data["checks"]
        assert data["checks"]["health"]["pass"] is True

    def test_validate_with_goal(self):
        result = runner.invoke(app, ["validate", "--goal", "Coding Agent"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["all_pass"] is True

    def test_validate_goal_checks_recommend_and_blueprint(self):
        result = runner.invoke(app, ["validate", "--goal", "RAG Assistant"])
        data = json.loads(result.output)
        assert "recommend" in data["checks"]
        assert "blueprint" in data["checks"]
        assert data["checks"]["recommend"]["pass"] is True
        assert data["checks"]["blueprint"]["pass"] is True

    def test_validate_includes_goal_and_skill_counts(self):
        result = runner.invoke(app, ["validate"])
        data = json.loads(result.output)
        assert data["checks"]["goals"]["goal_count"] > 0
        assert data["checks"]["skills"]["skill_count"] > 0


# ===========================================================================
# Output format variants — 3 tests
# ===========================================================================

class TestOutputFormats:
    def test_recommend_pretty_format(self):
        result = runner.invoke(app, ["recommend", "--goal", "Coding Agent", "--format", "pretty"])
        assert result.exit_code == 0
        # pretty uses rich rprint — output contains key names but not strict JSON
        assert "goal_id" in result.output or "Coding" in result.output

    def test_goals_pretty_format(self):
        result = runner.invoke(app, ["goals", "-f", "pretty"])
        assert result.exit_code == 0

    def test_blueprint_pretty_format(self):
        result = runner.invoke(app, ["blueprint", "--goal", "Coding Agent", "-f", "pretty"])
        assert result.exit_code == 0


# ===========================================================================
# App-level meta — 2 tests  (total: 36, satisfying >=30 requirement)
# ===========================================================================

class TestAppMeta:
    def test_help_exits_zero(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "recommend" in result.output
        assert "blueprint" in result.output

    def test_no_args_shows_help(self):
        result = runner.invoke(app, [])
        # Typer with no_args_is_help=True exits 0 and prints help
        assert "Usage" in result.output or "recommend" in result.output


if __name__ == "__main__":
    import pytest
    pytest.main(["-v", __file__])
