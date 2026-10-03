from __future__ import annotations

import json

from typer.testing import CliRunner

from cli.main import app

runner = CliRunner()


def test_search_command_returns_ranked_json_results():
    result = runner.invoke(app, ["search", "memory"])
    assert result.exit_code == 0, result.output
    data = json.loads(result.output)
    assert isinstance(data, list)
    assert data
    assert {"id", "title", "category", "level", "stability", "description", "score"} <= data[0].keys()
    assert all(data[i]["score"] >= data[i + 1]["score"] for i in range(len(data) - 1))


def test_search_command_respects_limit():
    result = runner.invoke(app, ["search", "agent", "--limit", "3"])
    assert result.exit_code == 0, result.output
    assert len(json.loads(result.output)) <= 3


def test_search_command_table_output():
    result = runner.invoke(app, ["search", "memory", "--format", "table"])
    assert result.exit_code == 0
    assert "score" in result.output


def test_search_command_rejects_non_word_query():
    result = runner.invoke(app, ["search", "!!!"])
    assert result.exit_code == 1
    assert "at least one word" in result.output


def test_search_command_returns_empty_array_for_unmatched_query():
    result = runner.invoke(app, ["search", "zzzzunlikelytoken999"])
    assert result.exit_code == 0
    assert json.loads(result.output) == []
