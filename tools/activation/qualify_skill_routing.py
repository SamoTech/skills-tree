#!/usr/bin/env python3
"""Qualify Hermes skill routing on one fresh session per benchmark case.

Extracted verbatim from the "Qualify Hermes skill routing before the full benchmark" step of
.github/workflows/skill-activation-runtime.yml (behavior-preserving
decomposition, 2026-10-12). Runs under the same interpreter, environment,
and working directory as the original inline heredoc.
"""

import json
import os
import shutil
import subprocess
from pathlib import Path

dataset = json.loads(Path("benchmarks/activation/skill-activation-v1.json").read_text(encoding="utf-8"))
trace_root = Path(os.environ["RUNNER_TEMP"]) / "activation-qualification"
trace_root.mkdir(parents=True, exist_ok=True)
base_home = Path(os.environ["HERMES_HOME"])
model = os.environ["HERMES_LOCAL_MODEL"]
expected_runtime_names = {
    "03-memory/rag": "skills-tree-rag",
    "05-code/code-review": "skills-tree-code-review",
    "11-web/web-search": "skills-tree-web-search",
}

for case in dataset["cases"]:
    trace_id = f'{case["id"]}-qualification'
    trace_path = trace_root / f"{trace_id}.jsonl"
    trace_path.unlink(missing_ok=True)
    trace_path.touch()
    session_home = trace_root / f"{trace_id}-home"
    shutil.rmtree(session_home, ignore_errors=True)
    session_home.mkdir(parents=True)
    (session_home / "config.yaml").write_bytes((base_home / "config.yaml").read_bytes())
    for dirname in ("plugins", "skills"):
        (session_home / dirname).symlink_to(base_home / dirname, target_is_directory=True)

    env = os.environ.copy()
    env["SKILLS_TREE_HERMES_TRACE"] = str(trace_path)
    env["HERMES_HOME"] = str(session_home)
    env["HERMES_RUNTIME_HOME"] = str(base_home)
    log_path = trace_root / f"{trace_id}.log"
    print(f"QUALIFY START {case['id']}", flush=True)
    try:
        proc = subprocess.run(
            ["hermes", "chat", "--toolsets", "skills", "-q", case["prompt"],
             "--provider", "custom", "--model", model],
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=240,
        )
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        log_path.write_text(output + "\nqualification stopped after 60s; checking activation trace\n", encoding="utf-8")
        selected_timeout, loaded_timeout = set(), set()
        for line in trace_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            event = json.loads(line)
            if event.get("hook_event_name") == "post_tool_call" and event.get("tool_name") == "skill_view":
                name = (event.get("args") or {}).get("name")
                if isinstance(name, str) and name:
                    selected_timeout.add(name)
            if event.get("hook_event_name") == "on_skill_lifecycle" and event.get("action") == "loaded":
                name = event.get("skill_name")
                if isinstance(name, str) and name:
                    loaded_timeout.add(name)
        expected_timeout = expected_runtime_names[case["expected_skill"]]
        if selected_timeout != {expected_timeout} or loaded_timeout != {expected_timeout}:
            raise SystemExit(f"FAIL: {case['id']} did not produce exactly one expected skill selection and load within 60 seconds; selected={sorted(selected_timeout)}, loaded={sorted(loaded_timeout)}.")
        print(f"PASS: {case['id']} produced the exact expected selection and load evidence before the response timeout.", flush=True)
        continue

    selected, loaded = set(), set()
    for line in trace_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if event.get("hook_event_name") == "post_tool_call" and event.get("tool_name") == "skill_view":
            name = (event.get("args") or {}).get("name")
            if isinstance(name, str) and name:
                selected.add(name)
        if event.get("hook_event_name") == "on_skill_lifecycle" and event.get("action") == "loaded":
            name = event.get("skill_name")
            if isinstance(name, str) and name:
                loaded.add(name)

    expected = expected_runtime_names[case["expected_skill"]]
    if selected != {expected}:
        raise SystemExit(f"FAIL: {case['id']} must call skill_view exactly once for {expected}; observed {sorted(selected)}.")
    if loaded != {expected}:
        raise SystemExit(f"FAIL: {case['id']} must load exactly {expected}; observed {sorted(loaded)}.")
    print(f"PASS: {case['id']} selected and loaded only {expected}.", flush=True)

print("PASS: all four routing qualification cases passed; starting the 12-observation benchmark.", flush=True)
