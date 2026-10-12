#!/usr/bin/env python3
"""Enforce the benchmark acceptance contract.

Extracted verbatim from the "Enforce benchmark acceptance contract" step of
.github/workflows/skill-activation-runtime.yml (behavior-preserving
decomposition, 2026-10-12). Runs under the same interpreter, environment,
and working directory as the original inline heredoc.
"""

import json
import os
from pathlib import Path

runtime_report = Path(os.environ["RUNNER_TEMP"]) / "activation-runtime-preflight.txt"
if runtime_report.exists():
    runtime_text = runtime_report.read_text(encoding="utf-8", errors="replace")
    if any(line in runtime_text.splitlines() for line in (
        "STATUS=INFRASTRUCTURE_INELIGIBLE",
        "STATUS=RUNTIME_PREFLIGHT_FAILED",
    )):
        print("NOT RUN: activation benchmark was blocked by runtime eligibility preflight.")
        print("Classification: infrastructure/runtime preflight, not skill-routing acceptance.")
        raise SystemExit(0)

result_path = Path(os.environ["RUNNER_TEMP"]) / "skill-activation-benchmark-result.json"
if not result_path.exists():
    raise SystemExit("FAIL: benchmark result is missing without a recorded runtime-preflight block.")
result = json.loads(result_path.read_text(encoding="utf-8"))
metrics = result.get("metrics", {})
acceptance = result.get("acceptance", {})
required_runs = metrics.get("required_runs")
runs = metrics.get("runs")
failures = list(acceptance.get("failures", []))
if result.get("status") != "COMPLETE":
    failures.append(f"corpus status must be COMPLETE, got {result.get('status')}")
if runs != required_runs:
    failures.append(f"observation count must equal required_runs ({required_runs}), got {runs}")
if metrics.get("expected_activation_rate") != 1.0:
    failures.append("expected_activation_rate must equal 1.0")
if metrics.get("false_activation_rate") != 0.0:
    failures.append("false_activation_rate must equal 0.0")
if metrics.get("invocation_evidence_rate") != 1.0:
    failures.append("invocation_evidence_rate must equal 1.0")
if acceptance.get("status") != "PASS" or failures:
    print("FAIL: benchmark acceptance contract not satisfied.")
    for failure in dict.fromkeys(failures):
        print(f"- {failure}")
    raise SystemExit(1)
print(f"PASS: exact {required_runs}-observation corpus meets all activation and invocation gates.")
