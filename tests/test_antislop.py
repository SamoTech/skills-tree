"""Tests for the deterministic anti-slop skill gate."""

from pathlib import Path

from tools.check_antislop import findings_for


def write_skill(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "skill.md"
    path.write_text("---\ntitle: Test\ncategory: test\n---\n" + body, encoding="utf-8")
    return path


def test_placeholder_is_error(tmp_path: Path) -> None:
    findings = findings_for(write_skill(tmp_path, "TODO: finish this skill"))
    assert any(level == "ERROR" and "placeholder" in message for level, _, message in findings)


def test_marketing_filler_is_error(tmp_path: Path) -> None:
    findings = findings_for(write_skill(tmp_path, "This is a revolutionary solution."))
    assert any(level == "ERROR" and "marketing filler" in message for level, _, message in findings)


def test_unsupported_absolute_is_warning(tmp_path: Path) -> None:
    findings = findings_for(write_skill(tmp_path, "This guarantees correct results."))
    assert any(level == "WARN" and "absolute claim" in message for level, _, message in findings)


def test_code_block_is_not_scanned_for_filler(tmp_path: Path) -> None:
    fence = chr(96) * 3
    findings = findings_for(write_skill(tmp_path, fence + "text\nTODO: literal fixture\n" + fence))
    assert not findings


def test_lowercase_todo_lifecycle_state_is_allowed(tmp_path: Path) -> None:
    findings = findings_for(write_skill(tmp_path, "Kanban lifecycle state: todo -> in_progress"))
    assert not any(level == "ERROR" and "placeholder" in message for level, _, message in findings)


def test_changed_skill_files_include_renames(monkeypatch, tmp_path: Path) -> None:
    import tools.check_antislop as checker

    repo_root = tmp_path / "repo"
    skill_path = repo_root / "skills" / "renamed.md"
    skill_path.parent.mkdir(parents=True)
    skill_path.write_text("# Renamed skill\n", encoding="utf-8")
    monkeypatch.setattr(checker, "REPO_ROOT", repo_root)
    calls: list[list[str]] = []

    def fake_check_output(command, **kwargs):
        calls.append(command)
        return "skills/renamed.md\n"

    monkeypatch.setattr(checker.subprocess, "check_output", fake_check_output)
    assert checker.changed_skill_files("origin/main") == [skill_path]
    assert "--diff-filter=AMR" in calls[0]
