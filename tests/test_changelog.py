"""Unit tests for tools/generate_changelog.py

Tests all pure functions and main() via monkeypatching.
No filesystem writes — all file I/O is mocked.
"""
import sys
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

import generate_changelog


# ---------------------------------------------------------------------------
# Pattern matching
# ---------------------------------------------------------------------------

class TestPatternMatching:
    """Verify PR title classification logic."""

    @pytest.mark.parametrize("title,expected_type", [
        ("feat: add new perception skill", "Added"),
        ("FEAT: Add Something", "Added"),          # case-insensitive
        ("fix: correct broken link", "Fixed"),
        ("improve: faster badge sync", "Improved"),
        ("deprecate: remove old format", "Deprecated"),
    ])
    def test_known_patterns(self, title, expected_type):
        import re
        for pattern, ctype in generate_changelog.PATTERNS:
            m = re.match(pattern, title, re.IGNORECASE)
            if m:
                assert ctype == expected_type
                return
        pytest.fail(f"No pattern matched title: {title!r}")

    @pytest.mark.parametrize("title", [
        "chore: update deps",
        "docs: fix typo",
        "refactor: cleanup",
        "",
        "random PR title with no prefix",
    ])
    def test_unmatched_titles_produce_no_entry(self, title):
        import re
        for pattern, _ in generate_changelog.PATTERNS:
            if re.match(pattern, title, re.IGNORECASE):
                pytest.fail(f"Title {title!r} should NOT match but did")


# ---------------------------------------------------------------------------
# main() — env var validation
# ---------------------------------------------------------------------------

class TestMainEnvValidation:
    def _env(self, **kwargs):
        base = {
            "PR_TITLE": "feat: add skill",
            "PR_NUMBER": "42",
            "PR_AUTHOR": "alice",
            "PR_URL": "https://github.com/SamoTech/skills-tree/pull/42",
            "MERGED_AT": "2026-06-14T10:00:00Z",
        }
        base.update(kwargs)
        return base

    def test_missing_pr_title_exits_1(self):
        with patch.dict("os.environ", {"PR_TITLE": "", "PR_NUMBER": "", "PR_AUTHOR": "", "PR_URL": "", "MERGED_AT": ""}, clear=True):
            with pytest.raises(SystemExit) as exc:
                generate_changelog.main()
            assert exc.value.code == 1

    def test_unmatched_title_exits_0(self):
        env = self._env(PR_TITLE="chore: update deps")
        with patch.dict("os.environ", env, clear=True):
            with pytest.raises(SystemExit) as exc:
                generate_changelog.main()
            assert exc.value.code == 0

    def test_missing_pr_number_exits_1(self):
        env = self._env(PR_NUMBER="")
        with patch.dict("os.environ", env, clear=True):
            with patch("generate_changelog.CHANGELOG") as mock_path:
                mock_path.exists.return_value = False
                with pytest.raises(SystemExit) as exc:
                    generate_changelog.main()
                assert exc.value.code == 1

    def test_success_writes_entry(self, tmp_path):
        env = self._env()
        changelog = tmp_path / "CHANGELOG.md"
        with patch.dict("os.environ", env, clear=True):
            with patch.object(generate_changelog, "CHANGELOG", changelog):
                generate_changelog.main()
        content = changelog.read_text()
        assert "feat: add skill" in content or "Added" in content
        assert "alice" in content
        assert "#42" in content
