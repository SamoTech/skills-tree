#!/usr/bin/env python3
"""Render benchmark result summary lines for the step summary.

Extracted verbatim from the "Write evidence summary" step of
.github/workflows/skill-activation-runtime.yml (behavior-preserving
decomposition, 2026-10-12). Runs under the same interpreter, environment,
and working directory as the original inline heredoc.
"""

import json, os
from pathlib import Path
p=Path(os.environ["RUNNER_TEMP"])/"skill-activation-benchmark-result.json"
d=json.loads(p.read_text())
print(f"- Status: **{d['status']}**")
print(f"- Runs: **{d['metrics']['runs']} / {d['metrics']['required_runs']}**")
print(f"- Observed cases: **{d['metrics']['observed_cases']} / {d['metrics']['cases']}**")
print(f"- Invocation evidence rate: **{d['metrics']['invocation_evidence_rate']}**")
print(f"- False activation rate: **{d['metrics']['false_activation_rate']}**")
print(f"- Acceptance: **{d.get('acceptance', {}).get('status', 'NOT_EVALUATED')}**")
for failure in d.get('acceptance', {}).get('failures', []):
    print(f"  - FAIL: {failure}")
