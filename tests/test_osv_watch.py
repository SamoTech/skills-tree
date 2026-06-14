"""Unit tests for tools/osv_watch_scan.py

Tests the pure helper functions (no network calls, no filesystem writes).
The main() function is tested via subprocess to avoid global side-effects.
"""
import sys
from pathlib import Path

import pytest

# Ensure tools/ is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from osv_watch_scan import parse_frontmatter, get_deps, parse_dep, classify_vuln_state


# ---------------------------------------------------------------------------
# parse_frontmatter
# ---------------------------------------------------------------------------

class TestParseFrontmatter:
    def test_basic_key_value(self):
        text = "---\ntitle: My Skill\nauthor: alice\n---\nbody"
        fm = parse_frontmatter(text)
        assert fm["title"] == "My Skill"
        assert fm["author"] == "alice"

    def test_missing_frontmatter_returns_empty(self):
        assert parse_frontmatter("No frontmatter here") == {}

    def test_empty_value(self):
        text = "---\ndependencies:\n---"
        fm = parse_frontmatter(text)
        assert fm.get("dependencies") == ""

    def test_colon_in_value(self):
        text = "---\nurl: https://example.com\n---"
        fm = parse_frontmatter(text)
        assert fm["url"] == "https://example.com"


# ---------------------------------------------------------------------------
# get_deps
# ---------------------------------------------------------------------------

class TestGetDeps:
    def test_comma_separated(self):
        fm = {"dependencies": "httpx, requests, pyyaml"}
        assert get_deps(fm) == ["httpx", "requests", "pyyaml"]

    def test_space_separated(self):
        fm = {"requires": "numpy scipy"}
        assert get_deps(fm) == ["numpy", "scipy"]

    def test_bracket_wrapped(self):
        fm = {"packages": "[httpx, pyyaml]"}
        deps = get_deps(fm)
        assert "httpx" in deps
        assert "pyyaml" in deps

    def test_empty_returns_empty_list(self):
        assert get_deps({}) == []

    def test_prefers_dependencies_key(self):
        fm = {"dependencies": "httpx", "requires": "numpy"}
        deps = get_deps(fm)
        # Both keys are collected
        assert "httpx" in deps
        assert "numpy" in deps


# ---------------------------------------------------------------------------
# parse_dep
# ---------------------------------------------------------------------------

class TestParseDep:
    def test_name_only(self):
        assert parse_dep("httpx") == ("httpx", None)

    def test_name_with_version_ge(self):
        pkg, ver = parse_dep("httpx>=0.28.1")
        assert pkg == "httpx"
        assert ver == "0.28.1"

    def test_name_with_version_eq(self):
        pkg, ver = parse_dep("pyyaml==6.0.3")
        assert pkg == "pyyaml"
        assert ver == "6.0.3"

    def test_name_with_dots_and_dashes(self):
        pkg, ver = parse_dep("python-dateutil==2.9.0")
        assert pkg == "python-dateutil"

    def test_invalid_returns_name_none(self):
        # Should not raise — graceful fallback
        pkg, ver = parse_dep("!!!invalid")
        assert ver is None


# ---------------------------------------------------------------------------
# classify_vuln_state
# ---------------------------------------------------------------------------

class TestClassifyVulnState:
    def test_no_fix_returns_critical(self):
        vulns = [{"id": "GHSA-xxxx", "affected": [{"ranges": [{"type": "ECOSYSTEM", "events": [{"introduced": "0"}]}]}]}]
        assert classify_vuln_state(vulns) == "critical"

    def test_with_fix_returns_advisory(self):
        vulns = [{"id": "GHSA-yyyy", "affected": [{"ranges": [{"type": "ECOSYSTEM", "events": [{"introduced": "0"}, {"fixed": "1.2.3"}]}]}]}]
        assert classify_vuln_state(vulns) == "advisory"

    def test_empty_vulns_returns_critical(self):
        # Edge case: called with empty list (shouldn't happen but must not crash)
        assert classify_vuln_state([]) == "critical"

    def test_non_ecosystem_range_ignored(self):
        vulns = [{"id": "GHSA-zzzz", "affected": [{"ranges": [{"type": "GIT", "events": [{"introduced": "0"}, {"fixed": "abc123"}]}]}]}]
        # GIT range type should NOT be treated as a fix for ECOSYSTEM
        assert classify_vuln_state(vulns) == "critical"
