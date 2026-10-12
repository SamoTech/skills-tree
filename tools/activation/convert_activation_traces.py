#!/usr/bin/env python3
"""Convert explicit runtime traces into benchmark observations.

Extracted verbatim from the "Convert explicit runtime traces to benchmark observations" step of
.github/workflows/skill-activation-runtime.yml (behavior-preserving
decomposition, 2026-10-12). Runs under the same interpreter, environment,
and working directory as the original inline heredoc.
"""

import json
import os
from pathlib import Path

trace_root = Path(os.environ["RUNNER_TEMP"]) / "activation-traces"
import re

mapping = {
    "skills-tree-rag": "03-memory/rag",
    "skills-tree-code-review": "05-code/code-review",
    "skills-tree-web-search": "11-web/web-search",
}

def observed_skill_id(name):
    if name in mapping:
        return mapping[name]
    # Preserve out-of-scope skill loads instead of silently dropping them.
    # The evaluator treats any non-expected skill selection as a false activation.
    safe_name = re.sub(r"[^a-z0-9._/-]+", "-", name.lower()).strip("-")
    return "unmapped/" + safe_name

runs = []
for trace_path in sorted(trace_root.glob("ACT-*.jsonl")):
    trace_id = trace_path.stem
    case_id = trace_id.split("-r", 1)[0]
    selected, executed = set(), set()

    for line in trace_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if event.get("hook_event_name") == "post_tool_call" and event.get("tool_name") == "skill_view":
            name = (event.get("args") or {}).get("name")
            if isinstance(name, str) and name:
                selected.add(observed_skill_id(name))
        if event.get("hook_event_name") == "on_skill_lifecycle" and event.get("action") == "loaded":
            name = event.get("skill_name")
            if isinstance(name, str) and name:
                executed.add(observed_skill_id(name))

    events = [
        {"kind": "skill_selection", "skill_id": skill, "status": "observed"}
        for skill in sorted(selected)
    ]
    events.extend(
        {"kind": "skill_execution", "skill_id": skill, "status": "observed"}
        for skill in sorted(executed)
    )

    runs.append({
        "run_id": trace_id,
        "case_id": case_id,
        "trace_id": trace_id,
        "events": events,
    })

out = Path(os.environ["RUNNER_TEMP"]) / "skill-activation-observations.json"
out.write_text(
    json.dumps({"schema_version": "1.0", "runs": runs}, indent=2) + chr(10),
    encoding="utf-8",
)
print(out.read_text())
