#!/usr/bin/env python3
"""Disable non-benchmark Hermes skills and install the skill_view allowlist patch.

Extracted verbatim from the "Restrict skill catalog to benchmark skills" step of
.github/workflows/skill-activation-runtime.yml (behavior-preserving
decomposition, 2026-10-12). Runs under the same interpreter, environment,
and working directory as the original inline heredoc.
"""

import os
from pathlib import Path
from agent.skill_utils import ESSENTIAL_SKILLS
from hermes_cli.config import load_config, save_config
from tools.skills_tool import _find_all_skills

allowed = {"skills-tree-rag", "skills-tree-code-review", "skills-tree-web-search"} | set(ESSENTIAL_SKILLS)
catalog = _find_all_skills(skip_disabled=True)
disabled = sorted({item["name"] for item in catalog if item["name"] not in allowed})
config = load_config()
config.setdefault("skills", {})["disabled"] = disabled
save_config(config)

# Enforce the benchmark's closed skill universe at the actual skill_view
# tool boundary too. Catalog filtering alone is not an authorization check:
# a model can still request a name that is not listed.
home = Path(os.environ["HERMES_HOME"])
runtime_file = home / "hermes-agent" / "tools" / "skills_tool.py"
source = runtime_file.read_text(encoding="utf-8")
function_start = source.find("def skill_view(")
if function_start < 0:
    raise SystemExit("Could not locate Hermes skill_view function.")
try_marker = "    try:\n"
try_start = source.find(try_marker, function_start)
if try_start < 0:
    raise SystemExit("Could not locate skill_view function entry.")
insert_at = try_start + len(try_marker)
guard = (
    "        allowed_benchmark_skills = {\n"
    "            \"skills-tree-rag\",\n"
    "            \"skills-tree-code-review\",\n"
    "            \"skills-tree-web-search\",\n"
    "        }\n"
    "        if name not in allowed_benchmark_skills:\n"
    "            return _fail(\n"
    "                f\"Skill '{name}' is outside the activation benchmark allowlist.\"\n"
    "            )\n"
)
runtime_file.write_text(source[:insert_at] + guard + source[insert_at:], encoding="utf-8")

print(f"Disabled {len(disabled)} unrelated skills; retained {sorted(allowed)}")
print("Installed strict skill_view allowlist for the three benchmark runtime names.")
