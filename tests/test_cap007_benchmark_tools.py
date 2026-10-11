from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import run_cap007_retrieval_benchmark as runner
import validate_cap007_dataset as validator

QUERY_TYPES = ["exact_match", "paraphrase", "multi_hop", "no_relevant_document"]


def write_skills_tree(tmp_path: Path) -> Path:
    skills_root = tmp_path / "skills"
    for skill_id in ("07-tool-use/web-search", "03-memory/rag", "05-code/debugging"):
        skill_file = skills_root / f"{skill_id}.md"
        skill_file.parent.mkdir(parents=True, exist_ok=True)
        skill_file.write_text("# Synthetic fixture skill\n", encoding="utf-8")
    return skills_root


def write_dataset(tmp_path: Path, count: int = 100, dangling: bool = False, duplicate: bool = False) -> Path:
    cases = []
    for i in range(1, count + 1):
        query_type = QUERY_TYPES[(i - 1) % 4]
        if dangling and i == 1:
            expected = ["99-nonexistent/no-such-skill"]
        elif query_type == "no_relevant_document":
            expected = []
        else:
            expected = ["07-tool-use/web-search"]
        cases.append({
            "case_id": f"CAP007-TEST-{i:03d}" if not (duplicate and i == count) else "CAP007-TEST-001",
            "query": f"Synthetic schema test support query {i}",
            "query_type": query_type,
            "expected_skill_ids": expected,
            "labeling": {
                "labeler_id": "schema-test-fixture",
                "labeled_at": "2026-10-11T00:00:00Z",
                "evidence_references": [f"fixture://case/{i}"],
                "rationale": "Synthetic rationale used only to test tool behavior.",
            },
        })
    dataset = {
        "schema_version": "1.0",
        "benchmark_id": "cap007-retrieval-human-v1",
        "dataset_status": "human_labeled",
        "provenance": {
            "source_type": "support_tickets",
            "created_at": "2026-10-11T00:00:00Z",
            "label_protocol": "Synthetic schema test fixture, not actual human labels.",
            "source_references": ["fixture://cap007-schema-test"],
            "labels_independent_of_retrieval_engine": True,
        },
        "cases": cases,
    }
    path = tmp_path / "cap007-dataset.json"
    path.write_text(json.dumps(dataset, indent=2), encoding="utf-8")
    return path


def load_schema() -> dict:
    return json.loads((ROOT / "benchmarks" / "retrieval" / "cap007-dataset.schema.json").read_text(encoding="utf-8"))


def test_validator_accepts_valid_dataset(tmp_path):
    skills_root = write_skills_tree(tmp_path)
    dataset_path = write_dataset(tmp_path)
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    report = validator.validate_dataset(dataset, load_schema(), skills_root)
    assert report["status"] == "VALID"
    assert report["cases"] == 100
    assert all(report["query_type_counts"][qt] == 25 for qt in QUERY_TYPES)
    assert report["distinct_labelers"] == 1


def test_validator_rejects_dangling_skill_reference(tmp_path):
    skills_root = write_skills_tree(tmp_path)
    dataset_path = write_dataset(tmp_path, dangling=True)
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    report = validator.validate_dataset(dataset, load_schema(), skills_root)
    assert report["status"] == "INVALID"
    assert any("unresolved canonical skill" in err for err in report["errors"])


def test_validator_rejects_duplicate_case_ids(tmp_path):
    skills_root = write_skills_tree(tmp_path)
    dataset_path = write_dataset(tmp_path, duplicate=True)
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    report = validator.validate_dataset(dataset, load_schema(), skills_root)
    assert report["status"] == "INVALID"
    assert any("duplicate case ids" in err for err in report["errors"])


def test_validator_rejects_fewer_than_100_cases(tmp_path):
    skills_root = write_skills_tree(tmp_path)
    dataset_path = write_dataset(tmp_path, count=99)
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    report = validator.validate_dataset(dataset, load_schema(), skills_root)
    assert report["status"] == "INVALID"
    assert any(err.startswith("schema:") for err in report["errors"])


def test_validator_main_returns_exit_codes(tmp_path):
    skills_root = write_skills_tree(tmp_path)
    dataset_path = write_dataset(tmp_path)
    assert validator.main([
        "--dataset", str(dataset_path),
        "--skills-root", str(skills_root),
    ]) == 0
    bad_path = write_dataset(tmp_path, count=99)
    bad_path = bad_path.rename(tmp_path / "bad.json") if False else bad_path
    assert validator.main([
        "--dataset", str(bad_path),
        "--skills-root", str(skills_root),
    ]) == 1


def test_compute_metrics_micro_averages_hits():
    cases = [
        {"case_id": "CAP007-A", "query_type": "exact_match", "expected_skill_ids": ["s1", "s2"]},
        {"case_id": "CAP007-B", "query_type": "no_relevant_document", "expected_skill_ids": []},
    ]
    per_case = {
        "CAP007-A": (["s1", "x", "y", "z", "w"], 1.5),
        "CAP007-B": (["a", "b", "c", "d", "e"], 2.5),
    }
    metrics = runner.compute_metrics(cases, per_case)
    assert metrics["recall_at_5"] == 0.5
    assert metrics["precision_at_5"] == 0.1
    assert metrics["query_type_breakdown"]["no_relevant_document"]["recall_at_5"] is None
    assert metrics["query_type_breakdown"]["no_relevant_document"]["precision_at_5"] == 0.0
    assert metrics["latency_ms"]["p50"] == 1.5
    assert metrics["latency_ms"]["p95"] == 2.5


def test_decide_status_follows_ontology_thresholds():
    assert runner.decide_status(0.85, 0.75, 5000, True) == "PASS"
    assert runner.decide_status(0.99, 0.99, 100, True) == "PASS"
    assert runner.decide_status(0.80, 0.80, 5000, True) == "NEEDS_INVESTIGATION"
    assert runner.decide_status(0.79, 0.90, 100, True) == "OBSERVED_FAILURE"
    assert runner.decide_status(0.90, 0.69, 100, True) == "OBSERVED_FAILURE"
    assert runner.decide_status(0.90, 0.90, 5001, True) == "OBSERVED_FAILURE"
    assert runner.decide_status(0.99, 0.99, 100, False) == "OBSERVED_FAILURE"


def test_runner_returns_not_run_for_invalid_dataset(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    skills_root = write_skills_tree(tmp_path)
    dataset_path = write_dataset(tmp_path, count=99)
    index_path = tmp_path / "search-index.json"
    index_path.write_text(json.dumps([]), encoding="utf-8")
    output_path = tmp_path / "cap007-result.json"
    exit_code = runner.main([
        "--dataset", str(dataset_path),
        "--skills-root", str(skills_root),
        "--index", str(index_path),
        "--output", str(output_path),
    ])
    assert exit_code == 1
    result = json.loads(output_path.read_text(encoding="utf-8"))
    assert result["status"] == "NOT_RUN"
    assert result["validation"]["status"] == "INVALID"
