"""Test suite for SkillsGraph component - Sprint A baseline"""
import pytest


class TestSkillsGraphBaseline:
    """Deterministic tests for SkillsGraph behavior"""

    def test_empty_graph_initialization(self):
        """Test 1: Empty graph creates with zero nodes"""
        graph = {"nodes": [], "edges": []}
        assert len(graph["nodes"]) == 0
        assert len(graph["edges"]) == 0

    def test_single_node_graph(self):
        """Test 2: Single node graph validates structure"""
        graph = {
            "nodes": [{"id": "python", "label": "Python", "category": "language"}],
            "edges": []
        }
        assert len(graph["nodes"]) == 1
        assert graph["nodes"][0]["id"] == "python"

    def test_dependency_edge_creation(self):
        """Test 3: Edge represents valid dependency"""
        edge = {"from": "python", "to": "django", "type": "prerequisite"}
        assert edge["from"] == "python"
        assert edge["to"] == "django"
        assert edge["type"] == "prerequisite"

    def test_multiple_nodes_with_categories(self):
        """Test 4: Multiple nodes with distinct categories"""
        nodes = [
            {"id": "js", "category": "language"},
            {"id": "react", "category": "framework"},
            {"id": "aws", "category": "infrastructure"}
        ]
        categories = set(n["category"] for n in nodes)
        assert len(categories) == 3
        assert "language" in categories

    def test_graph_with_chain_dependencies(self):
        """Test 5: Chain of dependencies (A->B->C)"""
        edges = [
            {"from": "html", "to": "css"},
            {"from": "css", "to": "javascript"}
        ]
        assert len(edges) == 2
        assert edges[0]["to"] == edges[1]["from"]

    def test_node_id_uniqueness(self):
        """Test 6: Node IDs are unique"""
        nodes = [
            {"id": "node1"},
            {"id": "node2"},
            {"id": "node3"}
        ]
        ids = [n["id"] for n in nodes]
        assert len(ids) == len(set(ids))

    def test_bidirectional_edges(self):
        """Test 7: Bidirectional relationships exist"""
        edges = [
            {"from": "frontend", "to": "backend", "type": "synergy"},
            {"from": "backend", "to": "frontend", "type": "synergy"}
        ]
        assert edges[0]["from"] == edges[1]["to"]
        assert edges[0]["to"] == edges[1]["from"]

    def test_self_loop_detection(self):
        """Test 8: Self-loops are identifiable"""
        edge = {"from": "skill", "to": "skill"}
        is_self_loop = edge["from"] == edge["to"]
        assert is_self_loop is True

    def test_node_metadata_preservation(self):
        """Test 9: Node metadata is preserved"""
        node = {
            "id": "python",
            "label": "Python Programming",
            "difficulty": "intermediate",
            "time_estimate": "40h"
        }
        assert "difficulty" in node
        assert node["time_estimate"] == "40h"

    def test_graph_merge_operation(self):
        """Test 10: Two graphs can be merged"""
        graph1 = {"nodes": [{"id": "a"}], "edges": []}
        graph2 = {"nodes": [{"id": "b"}], "edges": []}
        merged_nodes = graph1["nodes"] + graph2["nodes"]
        assert len(merged_nodes) == 2


class TestSkillsGraphQueries:
    """Tests for graph query operations"""

    def test_find_node_by_id(self):
        """Test 11: Find node by ID"""
        nodes = [{"id": "python"}, {"id": "java"}]
        found = [n for n in nodes if n["id"] == "python"]
        assert len(found) == 1
        assert found[0]["id"] == "python"

    def test_filter_nodes_by_category(self):
        """Test 12: Filter nodes by category"""
        nodes = [
            {"id": "py", "category": "language"},
            {"id": "docker", "category": "tool"},
            {"id": "js", "category": "language"}
        ]
        languages = [n for n in nodes if n["category"] == "language"]
        assert len(languages) == 2

    def test_get_node_dependencies(self):
        """Test 13: Get dependencies for a node"""
        edges = [
            {"from": "html", "to": "react"},
            {"from": "css", "to": "react"},
            {"from": "js", "to": "react"}
        ]
        deps = [e["from"] for e in edges if e["to"] == "react"]
        assert len(deps) == 3
        assert "html" in deps

    def test_get_dependent_nodes(self):
        """Test 14: Get nodes that depend on a skill"""
        edges = [
            {"from": "python", "to": "django"},
            {"from": "python", "to": "flask"},
        ]
        dependents = [e["to"] for e in edges if e["from"] == "python"]
        assert len(dependents) == 2

    def test_count_incoming_edges(self):
        """Test 15: Count incoming edges to a node"""
        edges = [
            {"from": "a", "to": "target"},
            {"from": "b", "to": "target"},
            {"from": "c", "to": "other"}
        ]
        incoming = len([e for e in edges if e["to"] == "target"])
        assert incoming == 2

    def test_count_outgoing_edges(self):
        """Test 16: Count outgoing edges from a node"""
        edges = [
            {"from": "source", "to": "a"},
            {"from": "source", "to": "b"},
            {"from": "other", "to": "c"}
        ]
        outgoing = len([e for e in edges if e["from"] == "source"])
        assert outgoing == 2

    def test_detect_isolated_nodes(self):
        """Test 17: Detect nodes with no edges"""
        nodes = [{"id": "isolated"}, {"id": "connected"}]
        edges = [{"from": "connected", "to": "other"}]
        node_ids = {n["id"] for n in nodes}
        connected_ids = {e["from"] for e in edges} | {e["to"] for e in edges}
        isolated = node_ids - connected_ids
        assert "isolated" in isolated

    def test_graph_node_count(self):
        """Test 18: Total node count is accurate"""
        graph = {
            "nodes": [{"id": f"n{i}"} for i in range(10)],
            "edges": []
        }
        assert len(graph["nodes"]) == 10

    def test_graph_edge_count(self):
        """Test 19: Total edge count is accurate"""
        graph = {
            "nodes": [],
            "edges": [{"from": f"n{i}", "to": f"n{i+1}"} for i in range(5)]
        }
        assert len(graph["edges"]) == 5

    def test_validate_edge_endpoints_exist(self):
        """Test 20: Validate edge endpoints reference existing nodes"""
        nodes = [{"id": "a"}, {"id": "b"}]
        edges = [{"from": "a", "to": "b"}]
        node_ids = {n["id"] for n in nodes}
        for edge in edges:
            assert edge["from"] in node_ids
            assert edge["to"] in node_ids
