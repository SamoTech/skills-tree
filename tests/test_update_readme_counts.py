import re
from pathlib import Path

import pytest

from tools.update_readme_counts import README, SKILLS_DIR, gather_counts, patch_text

ROOT = Path(__file__).resolve().parents[1]


def test_count_authority_excludes_sandbox_from_public_totals():
    counts = gather_counts()
    sandbox_files = [
        p for p in (SKILLS_DIR / "00-sandbox").glob("*.md")
        if p.name.lower() != "readme.md"
    ]
    all_skill_files = [
        p for p in SKILLS_DIR.rglob("*.md")
        if p.name.lower() != "readme.md"
    ]

    assert "00-sandbox" not in counts["by_cat"]
    assert counts["categories"] == len(counts["by_cat"])
    assert counts["total"] == len(all_skill_files) - len(sandbox_files)
    assert isinstance(counts["graph_edges"], int)
    assert counts["graph_edges"] > 0


def test_readme_category_heading_is_derived_from_same_count_authority():
    counts = gather_counts()
    source = README.read_text(encoding="utf-8")
    source = re.sub(
        r"^## 🗂️ The \d+ Skill Categories$",
        "## 🗂️ The 999 Skill Categories",
        source,
        flags=re.MULTILINE,
    )

    patched = patch_text(source, counts)

    assert f"## 🗂️ The {counts['categories']} Skill Categories" in patched
    assert "## 🗂️ The 999 Skill Categories" not in patched


def test_hero_stat_strip_is_patched_from_live_counts():
    counts = gather_counts()
    source = README.read_text(encoding="utf-8")
    source = re.sub(
        r"\| \d+ Public Skills \| \d+ Graph Edges \|",
        "| 999 Public Skills | 999 Graph Edges |",
        source,
        count=1,
    )

    patched = patch_text(source, counts)

    hero = f"| {counts['total']} Public Skills | {counts['graph_edges']} Graph Edges |"
    assert hero in patched
    assert "999 Public Skills" not in patched
    assert f"✅ {counts['total']} public skills" in patched
    whats_inside = (
        f"→ {counts['total']} public skills "
        f"({counts['total'] + 1} quality-corpus files "
        "including one sandbox fixture)"
    )
    assert whats_inside in patched


def test_patch_text_raises_when_anchors_are_missing():
    counts = gather_counts()

    with pytest.raises(RuntimeError):
        patch_text("This document has no README stat anchors at all.", counts)


def test_update_skill_count_workflow_has_single_readme_writer():
    workflow = (
        ROOT / ".github/workflows/update-skill-count.yml"
    ).read_text(encoding="utf-8")

    assert "python3 tools/update_readme_counts.py" in workflow
    assert "git add README.md" in workflow
    assert "docs/index.html" not in workflow
    assert "steps.count.outputs" not in workflow
    assert "find skills/" not in workflow


def test_committed_readme_is_at_live_counts():
    counts = gather_counts()
    source = README.read_text(encoding="utf-8")
    assert patch_text(source, counts) == source, (
        "README.md skill-count anchors are stale relative to the live "
        "corpus; run python3 tools/update_readme_counts.py and commit "
        "the result (or merge the pending count automation PR)"
    )


def test_index_hero_card_and_search_comment_are_patched_from_live_counts():
    from tools.update_readme_counts import INDEX_MD, patch_index_text

    counts = gather_counts()
    source = INDEX_MD.read_text(encoding="utf-8")
    source = re.sub(r"— \d+\+? skills, versioned", "— 9999 skills, versioned", source, count=1)
    source = re.sub(r"\*\*\d+\+? Skills\*\*", "**9999 Skills**", source, count=1)
    source = re.sub(r"# search across \d+\+? skills", "# search across 9999 skills", source, count=1)

    patched = patch_index_text(source, counts)

    assert f"— {counts['total']} skills, versioned" in patched
    assert f"**{counts['total']} Skills**" in patched
    assert f"# search across {counts['total']} skills" in patched
    assert "9999" not in patched


def test_committed_docs_index_is_at_live_counts():
    from tools.update_readme_counts import INDEX_MD, patch_index_text

    counts = gather_counts()
    source = INDEX_MD.read_text(encoding="utf-8")
    assert patch_index_text(source, counts) == source, (
        "docs/index.md (the Pages landing page) skill counts are stale "
        "relative to the live corpus; run python3 "
        "tools/update_readme_counts.py and commit the result"
    )


def test_count_workflow_stages_docs_index_next_to_readme():
    workflow = (
        ROOT / ".github/workflows/update-skill-count.yml"
    ).read_text(encoding="utf-8")

    assert "git add README.md docs/index.md" in workflow
