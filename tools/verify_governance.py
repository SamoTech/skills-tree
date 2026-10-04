#!/usr/bin/env python3
"""Verify repository-level governance contracts without GitHub branch protection."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def fail(message):
    print(f"FAIL: {message}")
    raise SystemExit(1)

def require_file(path):
    p = ROOT / path
    if not p.is_file(): fail(f"required governance file is missing: {path}")
    return p.read_text(encoding="utf-8")

def require_path(path):
    p = ROOT / path
    if not p.exists(): fail(f"required governance path is missing: {path}")
    return p

def main():
    agents = require_file("AGENTS.md")
    constitution = require_file("AI_CONSTITUTION.md")
    require_file("meta/CURRENT-STATE.md")
    require_file("meta/memory/DECISIONS.md")
    workflows_dir = ROOT / ".github/workflows"
    workflows = {p.name: p.read_text(encoding="utf-8") for p in workflows_dir.glob("*.yml")}

    for phrase in ("READ → VERIFY LIVE STATE → AUDIT DOCUMENTATION DRIFT → SYNCHRONIZE","COMPLETE requires both implementation and documentation verification.","Do not weaken validation or security gates","Treat `skills/` as the canonical registry source"):
        if phrase not in agents: fail(f"AGENTS.md lost mandatory clause: {phrase}")
    if "## 4. Documentation Is a Completion Gate" not in constitution: fail("documentation completion gate missing from AI_CONSTITUTION.md")
    if "## 10. Core Agentic Execution Contract" not in constitution: fail("core agentic execution contract missing from AI_CONSTITUTION.md")
    for phrase in ("OBSERVE → ASSESS → PLAN → EXECUTE → VERIFY → RECORD → DECIDE","treat failures and regressions as inputs to the next cycle","default loop ceiling is 12 iterations per goal","select `DONE` only after goal satisfaction"):
        if phrase not in constitution: fail(f"agentic execution invariant missing: {phrase}")
    if "## 11. Mandatory Agent Documentation Preflight Gate" not in constitution: fail("mandatory documentation preflight missing from AI_CONSTITUTION.md")

    operating = require_file("meta/AGENT_OPERATING_MODEL.md")
    for phrase in ("## Core Agentic Execution Loop","Failure-driven continuation","Bounded-loop safeguards","Completion contract","Authority boundary"):
        if phrase not in operating: fail(f"agent operating loop contract missing: {phrase}")

    for path in ("skills","tools/export_skills.py","tools/build_graph.py","tools/build_search_index.py"): require_path(path)

    release_writers = [name for name,text in workflows.items() if "semantic-release version" in text]
    if release_writers != ["zero-touch-release.yml"]: fail(f"release authority drift: semantic-release mutation found in {release_writers}")
    zero = workflows.get("zero-touch-release.yml", "")
    for phrase in ("NEXT=$(semantic-release version --print)","if: needs.semantic-release.outputs.released == 'true'","id-token: write"):
        if phrase not in zero: fail(f"zero-touch release contract missing: {phrase}")

    # All direct-main generated/release writers share one serialization boundary
    # and must synchronize their event checkout to the live main tip before
    # calculating or committing generated state.
    writer_contracts = {
        "zero-touch-release.yml": ("group: auto-commit-main", "queue: max", "git fetch origin main", "git reset --hard origin/main"),
        "validate-graph.yml": ("group: auto-commit-main", "git fetch origin main", "git reset --hard origin/main"),
        "generate-search-index.yml": ("group: auto-commit-main", "queue: max", "git push origin main"),
        "export-skills.yml": ("group: auto-commit-main", "git push origin main"),
        "update-skill-count.yml": ("group: auto-commit-main", "git push origin main"),
        "sync-badges.yml": ("group: auto-commit-main", "git push origin main"),
        "version-stats.yml": ("group: auto-commit-main", "git push origin main"),
        "leaderboard.yml": ("group: auto-commit-main", "git push origin main"),
        "weekly-highlights.yml": ("group: auto-commit-main", "git push origin main"),
        "used-in-tracker.yml": ("group: auto-commit-main", "git push origin main"),
        "quality-report.yml": ("group: auto-commit-main", "queue: max"),
        "generate-changelog.yml": ("group: auto-commit-main",),
    }
    for workflow, phrases in writer_contracts.items():
        text = workflows.get(workflow, "")
        if not text:
            fail(f"main writer workflow missing: {workflow}")
        for phrase in phrases:
            if phrase not in text: fail(f"main writer contract missing in {workflow}: {phrase}")

    quality = workflows.get("quality-report.yml", "")
    if "check_antislop.py --changed-only --base" not in quality: fail("blocking anti-slop gate missing")
    if "--enforce-new-stubs" not in quality: fail("blocking new-stub gate missing")

    security = workflows.get("security-scan.yml", "")
    for phrase in ("gitleaks/gitleaks-action@","bandit -r api cli mcp registry tools -lll -iii","pip-audit --strict"):
        if phrase not in security: fail(f"blocking security control missing: {phrase}")

    demand = workflows.get("demand-signals.yml", "")
    if not demand: fail("demand signal collection workflow missing")
    for phrase in ("tools/collect_demand_signals.py", "meta/demand-sources.json", "upload-artifact@v4"):
        if phrase not in demand: fail(f"demand signal collection contract missing: {phrase}")

    pages = workflows.get("deploy-pages.yml", "")
    for phrase in ("tools/build_agent_skills_discovery.py", "site/.well-known/agent-skills/index.json", "tools/verify_agent_skills_discovery.py"):
        if phrase not in pages: fail(f"Agent Skills publication contract missing: {phrase}")

    expected={"search":("generate-search-index.yml","build_search_index.py"),"jsonld":("export-skills.yml","export_skills.py"),"agent-skills":("agent-skills-distribution.yml","generate_agent_skills.py"),"graph":("validate-graph.yml","build_graph.py")}
    for label,(workflow,tool) in expected.items():
        if workflow not in workflows or tool not in workflows[workflow]: fail(f"{label} authoritative path missing or drifted: {workflow} / {tool}")

    policy=require_file("meta/GOVERNANCE_MODEL.md")
    if "GitHub branch protection is not a project completion gate" not in policy: fail("governance model does not decouple completion from branch protection")
    if "automated validation" not in policy: fail("governance model does not define automated validation as the merge gate")

    print("PASS: repository self-enforced governance contracts are intact.")
    print(f"PASS: inspected {len(workflows)} workflow files.")
    print("PASS: canonical source, projection writers, release, anti-slop, security, and documentation gates verified.")
    print("PASS: GitHub branch protection is not required by this repository-local gate.")

if __name__ == "__main__": main()
