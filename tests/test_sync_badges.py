"""Unit tests for tools/sync_badges.py"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from sync_badges import skill_to_badge_key, UNSCANNED_BADGE, main


class TestSkillToBadgeKey:
    def test_nested_path(self):
        key = skill_to_badge_key(Path("skills/01-perception/vision.md"))
        assert key == "skills-01-perception-vision"

    def test_root_path(self):
        key = skill_to_badge_key(Path("skills/tool-use.md"))
        assert key == "skills-tool-use"

    def test_no_md_extension_in_key(self):
        key = skill_to_badge_key(Path("skills/foo.md"))
        assert not key.endswith(".md")


class TestUnscannedBadge:
    def test_has_required_shields_fields(self):
        assert UNSCANNED_BADGE["schemaVersion"] == 1
        assert "label" in UNSCANNED_BADGE
        assert "message" in UNSCANNED_BADGE
        assert UNSCANNED_BADGE["message"] == "unscanned"


class TestMain:
    def test_creates_missing_badges(self, tmp_path):
        skills = tmp_path / "skills" / "01-cat"
        skills.mkdir(parents=True)
        (skills / "foo.md").write_text("# foo")
        badges = tmp_path / "docs" / "badges"

        import sync_badges as sb
        orig_skills = sb.SKILLS_ROOT
        orig_badges = sb.BADGE_DIR
        sb.SKILLS_ROOT = tmp_path / "skills"
        sb.BADGE_DIR = badges

        try:
            main()
        finally:
            sb.SKILLS_ROOT = orig_skills
            sb.BADGE_DIR = orig_badges

        created = list(badges.glob("*.json"))
        assert len(created) == 1
        data = json.loads(created[0].read_text())
        assert data["message"] == "unscanned"

    def test_removes_orphan_badges(self, tmp_path):
        skills = tmp_path / "skills"
        skills.mkdir()
        badges = tmp_path / "docs" / "badges"
        badges.mkdir(parents=True)
        orphan = badges / "orphan-skill.json"
        orphan.write_text(json.dumps(UNSCANNED_BADGE))

        import sync_badges as sb
        orig_skills = sb.SKILLS_ROOT
        orig_badges = sb.BADGE_DIR
        sb.SKILLS_ROOT = skills
        sb.BADGE_DIR = badges

        try:
            main()
        finally:
            sb.SKILLS_ROOT = orig_skills
            sb.BADGE_DIR = orig_badges

        assert not orphan.exists()
