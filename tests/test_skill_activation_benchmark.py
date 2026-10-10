import json
from pathlib import Path

import pytest

from tools.run_skill_activation_benchmark import main


ROOT = Path(__file__).resolve().parents[1]


def write_observations(path: Path) -> None:
    path.write_text(json.dumps({
        "schema_version": "1.0",
        "runs": [
            {
                "run_id": "fixture-1",
                "case_id": "ACT-001",
                "trace_id": "trace-1",
                "events": [
                    {"kind": "skill_selection", "skill_id": "03-memory/rag", "status": "selected"},
                    {"kind": "skill_execution", "skill_id": "03-memory/rag", "status": "ok"}
                ]
            },
            {
                "run_id": "fixture-2",
                "case_id": "ACT-001",
                "trace_id": "trace-2",
                "events": [
                    {"kind": "skill_selection", "skill_id": "05-code/code-review", "status": "selected"}
                ]
            }
        ]
    }, indent=2) + "\n", encoding="utf-8")


def test_activation_benchmark_requires_explicit_observations(tmp_path, monkeypatch):
    observations = tmp_path / "observations.json"
    write_observations(observations)
    output = tmp_path / "result.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_skill_activation_benchmark.py",
            "--dataset", str(ROOT / "benchmarks/activation/skill-activation-v1.json"),
            "--observations", str(observations),
            "--output", str(output),
        ],
    )

    assert main() == 2
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["status"] == "PARTIAL"
    assert result["metrics"]["expected_activation_rate"] == 0.5
    assert result["metrics"]["false_activation_rate"] == 0.5
    assert result["metrics"]["invocation_evidence_rate"] == 0.5
    assert result["metrics"]["max_activation_variance"] == 1
    assert result["metrics"]["complete_cases"] == 0
    assert result["metrics"]["partial_cases"] == 1
    assert result["metrics"]["required_runs"] == 12


def test_empty_observation_set_is_not_pass(tmp_path, monkeypatch):
    observations = tmp_path / "observations.json"
    observations.write_text('{"schema_version":"1.0","runs":[]}\n', encoding="utf-8")
    output = tmp_path / "result.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_skill_activation_benchmark.py",
            "--dataset", str(ROOT / "benchmarks/activation/skill-activation-v1.json"),
            "--observations", str(observations),
            "--output", str(output),
        ],
    )

    assert main() == 2
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["status"] == "NO_OBSERVATIONS"
    assert result["metrics"]["expected_activation_rate"] is None
    assert result["metrics"]["invocation_evidence_rate"] is None



def test_complete_activation_corpus_is_distinguished(tmp_path, monkeypatch):
    observations = tmp_path / "observations.json"
    cases = json.loads(
        (ROOT / "benchmarks/activation/skill-activation-v1.json").read_text(encoding="utf-8")
    )["cases"]
    runs = []
    run_number = 1
    for case in cases:
        for _ in range(case["repetitions"]):
            runs.append({
                "run_id": f"complete-{run_number}",
                "case_id": case["id"],
                "trace_id": f"complete-trace-{run_number}",
                "events": [
                    {"kind": "skill_selection", "skill_id": case["expected_skill"], "status": "selected"},
                    {"kind": "skill_execution", "skill_id": case["expected_skill"], "status": "ok"},
                ],
            })
            run_number += 1
    observations.write_text(
        json.dumps({"schema_version": "1.0", "runs": runs}, indent=2) + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "result.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_skill_activation_benchmark.py",
            "--dataset", str(ROOT / "benchmarks/activation/skill-activation-v1.json"),
            "--observations", str(observations),
            "--output", str(output),
        ],
    )

    assert main() == 0
    result = json.loads(output.read_text(encoding="utf-8"))
    assert result["status"] == "COMPLETE"
    assert result["metrics"]["complete_cases"] == 4
    assert result["metrics"]["partial_cases"] == 0
    assert result["metrics"]["runs"] == 12


def write_custom_observations(path: Path, runs: list[dict]) -> None:
    path.write_text(
        json.dumps({"schema_version": "1.0", "runs": runs}, indent=2) + "\n",
        encoding="utf-8",
    )


def test_unknown_case_id_fails_closed(tmp_path, monkeypatch):
    observations = tmp_path / "observations.json"
    write_custom_observations(
        observations,
        [{
            "run_id": "run-unknown",
            "case_id": "ACT-999",
            "trace_id": "trace-unknown",
            "events": [
                {"kind": "skill_selection", "skill_id": "03-memory/rag", "status": "selected"},
            ],
        }],
    )
    output = tmp_path / "result.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_skill_activation_benchmark.py",
            "--dataset", str(ROOT / "benchmarks/activation/skill-activation-v1.json"),
            "--observations", str(observations),
            "--output", str(output),
        ],
    )

    with pytest.raises(ValueError, match="not present in selected dataset"):
        main()
    assert not output.exists()


def test_duplicate_run_id_fails_closed(tmp_path, monkeypatch):
    observations = tmp_path / "observations.json"
    duplicate = {
        "run_id": "run-duplicate",
        "case_id": "ACT-001",
        "trace_id": "trace-duplicate",
        "events": [
            {"kind": "skill_selection", "skill_id": "03-memory/rag", "status": "selected"},
        ],
    }
    write_custom_observations(observations, [duplicate, dict(duplicate)])
    output = tmp_path / "result.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_skill_activation_benchmark.py",
            "--dataset", str(ROOT / "benchmarks/activation/skill-activation-v1.json"),
            "--observations", str(observations),
            "--output", str(output),
        ],
    )

    with pytest.raises(ValueError, match="duplicate observation run_id"):
        main()
    assert not output.exists()


