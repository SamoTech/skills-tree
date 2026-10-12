#!/usr/bin/env python3
"""Validate the observation corpus against the schema.

Extracted verbatim from the "Validate observation corpus against schema" step of
.github/workflows/skill-activation-runtime.yml (behavior-preserving
decomposition, 2026-10-12). Runs under the same interpreter, environment,
and working directory as the original inline heredoc.
"""

import json, os
from pathlib import Path
from jsonschema import Draft202012Validator

obs = json.loads((Path(os.environ["RUNNER_TEMP"]) / "skill-activation-observations.json").read_text())
schema = json.loads(Path("meta/skill-activation-observation.schema.json").read_text())
errors = list(Draft202012Validator(schema).iter_errors(obs))
if errors:
    print(errors[0].message)
    raise SystemExit(1)
print("PASS: observation corpus matches schema.")
