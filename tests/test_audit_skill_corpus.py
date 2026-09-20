from pathlib import Path

from tools.audit_skill_corpus import audit_skill_files, normalize, python_syntax_errors, stale_version


def test_normalize_collapses_title_variants() -> None:
    assert normalize("API Response Parsing") == "apiresponseparsing"
    assert normalize("api-response_parsing") == "apiresponseparsing"


def test_stale_version_requires_self_declared_changelog_conflict() -> None:
    text = "## Changelog\n- v1 (2025-01): Initial\n- v2 (2026-01): Contract update\n"
    assert stale_version({"version": "v1"}, text) is True
    assert stale_version({"version": "v2"}, text) is False
    assert stale_version({"version": "v3"}, text) is False


def test_python_syntax_errors_reports_invalid_fenced_example() -> None:
    text = "```python\ndef broken(:\n    pass\n```"
    errors = python_syntax_errors(text)
    assert errors
    assert "invalid syntax" in errors[0]


def test_whole_corpus_audit_returns_one_record_per_skill() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = sorted((root / "skills").rglob("*.md"))
    paths = [path for path in paths if path.name.lower() != "readme.md"]
    records = audit_skill_files(paths)
    assert len(records) == len(paths)
    assert all(record.quality in {"battle_tested", "enriched", "stub", "invalid"} for record in records)


def test_existing_corpus_has_no_broken_python_examples() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = sorted((root / "skills").rglob("*.md"))
    paths = [path for path in paths if path.name.lower() != "readme.md"]
    records = audit_skill_files(paths)
    broken_python = [record for record in records if any(f.startswith("broken-python:") for f in record.findings)]
    assert broken_python == []
