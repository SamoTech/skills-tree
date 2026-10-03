"""Deterministic typed runtime access to benchmark evaluation definitions."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, NotRequired, TypedDict


class BenchmarkResult(TypedDict):
    """Normative historical benchmark result shape."""

    recorded_at: str
    metric: str
    value: Any
    notes: NotRequired[str]


class BenchmarkRecord(TypedDict):
    """Normative runtime shape for a registered Benchmark."""

    id: str
    version: str
    name: str
    task: str
    inputs: list[str]
    expected_behavior: list[str]
    evaluation_criteria: list[str]
    test_data: list[str]
    methodology: str
    historical_results: list[BenchmarkResult]
    subjects: NotRequired[list[str]]
    provenance: dict[str, Any]


class BenchmarkRuntime:
    """Read-only typed access to validated Benchmark records."""

    def __init__(self, registry_data: dict[str, Any]) -> None:
        benchmarks = registry_data.get("entities", {}).get("benchmarks")
        if not isinstance(benchmarks, list):
            raise ValueError("Registry must contain a benchmarks collection")
        self._data = registry_data

    def resolve_benchmark(self, benchmark_id: str) -> BenchmarkRecord:
        """Return one validated Benchmark record by canonical ID."""
        matches = [
            item
            for item in self._data["entities"]["benchmarks"]
            if item["id"] == benchmark_id
        ]
        if not matches:
            raise KeyError(f"Unknown benchmark: {benchmark_id}")
        return deepcopy(matches[0])

    def benchmarks_for_entity(self, entity_id: str) -> list[BenchmarkRecord]:
        """Return Benchmarks explicitly scoped to an entity in deterministic order."""
        records = [
            item
            for item in self._data["entities"]["benchmarks"]
            if entity_id in item.get("subjects", [])
        ]
        return deepcopy(sorted(records, key=lambda item: item["id"]))
