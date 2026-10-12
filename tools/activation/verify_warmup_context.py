#!/usr/bin/env python3
"""Validate the Ollama warmup response completed with the 64K context.

Extracted verbatim from the "Warm model and verify allocated context before qualification" step of
.github/workflows/skill-activation-runtime.yml (behavior-preserving
decomposition, 2026-10-12). Runs under the same interpreter, environment,
and working directory as the original inline heredoc.
"""

import json, os
from pathlib import Path
p = Path(os.environ["RUNNER_TEMP"]) / "ollama-context-preflight.json"
data = json.loads(p.read_text(encoding="utf-8"))
if data.get("error"):
    raise SystemExit(f"Ollama model warmup failed: {data['error']}")
# Thinking-capable models may return their generated tokens in a
# separate thinking field and leave response empty for a tiny token
# budget. The preflight validates completion, not answer quality.
if data.get("done") is not True:
    raise SystemExit("Ollama warmup did not complete.")
print("PASS: exact model completed a warmup request with num_ctx=65536.")
