import re
from pathlib import Path

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


def test_update_skill_count_workflow_has_single_readme_writer():
    workflow = (
        ROOT / ".github/workflows/update-skill-count.yml"
    ).read_text(encoding="utf-8")

    assert "python3 tools/update_readme_counts.py" in workflow
    assert "git add README.md" in workflow
    assert "docs/index.html" not in workflow
    assert "steps.count.outputs" not in workflow
    assert "find skills/" not in workflow
