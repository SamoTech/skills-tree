import json
from pathlib import Path

from tools.run_skill_activation_benchmark import main


ROOT = Path(__file__).resolve().parents[1]


def write_observations(path: Path) -> None:
    path.write_text(json.dumps({
        "schema_version": "1.0",
        "runs": [
            {
                "run_id": "fixture-1",
                "case_id": "ACT-001",
                "events": [
                    {"kind": "skill_selection", "skill_id": "03-memory/rag", "status": "selected"},
                    {"kind": "skill_execution", "skill_id": "03-memory/rag", "status": "ok"}
                ]
            },
            {
                "run_id": "fixture-2",
                "case_id": "ACT-001",
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

    assert main() == 0
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
