"""Regression tests for typed Benchmark runtime access."""

import json
from pathlib import Path

import pytest

from registry.runtime import UniversalRegistry


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "universal_registry.json"


def _registry_with_benchmark(tmp_path: Path) -> UniversalRegistry:
    target = tmp_path / "registry" / "universal_registry.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    data["entities"]["benchmarks"] = [{
        "id": "benchmark/synthetic-behavior-check",
        "version": "1.0",
        "name": "Synthetic Behavior Check",
        "task": "Verify deterministic benchmark retrieval and snapshot isolation.",
        "inputs": ["candidate output"],
        "expected_behavior": ["returns a deterministic evaluation result"],
        "evaluation_criteria": ["deterministic lookup", "read-only snapshots"],
        "test_data": ["fixture://benchmark/synthetic-behavior-check"],
        "methodology": "Repository-local synthetic fixture for runtime contract testing.",
        "historical_results": [],
        "subjects": ["05-code/code-review"],
        "provenance": {"source_type": "repository", "source": "tests/test_benchmark_runtime.py"}
    }]
    target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    for schema_name in (
        "implementation-contract.schema.json",
        "adapter-contract.schema.json",
        "evidence-contract.schema.json",
        "compatibility-model.schema.json",
        "benchmark-contract.schema.json",
        "universal-graph.schema.json",
        "universal-registry-data.schema.json",
    ):
        schema_target = tmp_path / "meta" / schema_name
        schema_target.parent.mkdir(parents=True, exist_ok=True)
        schema_target.write_text((ROOT / "meta" / schema_name).read_text(encoding="utf-8"), encoding="utf-8")
    graph_target = tmp_path / "graph" / "universal_graph.json"
    graph_target.parent.mkdir(parents=True, exist_ok=True)
    graph_target.write_text((ROOT / "graph" / "universal_graph.json").read_text(encoding="utf-8"), encoding="utf-8")
    return UniversalRegistry(target)


def test_resolve_benchmark_returns_normative_record(tmp_path: Path) -> None:
    registry = _registry_with_benchmark(tmp_path)
    record = registry.resolve_benchmark("benchmark/synthetic-behavior-check")
    assert record["task"].startswith("Verify deterministic benchmark")
    assert record["subjects"] == ["05-code/code-review"]


def test_benchmarks_for_entity_is_deterministic(tmp_path: Path) -> None:
    registry = _registry_with_benchmark(tmp_path)
    records = registry.benchmarks_for_entity("05-code/code-review")
    assert [item["id"] for item in records] == ["benchmark/synthetic-behavior-check"]


def test_unknown_benchmark_is_rejected(tmp_path: Path) -> None:
    registry = _registry_with_benchmark(tmp_path)
    with pytest.raises(KeyError, match="Unknown benchmark"):
        registry.resolve_benchmark("benchmark/missing")


def test_benchmark_runtime_returns_read_only_snapshots(tmp_path: Path) -> None:
    registry = _registry_with_benchmark(tmp_path)
    first = registry.resolve_benchmark("benchmark/synthetic-behavior-check")
    first["expected_behavior"].append("mutated")
    second = registry.resolve_benchmark("benchmark/synthetic-behavior-check")
    assert "mutated" not in second["expected_behavior"]


def _benchmark_with(subject: str = "05-code/code-review") -> dict[str, object]:
    return {
        "id": "benchmark/fixture",
        "version": "1.0",
        "name": "Fixture",
        "task": "Exercise registry benchmark validation.",
        "inputs": ["input"],
        "expected_behavior": ["deterministic behavior"],
        "evaluation_criteria": ["criteria"],
        "test_data": ["fixture://benchmark"],
        "methodology": "Repository-local synthetic fixture.",
        "historical_results": [],
        "subjects": [subject],
        "provenance": {"source_type": "repository", "source": "tests/test_benchmark_runtime.py"},
    }


def test_benchmark_subject_must_exist(tmp_path: Path) -> None:
    target = tmp_path / "registry" / "universal_registry.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    data["entities"]["benchmarks"] = [_benchmark_with("missing/entity")]
    target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    for schema_name in (
        "implementation-contract.schema.json",
        "adapter-contract.schema.json",
        "evidence-contract.schema.json",
        "compatibility-model.schema.json",
        "benchmark-contract.schema.json",
        "universal-graph.schema.json",
        "universal-registry-data.schema.json",
    ):
        schema_target = tmp_path / "meta" / schema_name
        schema_target.parent.mkdir(parents=True, exist_ok=True)
        schema_target.write_text((ROOT / "meta" / schema_name).read_text(encoding="utf-8"), encoding="utf-8")
    graph_target = tmp_path / "graph" / "universal_graph.json"
    graph_target.parent.mkdir(parents=True, exist_ok=True)
    graph_target.write_text((ROOT / "graph" / "universal_graph.json").read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(ValueError, match="unknown entity"):
        UniversalRegistry(target)


def test_benchmark_definition_lists_must_not_be_empty(tmp_path: Path) -> None:
    target = tmp_path / "registry" / "universal_registry.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    benchmark = _benchmark_with()
    benchmark["inputs"] = []
    data["entities"]["benchmarks"] = [benchmark]
    target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    for schema_name in (
        "implementation-contract.schema.json",
        "adapter-contract.schema.json",
        "evidence-contract.schema.json",
        "compatibility-model.schema.json",
        "benchmark-contract.schema.json",
        "universal-graph.schema.json",
        "universal-registry-data.schema.json",
    ):
        schema_target = tmp_path / "meta" / schema_name
        schema_target.parent.mkdir(parents=True, exist_ok=True)
        schema_target.write_text((ROOT / "meta" / schema_name).read_text(encoding="utf-8"), encoding="utf-8")
    graph_target = tmp_path / "graph" / "universal_graph.json"
    graph_target.parent.mkdir(parents=True, exist_ok=True)
    graph_target.write_text((ROOT / "graph" / "universal_graph.json").read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(Exception):
        UniversalRegistry(target)
