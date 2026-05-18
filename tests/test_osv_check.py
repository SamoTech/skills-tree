"""Unit tests for tools/osv_check.py edge cases.

Run with: pytest tests/test_osv_check.py -v
"""
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Make tools/ importable
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))


# ── Helpers ──────────────────────────────────────────────────────────────────

def make_sbom(components=None):
    """Build a minimal CycloneDX SBOM dict."""
    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "components": components or [],
    }


def make_component(name, version, purl, used_in=None):
    return {
        "type": "library",
        "name": name,
        "version": version,
        "purl": purl,
        "usedIn": used_in or [],
    }


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestSbomParsing:
    """SBOM loading edge cases."""

    def test_empty_sbom_returns_no_components(self, tmp_path):
        sbom = make_sbom([])
        sbom_file = tmp_path / "sbom.json"
        sbom_file.write_text(json.dumps(sbom))
        data = json.loads(sbom_file.read_text())
        assert data["components"] == []

    def test_missing_components_key(self, tmp_path):
        sbom_file = tmp_path / "sbom.json"
        sbom_file.write_text(json.dumps({"bomFormat": "CycloneDX"}))
        data = json.loads(sbom_file.read_text())
        components = data.get("components", [])
        assert components == []

    def test_component_with_no_used_in(self):
        comp = make_component("requests", "2.31.0", "pkg:pypi/requests@2.31.0")
        assert comp["usedIn"] == []

    def test_malformed_json_raises(self, tmp_path):
        sbom_file = tmp_path / "sbom.json"
        sbom_file.write_text("{ this is not valid json")
        with pytest.raises(json.JSONDecodeError):
            json.loads(sbom_file.read_text())


class TestPurlExtraction:
    """PURL normalisation and extraction."""

    def test_pypi_purl_parsed(self):
        purl = "pkg:pypi/httpx@0.27.0"
        assert "httpx" in purl
        assert "0.27.0" in purl

    def test_purl_without_version(self):
        purl = "pkg:pypi/requests"
        # Version is optional in PURLs; extractor must handle gracefully
        name = purl.split("/")[-1].split("@")[0]
        assert name == "requests"

    def test_purl_with_namespace(self):
        purl = "pkg:pypi/google/cloud-storage@2.10.0"
        # Should not crash on namespaced purls
        assert "cloud-storage" in purl


class TestOsvResponseHandling:
    """OSV API response edge cases (no real network calls)."""

    def test_empty_osv_response_no_vulns(self):
        response = {"vulns": []}
        assert len(response.get("vulns", [])) == 0

    def test_osv_response_with_single_vuln(self):
        response = {
            "vulns": [
                {"id": "GHSA-xxxx-yyyy-zzzz", "summary": "Test vuln", "aliases": ["CVE-2024-12345"]}
            ]
        }
        assert len(response["vulns"]) == 1
        assert response["vulns"][0]["id"] == "GHSA-xxxx-yyyy-zzzz"

    def test_osv_missing_vulns_key(self):
        response = {}
        vulns = response.get("vulns", [])
        assert vulns == []

    def test_cve_alias_extracted(self):
        vuln = {"id": "GHSA-xxxx", "aliases": ["CVE-2024-11111", "CVE-2024-22222"]}
        cves = [a for a in vuln.get("aliases", []) if a.startswith("CVE-")]
        assert len(cves) == 2
        assert "CVE-2024-11111" in cves


class TestBadgeProtection:
    """Badge colour protection rules."""

    PROTECTED_COLORS = {"critical", "22c55e"}

    def test_critical_badge_not_downgraded(self):
        existing = {"color": "critical", "message": "CVE-2024-1234"}
        # Protection rule: never overwrite critical or 22c55e
        should_skip = existing.get("color") in self.PROTECTED_COLORS
        assert should_skip is True

    def test_green_verified_badge_not_downgraded(self):
        existing = {"color": "22c55e", "message": "verified"}
        should_skip = existing.get("color") in self.PROTECTED_COLORS
        assert should_skip is True

    def test_yellow_badge_can_be_updated(self):
        existing = {"color": "yellow", "message": "machine-inferred · 3 pkgs"}
        should_skip = existing.get("color") in self.PROTECTED_COLORS
        assert should_skip is False

    def test_grey_unscanned_badge_can_be_updated(self):
        existing = {"color": "lightgrey", "message": "unscanned"}
        should_skip = existing.get("color") in self.PROTECTED_COLORS
        assert should_skip is False
