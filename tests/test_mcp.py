#!/usr/bin/env python3
"""
MCP server tests — Sprint C-10

Validates the Architect MCP tool layer and minimal JSON-RPC server wrapper.
24 tests total.
"""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest

from mcp.tools import (
    recommend_skills,
    generate_blueprint,
    list_goals,
    list_skills,
    tool_schemas,
    dispatch_tool,
    MCPToolError,
)
from mcp.server import handle_request


# ===========================================================================
# Tool metadata — 4 tests
# ===========================================================================

class TestToolSchemas:
    def test_tool_count(self):
        schemas = tool_schemas()
        assert len(schemas) == 4

    def test_tool_names(self):
        names = [t["name"] for t in tool_schemas()]
        assert "recommend_skills" in names
        assert "generate_blueprint" in names
        assert "list_goals" in names
        assert "list_skills" in names

    def test_recommend_schema_has_goal(self):
        schema = next(t for t in tool_schemas() if t["name"] == "recommend_skills")
        assert "goal" in schema["input_schema"]["properties"]

    def test_generate_blueprint_requires_goal(self):
        schema = next(t for t in tool_schemas() if t["name"] == "generate_blueprint")
        assert schema["input_schema"]["required"] == ["goal"]


# ===========================================================================
# Direct tool calls — 10 tests
# ===========================================================================

class TestDirectTools:
    def test_list_goals_returns_list(self):
        result = list_goals()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_list_goals_item_shape(self):
        item = list_goals()[0]
        assert "id" in item
        assert "name" in item

    def test_list_skills_returns_list(self):
        result = list_skills()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_list_skills_item_shape(self):
        item = list_skills()[0]
        assert "id" in item
        assert "name" in item

    def test_recommend_skills_valid_goal(self):
        result = recommend_skills("Coding Agent")
        assert result["goal_id"].startswith("G")
        assert "required_skills" in result
        assert len(result["required_skills"]) > 0

    def test_recommend_skills_confidence_range(self):
        result = recommend_skills("Coding Agent")
        assert 0.0 <= result["confidence_score"] <= 1.0

    def test_recommend_skills_budget(self):
        result = recommend_skills("Coding Agent", "intermediate", 40)
        assert "required_skills" in result
        assert isinstance(result["required_skills"], list)

    def test_generate_blueprint_valid_goal(self):
        result = generate_blueprint("Coding Agent")
        assert result["id"].startswith("blueprint-")
        assert result["goal_id"].startswith("G")

    def test_generate_blueprint_contains_required_skills(self):
        result = generate_blueprint("RAG Assistant")
        assert "required_skills" in result
        assert len(result["required_skills"]) > 0

    def test_unknown_goal_raises(self):
        with pytest.raises(MCPToolError):
            recommend_skills("Unknown Goal XYZ 999")


# ===========================================================================
# Generic dispatcher — 4 tests
# ===========================================================================

class TestDispatcher:
    def test_dispatch_recommend(self):
        result = dispatch_tool("recommend_skills", {"goal": "Coding Agent"})
        assert "goal_id" in result

    def test_dispatch_blueprint(self):
        result = dispatch_tool("generate_blueprint", {"goal": "Coding Agent"})
        assert "architecture_type" in result

    def test_dispatch_list_goals(self):
        result = dispatch_tool("list_goals", {})
        assert isinstance(result, list)

    def test_dispatch_unknown_tool(self):
        with pytest.raises(MCPToolError):
            dispatch_tool("not_a_real_tool", {})


# ===========================================================================
# JSON-RPC server wrapper — 6 tests
# ===========================================================================

class TestServerJSONRPC:
    def test_initialize(self):
        response = handle_request({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {},
        })
        assert response["result"]["serverInfo"]["name"] == "architect-mcp-server"

    def test_tools_list(self):
        response = handle_request({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {},
        })
        assert "tools" in response["result"]
        assert len(response["result"]["tools"]) == 4

    def test_tools_call_recommend(self):
        response = handle_request({
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "recommend_skills",
                "arguments": {"goal": "Coding Agent"},
            },
        })
        assert "result" in response
        payload = json.loads(response["result"]["content"][0]["text"])
        assert "goal_id" in payload

    def test_tools_call_blueprint(self):
        response = handle_request({
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "generate_blueprint",
                "arguments": {"goal": "Coding Agent"},
            },
        })
        assert "result" in response
        payload = json.loads(response["result"]["content"][0]["text"])
        assert "architecture_type" in payload

    def test_tools_call_unknown_tool_returns_error(self):
        response = handle_request({
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "fake_tool",
                "arguments": {},
            },
        })
        assert "error" in response
        assert response["error"]["code"] == -32000

    def test_unknown_method_returns_error(self):
        response = handle_request({
            "jsonrpc": "2.0",
            "id": 6,
            "method": "totally/unknown",
            "params": {},
        })
        assert "error" in response
        assert response["error"]["code"] == -32601


if __name__ == "__main__":
    pytest.main(["-v", __file__])
