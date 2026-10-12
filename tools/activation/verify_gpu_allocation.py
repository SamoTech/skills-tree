#!/usr/bin/env python3
"""Classify the Ollama model GPU allocation and record benchmark eligibility.

Extracted verbatim from the "Verify Ollama actually allocated GPU for the benchmark model" step of
.github/workflows/skill-activation-runtime.yml (behavior-preserving
decomposition, 2026-10-12). Runs under the same interpreter, environment,
and working directory as the original inline heredoc.
"""

import os
import re
from pathlib import Path

report = Path(os.environ["RUNNER_TEMP"]) / "activation-runtime-preflight.txt"
ps_file = Path(os.environ["RUNNER_TEMP"]) / "ollama-loaded-models.txt"
lines = ps_file.read_text(encoding="utf-8", errors="replace").splitlines()
model_lines = [line for line in lines if "qwen3.5:4b" in line]
if not model_lines:
    status = "RUNTIME_PREFLIGHT_FAILED"
    reason = "The expected qwen3.5:4b model was not present in ollama ps output."
else:
    allocation = model_lines[0]
    mixed = re.search(r"(\d+)%\s*/\s*(\d+)%\s+CPU/GPU", allocation, re.IGNORECASE)
    fully_gpu = re.search(r"\b100%\s+GPU\b", allocation, re.IGNORECASE)
    gpu_percent = int(mixed.group(2)) if mixed else (100 if fully_gpu else 0)
    if gpu_percent > 0:
        status = "RUNTIME_ELIGIBLE"
        reason = f"qwen3.5:4b reports {gpu_percent}% GPU allocation."
    else:
        status = "INFRASTRUCTURE_INELIGIBLE"
        reason = "The model is loaded without a verifiable GPU allocation; CPU-only runs are not eligible for this benchmark."
with report.open("a", encoding="utf-8") as stream:
    stream.write(f"STATUS={status}\n")
    stream.write(f"REASON={reason}\n")
summary = Path(os.environ["GITHUB_STEP_SUMMARY"])
with summary.open("a", encoding="utf-8") as stream:
    stream.write("## Activation benchmark runtime allocation\n")
    stream.write(f"- Status: **{status}**\n")
    stream.write(f"- Evidence: {reason}\n")
    if status == "INFRASTRUCTURE_INELIGIBLE":
        stream.write("- The routing qualification and 12-observation corpus were not started; this is not a skill-routing result.\n")
print(f"{status}: {reason}")
with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as stream:
    stream.write(f"eligible={'true' if status == 'RUNTIME_ELIGIBLE' else 'false'}\n")
