"""Tests for weekly_highlights helpers (issue #719: agent-skills layout support)."""

from tools.weekly_highlights import (
    collect_skill_counts,
    is_skill_file,
    skill_display_name,
)


def test_is_skill_file_matches_both_layouts():
    assert is_skill_file("skills/03-memory/rag.md")
    assert is_skill_file("agent-skills/rag/SKILL.md")
    assert is_skill_file("agent-skills/rag/skill.md")
    assert not is_skill_file("README.md")
    assert not is_skill_file("agent-skills/rag/NOTES.txt")
    assert not is_skill_file("docs/api/skills.json")
    assert not is_skill_file("")
    assert not is_skill_file(None)


def test_skill_display_name_uses_parent_dir_for_skill_packages():
    assert skill_display_name("skills/03-memory/rag.md") == "Rag"
    assert skill_display_name(
        "agent-skills/code-dependency-auditor/SKILL.md"
    ) == "Code Dependency Auditor"
    assert skill_display_name("skills/02-reasoning/self-consistency.md") == "Self Consistency"


def test_collect_skill_counts_counts_each_touch():
    files = [
        {"filename": "agent-skills/rag/SKILL.md"},
        {"filename": "agent-skills/rag/SKILL.md"},
        {"filename": "skills/03-memory/rag.md"},
        {"filename": "README.md"},
    ]
    counts = collect_skill_counts(files)
    assert counts == {
        "agent-skills/rag/SKILL.md": 2,
        "skills/03-memory/rag.md": 1,
    }


def test_collect_skill_counts_handles_missing_or_null_filename():
    assert collect_skill_counts([{}, {"filename": None}]) == {}
