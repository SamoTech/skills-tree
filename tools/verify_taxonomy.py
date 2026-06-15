#!/usr/bin/env python3
"""
Runtime Taxonomy Integration Verification

Proves that architect.py is taxonomy-driven:
1. Run recommend("Coding Agent") -> capture BEFORE output
2. Inject TEST_SKILL_999 into GOAL_TAXONOMY.md (if not already present)
3. Run recommend("Coding Agent") again -> capture AFTER output
4. Diff the two outputs
5. Assert TEST_SKILL_999 appears in AFTER but not BEFORE
"""

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap: add tools/ to path so we can import architect
# ---------------------------------------------------------------------------
script_dir = Path(__file__).parent
repo_root = script_dir.parent
sys.path.insert(0, str(script_dir))

# ---------------------------------------------------------------------------
# Minimal graph stub (no SKILLS_GRAPH.json needed)
# ---------------------------------------------------------------------------
class StubGraph:
    nodes = {}
    edges = []
    def get_node(self, x): return None
    def get_dependencies(self, x, t="REQUIRES"): return []
    def get_recommendations(self, x): return []
    def get_learning_path(self, x): return []

# ---------------------------------------------------------------------------
# Import taxonomy-driven classes from architect
# ---------------------------------------------------------------------------
from architect import GoalTaxonomyParser, RecommendationEngine, BlueprintGenerator

TAXONOMY_PATH = repo_root / "meta" / "GOAL_TAXONOMY.md"
TESTSKILL = "TEST_SKILL_999"
GOAL = "Coding Agent"

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def run_recommend(taxonomy_path: Path) -> dict:
    taxonomy = GoalTaxonomyParser(str(taxonomy_path))
    graph = StubGraph()
    engine = RecommendationEngine(graph, taxonomy)
    generator = BlueprintGenerator()
    rec = engine.recommend(GOAL)
    if "error" in rec:
        return {"error": rec["error"]}
    bp = generator.generate(GOAL, rec, taxonomy)
    return {
        "taxonomy_skills": rec["taxonomy_skills"],
        "required_skill_ids": [s["id"] for s in rec["required_skills"]],
        "optional_skill_ids": [s["id"] for s in rec["optional_skills"]],
        "blueprint_required": [s["id"] for s in bp["required_skills"]],
        "blueprint_optional": [s["id"] for s in bp["optional_skills"]],
        "estimated_learn_hours": bp["estimated_learn_hours"],
        "architecture_type": bp["architecture_type"],
    }

# ---------------------------------------------------------------------------
# BEFORE: read current taxonomy, check if TEST_SKILL already present
# ---------------------------------------------------------------------------
raw = TAXONOMY_PATH.read_text(encoding="utf-8")
already_present = TESTSKILL in raw

print(f"[BEFORE] TEST_SKILL_999 already in taxonomy: {already_present}")

# If it's already there, temporarily remove it so we get a clean BEFORE
if already_present:
    cleaned = re.sub(
        r"^\d+\.\s+`TEST_SKILL_999`[^\n]*\n",
        "",
        raw,
        flags=re.MULTILINE,
    )
    TAXONOMY_PATH.write_text(cleaned, encoding="utf-8")
    print("[BEFORE] Removed TEST_SKILL_999 for clean baseline measurement")
    before_raw = cleaned
else:
    before_raw = raw

before_result = run_recommend(TAXONOMY_PATH)
print(f"[BEFORE] Skills: {before_result.get('required_skill_ids', [])}")
print(f"[BEFORE] TEST_SKILL_999 present: {TESTSKILL in json.dumps(before_result)}")

Path("verify_before.json").write_text(json.dumps(before_result, indent=2))

# ---------------------------------------------------------------------------
# INJECT: add TEST_SKILL_999 into G01.1 skill list
# ---------------------------------------------------------------------------
injection_line = f"6. `{TESTSKILL}` (Critical, 1hrs)\n"

# Insert after G01.1 skill list block (after file-operations line)
modified = re.sub(
    r"(5\.\s+`file-operations`[^\n]*\n)",
    r"\g<1>" + injection_line,
    before_raw,
    count=1,
)

if TESTSKILL not in modified:
    # Fallback: append after G01.1 header
    modified = before_raw.replace(
        "#### G01.1: Code Generation\n",
        f"#### G01.1: Code Generation\n\n**Required Skills (Priority Order):**\n\n1. `{TESTSKILL}` (Critical, 1hrs)\n",
        1,
    )

TAXONOMY_PATH.write_text(modified, encoding="utf-8")
print(f"[INJECT] TEST_SKILL_999 injected into taxonomy")

# ---------------------------------------------------------------------------
# AFTER
# ---------------------------------------------------------------------------
after_result = run_recommend(TAXONOMY_PATH)
print(f"[AFTER] Skills: {after_result.get('required_skill_ids', [])}")
print(f"[AFTER] TEST_SKILL_999 present: {TESTSKILL in json.dumps(after_result)}")

Path("verify_after.json").write_text(json.dumps(after_result, indent=2))

# ---------------------------------------------------------------------------
# DIFF
# ---------------------------------------------------------------------------
before_ids = set(
    before_result.get("required_skill_ids", []) +
    before_result.get("optional_skill_ids", [])
)
after_ids = set(
    after_result.get("required_skill_ids", []) +
    after_result.get("optional_skill_ids", [])
)

added = after_ids - before_ids
removed = before_ids - after_ids

diff_lines = [
    f"BEFORE skills: {sorted(before_ids)}",
    f"AFTER  skills: {sorted(after_ids)}",
    f"Added:         {sorted(added)}",
    f"Removed:       {sorted(removed)}",
    f"TEST_SKILL_999 in BEFORE: {TESTSKILL in before_ids}",
    f"TEST_SKILL_999 in AFTER:  {TESTSKILL in after_ids}",
]

diff_text = "\n".join(diff_lines)
Path("verify_diff.txt").write_text(diff_text)
print("\n--- DIFF ---")
print(diff_text)

# ---------------------------------------------------------------------------
# RESULT
# ---------------------------------------------------------------------------
passed = TESTSKILL not in before_ids and TESTSKILL in after_ids

result_lines = [
    f"BEFORE output: {json.dumps(before_result, indent=2)}",
    "",
    f"AFTER output: {json.dumps(after_result, indent=2)}",
    "",
    f"Difference detected: {bool(added or removed)}",
    f"Taxonomy truly drives recommendations: {'YES' if passed else 'NO'}",
    f"TEST: {'PASS' if passed else 'FAIL'}",
]

result_text = "\n".join(result_lines)
Path("verify_result.txt").write_text(result_text)
print("\n--- RESULT ---")
print(f"Difference detected: {bool(added or removed)}")
print(f"Taxonomy truly drives recommendations: {'YES' if passed else 'NO'}")
print(f"TEST: {'PASS' if passed else 'FAIL'}")

if not passed:
    sys.exit(1)
