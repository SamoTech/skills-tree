import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from registry.runtime import UniversalRegistry
ROOT=Path(__file__).resolve().parents[1]; REGISTRY=ROOT/"registry"/"universal_registry.json"; GRAPH=ROOT/"graph"/"universal_graph.json"; SCHEMA=ROOT/"meta"/"universal-graph.schema.json"
def test_universal_graph_schema_is_valid():
    Draft202012Validator.check_schema(json.loads(SCHEMA.read_text(encoding="utf-8")))
def test_typed_graph_edges_resolve_to_registry_entities():
    edges=UniversalRegistry(REGISTRY).graph_edges()
    assert len(edges)==8
    assert edges==sorted(edges,key=lambda x:(x["source"],x["relationship_type"],x["target"]))
    assert any(edge["source"]=="05-code/code-review" and edge["target"]=="implementation/code-reviewer-system" for edge in edges)
    assert any(edge["target"]=="protocol/model-context-protocol" for edge in edges)
def test_graph_edges_are_deterministic():
    r=UniversalRegistry(REGISTRY); assert r.graph_edges()==r.graph_edges()
def test_graph_rejects_wrong_endpoint_type(tmp_path):
    graph=json.loads(GRAPH.read_text(encoding="utf-8")); graph["edges"][0]["target_type"]="skill"
    broken=tmp_path/"broken-graph.json"; broken.write_text(json.dumps(graph),encoding="utf-8")
    r=UniversalRegistry(REGISTRY); r._graph_data=graph
    with pytest.raises(ValueError,match="Invalid typed graph endpoint"): r.graph_edges()
def test_graph_rejects_self_loop(tmp_path):
    graph=json.loads(GRAPH.read_text(encoding="utf-8")); graph["edges"][0]["target"]=graph["edges"][0]["source"]; graph["edges"][0]["target_type"]=graph["edges"][0]["source_type"]
    broken=tmp_path/"broken-graph.json"; broken.write_text(json.dumps(graph),encoding="utf-8")
    r=UniversalRegistry(REGISTRY); r._graph_data=graph
    with pytest.raises(ValueError,match="Graph self-loop"): r.graph_edges()
