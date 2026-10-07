from pathlib import Path

from tools.build_search_index import build_index as build_search_index
from tools.export_skills import build_index as build_export_index
from tools.skill_corpus import (
    is_public_category,
    is_public_skill_path,
    iter_public_skill_files,
)


def test_sandbox_category_is_not_public():
    assert not is_public_category("00-sandbox")
    assert is_public_category("01-perception")


def test_public_skill_iterator_excludes_sandbox_fixture():
    root = Path("skills")
    paths = iter_public_skill_files(root)
    relative = {p.relative_to(root).as_posix() for p in paths}

    assert "00-sandbox/pipeline-test.md" not in relative
    assert "05-code/code-review.md" in relative


def test_public_skill_path_boundary_is_explicit():
    root = Path("skills")

    assert not is_public_skill_path(
        root / "00-sandbox/pipeline-test.md", root
    )
    assert is_public_skill_path(
        root / "05-code/code-review.md", root
    )


def test_export_projection_excludes_sandbox_fixture():
    entries = build_export_index()
    paths = {entry["path"] for entry in entries}
    assert "skills/00-sandbox/pipeline-test.md" not in paths


def test_search_projection_excludes_sandbox_fixture():
    entries = build_search_index(Path("skills"))
    ids = {entry["id"] for entry in entries}
    assert "00-sandbox/pipeline-test" not in ids
    assert "05-code/code-review" in ids
