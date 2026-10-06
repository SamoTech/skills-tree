#!/usr/bin/env python3
"""Convert explicit Hermes hook evidence into the Skills Tree activation observation contract.

The adapter consumes JSON Lines emitted by Hermes observer hooks. It never infers
activation from prompts, usage counters, or prose. A skill_selection event is
created only from an observed post_tool_call for skill_view; a skill_execution
event is created only from an observed on_skill_lifecycle action=loaded. Selection-only
or execution-only observations are preserved so missing or mismatched evidence remains measurable.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_events(path: Path) -> list[dict]:
    events = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON on line {number}: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"line {number} must contain a JSON object")
        events.append(value)
    return events


def correlation_key(event: dict) -> str:
    return str(
        event.get("session_id")
        or event.get("task_id")
        or event.get("extra", {}).get("task_id")
        or ""
    )


def skill_name(event: dict) -> str | None:
    return event.get("skill_name") or event.get("extra", {}).get("skill_name")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--case-map", required=True, help="JSON object mapping session/task correlation keys to ACT-### case IDs")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    events = load_events(Path(args.input))
    case_map = json.loads(args.case_map)
    if not isinstance(case_map, dict):
        raise ValueError("--case-map must be a JSON object")
    grouped: dict[str, dict[str, set[str]]] = defaultdict(
        lambda: {"selected": set(), "executed": set()}
    )

    for event in events:
        kind = event.get("hook_event_name") or event.get("event")
        key = correlation_key(event)
        if not key:
            continue

        if kind == "post_tool_call" and event.get("tool_name") == "skill_view":
            args_obj = event.get("args") or event.get("tool_input") or {}
            selected = args_obj.get("name") if isinstance(args_obj, dict) else None
            if selected:
                grouped[key]["selected"].add(str(selected))

        if kind == "on_skill_lifecycle" and event.get("action") == "loaded":
            loaded = skill_name(event)
            if loaded:
                grouped[key]["executed"].add(str(loaded))

    runs = []
    for index, key in enumerate(sorted(grouped), 1):
        case_id = case_map.get(key)
        if not isinstance(case_id, str) or not case_id:
            continue
        selected = grouped[key]["selected"]
        executed = grouped[key]["executed"]
        if not selected and not executed:
            continue
        events_out = []
        for skill_id in sorted(selected):
            events_out.append({"kind": "skill_selection", "skill_id": skill_id, "status": "observed"})
        for skill_id in sorted(executed):
            events_out.append({"kind": "skill_execution", "skill_id": skill_id, "status": "observed"})
        runs.append({"run_id": f"hermes-{index:03d}", "case_id": case_id, "trace_id": key, "events": events_out})

    Path(args.output).write_text(
        json.dumps({"schema_version": "1.0", "runs": runs}, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
