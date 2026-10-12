#!/usr/bin/env python3
"""Run the independent fresh-session activation observations.

Extracted verbatim from the "Run 12 independent fresh-session observations" step of
.github/workflows/skill-activation-runtime.yml (behavior-preserving
decomposition, 2026-10-12). Runs under the same interpreter, environment,
and working directory as the original inline heredoc.
"""

import json
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

cases = json.loads(Path("benchmarks/activation/skill-activation-v1.json").read_text())["cases"]
trace_root = Path(os.environ["RUNNER_TEMP"]) / "activation-traces"
base_home = Path(os.environ["HERMES_HOME"])
model = os.environ["HERMES_LOCAL_MODEL"]

runs = []
for case in cases:
    for repetition in range(1, int(case["repetitions"]) + 1):
        runs.append((case, repetition))

def run_observation(item):
    case, repetition = item
    trace_id = f'{case["id"]}-r{repetition}'
    trace_path = trace_root / f"{trace_id}.jsonl"
    trace_path.unlink(missing_ok=True)
    # Preserve every attempted fresh session, including a valid
    # negative observation where Hermes never calls skill_view.
    # Otherwise the converter silently drops sessions with no events,
    # biasing activation rates and making the corpus incomplete.
    trace_path.touch()

    session_home = trace_root / f"{trace_id}-hermes-home"
    shutil.rmtree(session_home, ignore_errors=True)
    session_home.mkdir(parents=True, exist_ok=True)

    # Keep the installed runtime and static benchmark assets shared.
    # Only Hermes HOME state is isolated per observation. Copy only the
    # non-secret config so enabled plugins and runtime settings remain
    # identical; do not copy .env, auth, databases, sessions, or logs.
    (session_home / "config.yaml").write_bytes((base_home / "config.yaml").read_bytes())
    for dirname in ("plugins", "skills"):
        (session_home / dirname).symlink_to(base_home / dirname, target_is_directory=True)

    env = os.environ.copy()
    env["SKILLS_TREE_HERMES_TRACE"] = str(trace_path)
    env["HERMES_HOME"] = str(session_home)
    env["HERMES_RUNTIME_HOME"] = str(base_home)

    print(f"=== START {trace_id} ===", flush=True)
    try:
        proc = subprocess.run(
            ["hermes", "chat", "--toolsets", "skills", "-q", case["prompt"], "--provider", "custom", "--model", model],
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=240,
        )
        (trace_root / f"{trace_id}.log").write_text(proc.stdout, encoding="utf-8")
        print(f"=== END {trace_id}: exit_code={proc.returncode} ===", flush=True)
        return trace_id, proc.returncode
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        (trace_root / f"{trace_id}.log").write_text(
            output + "\nrunner timeout after 60s; evaluating captured activation evidence\n",
            encoding="utf-8",
        )
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
        if selected_timeout and loaded_timeout:
            print(f"=== END {trace_id}: response timed out after valid activation trace ===", flush=True)
            return trace_id, 0
        print(f"=== TIMEOUT {trace_id}: no complete activation evidence ===", flush=True)
        return trace_id, 124
    except Exception as exc:
        (trace_root / f"{trace_id}.log").write_text(
            f"runner exception: {exc}\n",
            encoding="utf-8",
        )
        print(f"=== ERROR {trace_id}: {exc} ===", flush=True)
        return trace_id, 125

max_workers = 1
with ThreadPoolExecutor(max_workers=max_workers) as pool:
    futures = [pool.submit(run_observation, item) for item in runs]
    for future in as_completed(futures):
        trace_id, rc = future.result()
        print(f"completed {trace_id} rc={rc}", flush=True)
