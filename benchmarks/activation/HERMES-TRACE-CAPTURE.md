# Hermes Real Activation Trace Capture

This is an evidence-capture procedure for Issue #357. It does not simulate routing and it does not produce benchmark results by itself.

## Capture

1. Load `benchmarks/activation/hermes_skill_activation_observer.py` as a Hermes Python plugin.
2. Set `SKILLS_TREE_HERMES_TRACE` to a writable JSONL path.
3. Run the bounded `benchmark/skill-activation-v1` prompts in fresh Hermes sessions, preserving the session/task identifiers.
4. Capture 4 cases × 3 repetitions = 12 observations.
5. Keep environment-specific trace files outside the repository unless they are sanitized.

The observer records only explicit `skill_view` and `on_skill_lifecycle(action=loaded)` facts. It does not record prompts, model output, tool results, or aggregate usage counters.

## Convert

Map each captured correlation to its ACT case explicitly, then run `tools/convert_hermes_activation_observations.py` and `tools/run_skill_activation_benchmark.py`. A missing trace corpus is not PASS. Do not manufacture events.

## Evidence boundary

`skill_view` → `skill_selection` is explicit selection evidence.
`on_skill_lifecycle(action=loaded)` → `skill_execution` is explicit load/lifecycle evidence.
This does not prove downstream task efficacy or authorization.
