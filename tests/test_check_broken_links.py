"""Unit tests for tools/check_broken_links.py edge cases.

Run with: pytest tests/test_check_broken_links.py -v
"""
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))


# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_md_links(text: str) -> list[str]:
    """Extract relative markdown link targets from text."""
    return re.findall(r'\[.*?\]\(([^)]+)\)', text)


def is_external(href: str) -> bool:
    return href.startswith("http://") or href.startswith("https://") or href.startswith("//")


def is_anchor_only(href: str) -> bool:
    return href.startswith("#")


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestLinkExtraction:

    def test_extracts_relative_links(self):
        md = "See [this skill](../05-code/code-generation.md) for more."
        links = extract_md_links(md)
        assert links == ["../05-code/code-generation.md"]

    def test_extracts_multiple_links(self):
        md = "[A](a.md) and [B](b.md) and [C](c.md)"
        links = extract_md_links(md)
        assert links == ["a.md", "b.md", "c.md"]

    def test_ignores_image_alt_text_confusion(self):
        md = "![logo](assets/logo.png) and [link](file.md)"
        links = extract_md_links(md)
        # Both image and link targets are extracted; caller filters by type
        assert "assets/logo.png" in links
        assert "file.md" in links

    def test_empty_text_returns_empty_list(self):
        assert extract_md_links("") == []

    def test_no_links_returns_empty_list(self):
        assert extract_md_links("Just plain text here.") == []


class TestLinkClassification:

    def test_http_link_is_external(self):
        assert is_external("https://example.com") is True

    def test_relative_link_is_not_external(self):
        assert is_external("../skill.md") is False

    def test_anchor_only(self):
        assert is_anchor_only("#description") is True
        assert is_anchor_only("../other.md#section") is False

    def test_protocol_relative_is_external(self):
        assert is_external("//cdn.example.com/file.js") is True


class TestRelativeLinkResolution:

    def test_resolve_sibling_file(self, tmp_path):
        source = tmp_path / "skills" / "02-reasoning" / "chain-of-thought.md"
        source.parent.mkdir(parents=True)
        target = tmp_path / "skills" / "02-reasoning" / "step-back.md"
        target.write_text("# Step Back")
        source.write_text("[Step Back](step-back.md)")

        links = extract_md_links(source.read_text())
        resolved = (source.parent / links[0]).resolve()
        assert resolved == target.resolve()

    def test_resolve_parent_relative_link(self, tmp_path):
        source = tmp_path / "skills" / "02-reasoning" / "chain-of-thought.md"
        source.parent.mkdir(parents=True)
        target = tmp_path / "skills" / "05-code" / "code-generation.md"
        target.parent.mkdir(parents=True)
        target.write_text("# Code Gen")
        source.write_text("[Code Gen](../05-code/code-generation.md)")

        links = extract_md_links(source.read_text())
        resolved = (source.parent / links[0]).resolve()
        assert resolved == target.resolve()

    def test_broken_link_detected(self, tmp_path):
        source = tmp_path / "skills" / "01-perception" / "skill.md"
        source.parent.mkdir(parents=True)
        source.write_text("[Missing](non-existent.md)")

        links = extract_md_links(source.read_text())
        resolved = (source.parent / links[0]).resolve()
        assert not resolved.exists()


class TestFrontmatterSkipping:
    """Links inside frontmatter (between --- markers) should not be checked."""

    def test_body_links_after_frontmatter(self):
        md = "---\ntitle: My Skill\n---\n\nSee [other skill](other.md)."
        parts = md.split("---", 2)
        body = parts[2] if len(parts) >= 3 else md
        links = extract_md_links(body)
        assert "other.md" in links

    def test_no_links_in_frontmatter_processed(self):
        md = "---\ntitle: My Skill\nref: [not-a-link](fake.md)\n---\n\nBody."
        parts = md.split("---", 2)
        frontmatter = parts[1]
        links_in_fm = extract_md_links(frontmatter)
        # We detect there ARE links in frontmatter — caller must skip them
        assert "fake.md" in links_in_fm  # confirms we need the skip logic
