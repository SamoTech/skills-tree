from pathlib import Path

from tools.reconcile_agent_skills import reconcile, reconciliation_failures


def write_skill(root: Path, rel: str, body: str = "# Skill\n\n## Evidence\n\n- Repository evidence\n") -> Path:
    path = root / "skills" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\ndescription: \"A useful skill.\"\n---\n\n{body}", encoding="utf-8")
    return path


def write_package(root: Path, package: str, source: str, body: str = "# Skill\n\n## Evidence\n\n- Repository evidence\n") -> None:
    path = root / "agent-skills" / package / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\nname: {package}\ndescription: A useful skill.\nmetadata:\n  source: {source}\n---\n\n{body}",
        encoding="utf-8",
    )


def test_check_fails_for_eligible_missing(tmp_path):
    write_skill(tmp_path, "01-test/example.md")
    report = reconcile(tmp_path)
    assert report["eligible_missing"]
    assert "eligible_missing: 1" in reconciliation_failures(report)


def test_check_fails_for_projection_drift(tmp_path):
    write_skill(tmp_path, "01-test/example.md")
    write_package(
        tmp_path,
        "example",
        "skills/01-test/example.md",
        "# Drift\n\n## Evidence\n\n- Different\n",
    )
    report = reconcile(tmp_path)
    assert report["drifted"]
    assert "drifted: 1" in reconciliation_failures(report)


def test_check_fails_for_rename_and_stale_provenance(tmp_path):
    write_skill(tmp_path, "01-test/example.md")
    write_package(tmp_path, "legacy-example", "skills/01-test/example.md")
    write_package(tmp_path, "stale", "skills/01-test/removed.md")
    report = reconcile(tmp_path)
    assert report["rename_needed"]
    assert report["stale"]
    failures = reconciliation_failures(report)
    assert "rename_needed: 1" in failures
    assert "stale: 1" in failures
