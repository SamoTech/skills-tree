import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/convert_hermes_activation_observations.py"


def test_hermes_adapter_requires_explicit_correlation_and_emits_only_observed_events(tmp_path):
    raw = tmp_path / "hermes.jsonl"
    raw.write_text(
        "\n".join(
            [
                json.dumps({
                    "hook_event_name": "post_tool_call",
                    "tool_name": "skill_view",
                    "args": {"name": "03-memory/rag"},
                    "session_id": "sess-1",
                }),
                json.dumps({
                    "hook_event_name": "on_skill_lifecycle",
                    "action": "loaded",
                    "skill_name": "03-memory/rag",
                    "session_id": "sess-1",
                }),
            ]
        ) + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "observations.json"
    result = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            str(raw),
            "--case-map",
            json.dumps({"sess-1": "ACT-001"}),
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["runs"][0]["case_id"] == "ACT-001"
    assert {event["kind"] for event in payload["runs"][0]["events"]} == {
        "skill_selection",
        "skill_execution",
    }


def test_hermes_adapter_does_not_infer_execution_from_selection(tmp_path):
    raw = tmp_path / "hermes.jsonl"
    raw.write_text(
        json.dumps({
            "hook_event_name": "post_tool_call",
            "tool_name": "skill_view",
            "args": {"name": "03-memory/rag"},
            "session_id": "sess-1",
        }) + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "observations.json"
    subprocess.run(
        [
            sys.executable,
            str(TOOL),
            str(raw),
            "--case-map",
            json.dumps({"sess-1": "ACT-001"}),
            "--output",
            str(output),
        ],
        check=True,
    )
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["runs"] == []
