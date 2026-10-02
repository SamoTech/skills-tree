from tools.reconcile_agent_skills import desired_names

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
