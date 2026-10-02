from tools.reconcile_agent_skills import desired_names, reconcile

def test_collision_names_are_deterministic():
    records = [
        {"source": "skills/07-tool-use/web-search.md", "id": "web-search", "base_name": "web-search", "category": "tool-use", "category_dir": "07-tool-use"},
        {"source": "skills/11-web/web-search.md", "id": "web-search", "base_name": "web-search", "category": "web", "category_dir": "11-web"},
    ]
    desired, collisions = desired_names(records)
    assert collisions == {"web-search": [r["source"] for r in records]}
    assert desired["skills/07-tool-use/web-search.md"] == "tool-use-web-search"
    assert desired["skills/11-web/web-search.md"] == "web-web-search"


from tools.reconcile_agent_skills import parse_frontmatter


def test_nested_metadata_source_is_parsed():
    fm = parse_frontmatter("""---
name: example
metadata:
  source: skills/01-test/example.md
  version: "v2"
---
""")
    assert fm["source"] == "skills/01-test/example.md"


def test_reconcile_prefers_provenance_over_package_name(tmp_path):
    canonical = tmp_path / "skills" / "04-action-execution"
    canonical.mkdir(parents=True)
    (canonical / "clipboard-ops.md").write_text(
        "# Clipboard Ops\n\n## Evidence\n\n- Evidence\n", encoding="utf-8"
    )
    package = tmp_path / "agent-skills" / "clipboard-operations"
    package.mkdir(parents=True)
    (package / "SKILL.md").write_text(
        """---
name: clipboard-operations
description: Clipboard operations.
metadata:
  source: skills/04-action-execution/clipboard-ops.md
---
# Clipboard Operations
""",
        encoding="utf-8",
    )
    report = reconcile(tmp_path)
    assert report["matched_by_provenance"][0]["package"] == "clipboard-operations"
    assert report["rename_needed"][0]["expected_package"] == "clipboard-ops"
    assert report["extra"] == []


def test_legacy_collision_aliases_have_explicit_sources(tmp_path):
    package = tmp_path / "agent-skills" / "web-search"
    package.mkdir(parents=True)
    (package / "SKILL.md").write_text(
        """---
name: web-search
description: Web search.
---
## Evidence
See the canonical tool.
""",
        encoding="utf-8",
    )
    report = reconcile(tmp_path)
    assert report["extra"] == []
