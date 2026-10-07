#!/usr/bin/env python3
"""Run the real Hermes activation corpus in isolated fresh sessions.

The harness deliberately records only explicit Hermes observer events. It never
infers activation from prompts or assistant prose. Each repetition gets a fresh
HERMES_HOME so session state and skill state cannot leak between observations.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


def run(cmd: list[str], env: dict[str, str], *, timeout: int, stdout: Path, stderr: Path) -> int:
    with stdout.open("w", encoding="utf-8") as out, stderr.open("w", encoding="utf-8") as err:
        proc = subprocess.run(cmd, env=env, stdout=out, stderr=err, timeout=timeout)
    return proc.returncode


def prepare_skill(source: Path, target: Path, skill_name: str) -> None:
    text = source.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"skill has no YAML frontmatter: {source}")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError(f"malformed frontmatter: {source}")
    frontmatter, body = parts[1], parts[2]
    if "\nname:" not in "\n" + frontmatter:
        frontmatter = f'name: "{skill_name}"\n' + frontmatter
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f"---\n{frontmatter}---\n{body}", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="benchmarks/activation/skill-activation-v1.json")
    parser.add_argument("--output-dir", default="activation-runtime-output")
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:8080/v1")
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    dataset = json.loads((root / args.dataset).read_text(encoding="utf-8"))
    output = root / args.output_dir
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    skill_sources = {
        "03-memory/rag": root / "skills/03-memory/rag.md",
        "05-code/code-review": root / "skills/05-code/code-review.md",
        "11-web/web-search": root / "skills/11-web/web-search.md",
    }

    all_events: list[dict] = []
    case_map: dict[str, str] = {}
    run_results: list[dict] = []

    for case in dataset["cases"]:
        case_id = case["id"]
        prompt = case["prompt"]
        repetitions = int(case.get("repetitions", 1))
        for repetition in range(1, repetitions + 1):
            run_key = f"{case_id}-R{repetition}"
            home = Path(tempfile.mkdtemp(prefix=f"hermes-{run_key.lower()}-"))
            trace = output / f"{run_key}.jsonl"
            stdout = output / f"{run_key}.stdout"
            stderr = output / f"{run_key}.stderr"
            try:
                env = os.environ.copy()
                env["HERMES_HOME"] = str(home)
                env["SKILLS_TREE_HERMES_TRACE"] = str(trace)

                # Disable the seeded bundled corpus: this runtime must expose only
                # the three Skills Tree benchmark skills.
                setup = [
                    "hermes", "skills", "opt-out", "--remove", "--yes",
                ]
                setup_rc = run(setup, env, timeout=120, stdout=stdout, stderr=stderr)

                plugin_dir = home / "plugins" / "skills-tree-activation"
                plugin_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(
                    root / "benchmarks/activation/hermes_skill_activation_observer.py",
                    plugin_dir / "__init__.py",
                )
                (plugin_dir / "plugin.yaml").write_text(
                    "name: skills-tree-activation\n"
                    "version: 1.0.0\n"
                    "description: Skills Tree activation evidence observer\n",
                    encoding="utf-8",
                )

                for skill_name, source in skill_sources.items():
                    prepare_skill(
                        source,
                        home / "skills" / skill_name / "SKILL.md",
                        skill_name,
                    )

                config_env = env.copy()
                config_steps = [
                    ["hermes", "plugins", "enable", "skills-tree-activation"],
                    ["hermes", "config", "set", "model.provider", "custom"],
                    ["hermes", "config", "set", "model.base_url", args.base_url],
                    ["hermes", "config", "set", "model.default", args.model],
                    ["hermes", "config", "set", "agent.max_turns", "12"],
                ]
                config_results = []
                for index, command in enumerate(config_steps, 1):
                    rc = run(
                        command,
                        config_env,
                        timeout=120,
                        stdout=output / f"{run_key}.setup-{index}.stdout",
                        stderr=output / f"{run_key}.setup-{index}.stderr",
                    )
                    config_results.append({"command": command[:4], "exit_code": rc})

                agent_stdout = output / f"{run_key}.agent.stdout"
                agent_stderr = output / f"{run_key}.agent.stderr"
                agent_rc = run(
                    [
                        "hermes", "chat", "--oneshot", "--quiet",
                        "--toolsets", "skills",
                        "--query", prompt,
                    ],
                    config_env,
                    timeout=args.timeout,
                    stdout=agent_stdout,
                    stderr=agent_stderr,
                )

                observed_events = []
                if trace.exists():
                    for line in trace.read_text(encoding="utf-8").splitlines():
                        if not line.strip():
                            continue
                        event = json.loads(line)
                        observed_events.append(event)
                        all_events.append(event)
                        key = str(
                            event.get("session_id")
                            or event.get("task_id")
                            or event.get("extra", {}).get("task_id")
                            or ""
                        )
                        if key:
                            case_map[key] = case_id

                run_results.append({
                    "case_id": case_id,
                    "repetition": repetition,
                    "setup_exit_code": setup_rc,
                    "config": config_results,
                    "agent_exit_code": agent_rc,
                    "event_count": len(observed_events),
                    "trace": str(trace),
                })
            finally:
                shutil.rmtree(home, ignore_errors=True)

    raw = output / "hermes-activation-observations.jsonl"
    raw.write_text(
        "\n".join(json.dumps(event, sort_keys=True) for event in all_events) + ("\n" if all_events else ""),
        encoding="utf-8",
    )
    (output / "case-map.json").write_text(json.dumps(case_map, indent=2) + "\n", encoding="utf-8")
    (output / "runtime-results.json").write_text(json.dumps(run_results, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "required_runs": sum(int(c.get("repetitions", 1)) for c in dataset["cases"]),
        "agent_invocations": len(run_results),
        "explicit_observer_events": len(all_events),
        "trace_groups": len(case_map),
        "raw_observations": str(raw),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
