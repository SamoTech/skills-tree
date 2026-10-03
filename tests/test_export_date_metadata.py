from __future__ import annotations

from tools.export_skills import build_index


def test_kanban_date_metadata_is_exportable_without_cross_field_contamination():
    item = next(skill for skill in build_index() if skill["id"] == "kanban-task-management")
    assert item["added"] == "2026-10"
    assert item["last_updated"] == "2026-10"