def test_case_status_matches_completion_status_for_partial_case(tmp_path, monkeypatch):
    observations = tmp_path / "observations.json"
    write_custom_observations(
        observations,
        [{
            "run_id": "run-partial",
            "case_id": "ACT-001",
            "trace_id": "trace-partial",
            "events": [
                {"kind": "skill_selection", "skill_id": "03-memory/rag", "status": "selected"},
            ],
        }],
    )
    output = tmp_path / "result.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_skill_activation_benchmark.py",
            "--dataset", str(ROOT / "benchmarks/activation/skill-activation-v1.json"),
            "--observations", str(observations),
            "--output", str(output),
        ],
    )

    assert main() == 2
    result = json.loads(output.read_text(encoding="utf-8"))
    row = next(row for row in result["cases_detail"] if row["id"] == "ACT-001")
    assert row["completion_status"] == "PARTIAL"
    assert row["status"] == "PARTIAL"


def test_duplicate_trace_id_fails_closed(tmp_path, monkeypatch):
    observations = tmp_path / "observations.json"
    write_custom_observations(
        observations,
        [
            {"run_id": "run-1", "case_id": "ACT-001", "trace_id": "same-trace", "events": []},
            {"run_id": "run-2", "case_id": "ACT-001", "trace_id": "same-trace", "events": []},
        ],
    )
    output = tmp_path / "result.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_skill_activation_benchmark.py",
            "--dataset", str(ROOT / "benchmarks/activation/skill-activation-v1.json"),
            "--observations", str(observations),
            "--output", str(output),
        ],
    )
    with pytest.raises(ValueError, match="duplicate observation trace_id"):
        main()
    assert not output.exists()



def complete_observation_runs() -> list[dict]:
    cases = json.loads(
        (ROOT / "benchmarks/activation/skill-activation-v1.json").read_text(encoding="utf-8")
    )["cases"]
    runs = []
    run_number = 1
    for case in cases:
        for _ in range(case["repetitions"]):
            runs.append({
                "run_id": f"negative-fixture-{run_number}",
                "case_id": case["id"],
                "trace_id": f"negative-trace-{run_number}",
                "events": [
                    {"kind": "skill_selection", "skill_id": case["expected_skill"], "status": "selected"},
                    {"kind": "skill_execution", "skill_id": case["expected_skill"], "status": "ok"},
                ],
            })
            run_number += 1
    return runs


def run_benchmark_with_runs(tmp_path, monkeypatch, runs: list[dict]) -> tuple[int, dict]:
    observations = tmp_path / "observations.json"
    write_custom_observations(observations, runs)
    output = tmp_path / "result.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_skill_activation_benchmark.py",
            "--dataset", str(ROOT / "benchmarks/activation/skill-activation-v1.json"),
            "--observations", str(observations),
            "--output", str(output),
        ],
    )
    exit_code = main()
    return exit_code, json.loads(output.read_text(encoding="utf-8"))


def test_complete_corpus_with_false_activation_fails_acceptance(tmp_path, monkeypatch):
    runs = complete_observation_runs()
    # ACT-001 must never select code-review; preserve all 12 observations.
    runs[0]["events"].append({
        "kind": "skill_selection",
        "skill_id": "05-code/code-review",
        "status": "selected",
    })

    exit_code, result = run_benchmark_with_runs(tmp_path, monkeypatch, runs)

    assert len(runs) == 12
    assert result["status"] == "COMPLETE"
    assert result["metrics"]["runs"] == result["metrics"]["required_runs"] == 12
    assert result["metrics"]["false_activation_rate"] > 0
    assert result["acceptance"]["status"] == "FAIL"
    assert "false activation rate must be 0.0" in result["acceptance"]["failures"]
    assert exit_code == 2


def test_complete_corpus_with_missing_invocation_evidence_fails_acceptance(tmp_path, monkeypatch):
    runs = complete_observation_runs()
    # Keep ACT-003's expected selection but remove explicit execution evidence.
    target = next(
        run for run in runs
        if run["case_id"] == "ACT-003" and run["run_id"] == "negative-fixture-7"
    )
    target["events"] = [
        event for event in target["events"]
        if not (event["kind"] == "skill_execution" and event["skill_id"] == "11-web/web-search")
    ]

    exit_code, result = run_benchmark_with_runs(tmp_path, monkeypatch, runs)

    assert len(runs) == 12
    assert result["status"] == "COMPLETE"
    assert result["metrics"]["invocation_evidence_rate"] < 1.0
    assert result["acceptance"]["status"] == "FAIL"
    assert "invocation evidence rate must be 1.0" in result["acceptance"]["failures"]
    assert exit_code == 2



def test_unmapped_skill_selection_is_a_false_activation(tmp_path, monkeypatch):
    runs = complete_observation_runs()
    # A runtime skill outside the benchmark mapping must not be silently ignored.
    runs[0]["events"].append({
        "kind": "skill_selection",
        "skill_id": "unmapped/hermes-agent-skill-authoring",
        "status": "selected",
    })

    exit_code, result = run_benchmark_with_runs(tmp_path, monkeypatch, runs)

    assert result["metrics"]["false_activation_rate"] > 0
    assert result["acceptance"]["status"] == "FAIL"
    assert "false activation rate must be 0.0" in result["acceptance"]["failures"]
    assert exit_code == 2
