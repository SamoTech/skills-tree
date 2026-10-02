from pathlib import Path

from tools.generate_agent_skills import audit, project, clean_description, normalize_name


def write_skill(root: Path, rel: str, content: str) -> Path:
    path = root / "skills" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_name_and_description_are_deterministic(tmp_path):
    source = write_skill(
        tmp_path,
        "01-test/My Skill.md",
        """---
title: "My Skill"
description: "A useful skill."
version: v2
---

# My Skill

## Evidence

- Authoritative test evidence
""",
    )
    first = project(source, tmp_path)
    second = project(source, tmp_path)
    assert first.name == "my-skill"
    assert first.description == "A useful skill."
    assert first.eligible
    assert first.content == second.content
    assert "source: skills/01-test/My Skill.md" in first.content
    assert 'version: "v2"' in first.content


def test_badges_are_removed_from_machine_description():
    assert (
        clean_description("[![status](badge.svg)](https://example.test) Real description.")
        == "Real description."
    )


def test_audit_reports_missing_evidence_and_collisions(tmp_path):
    write_skill(
        tmp_path,
        "01-test/First.md",
        """---
description: "Same"
---

# First
""",
    )
    write_skill(
        tmp_path,
        "02-test/first.md",
        """---
description: "Same"
---

# Second

## Evidence

- Evidence
""",
    )
    report = audit(tmp_path)
    assert report["total"] == 2
    assert report["blocked"] == 1
    assert "missing Evidence section" in report["blockers"]["skills/01-test/First.md"]
    assert "first" in report["name_collisions"]

 
 
def test_audit_excludes_category_readmes(tmp_path):
    write_skill(tmp_path, "01-test/README.md", "# Category README")
    write_skill(
        tmp_path,
        "01-test/real-skill.md",
        """---
description: "Real skill."
---

# Real

## Evidence

- Evidence
""",
    )
    report = audit(tmp_path)
    assert report["total"] == 1
    assert report["eligible"] == 1


def test_generated_name_rejects_consecutive_hyphens(tmp_path):
    source = write_skill(
        tmp_path,
        "01-test/foo--bar.md",
        """---
description: "A valid description."
---

# Foo

## Evidence

- Evidence
""",
    )
    assert "invalid generated name" in project(source, tmp_path).blockers
