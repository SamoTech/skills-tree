"""Regression gate for public trust claims (issue #730).

Derives the public skill count from the canonical quality report (itself
freshness-gated against the canonical skills/ registry), and asserts that the
public-facing claims surfaces (README, docs pages) carry no contradictory or
unsupported claims of the classes confirmed in the 2026-11-27 external
assessment remediation:

- Python API availability claims (historical skills_tree.SkillsTree is NOT
  implemented; docs/api.md is the verified boundary).
- Public skill count consistency (2489 total files = 2488 public + 1 fixture).
- Roadmap scale targets that the registry has already passed ("500+ skills").
- Benchmark claim accuracy: every linked benchmark page must exist, numeric
  margins must appear in the linked source document, and margin wording must
  use percentage points.
- Documented CLI commands must exist in docs/cli.md.

These are deliberately narrow, generated-surface checks. They never weaken
existing quality/security/governance gates.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _public_skill_count() -> int:
    """Public skills = quality-report total files minus intentional fixtures.

    meta/QUALITY-REPORT.md is auto-generated from the canonical skills/ tree by
    tools/check_skill_quality.py and freshness-gated by
    tests/test_quality_report_freshness.py, so it is a deterministic function
    of the canonical registry.
    """
    qr = _read("meta/QUALITY-REPORT.md")
    total = int(re.search(r"\*\*Total skill files:\*\*\s*(\d+)", qr).group(1))
    fixture = int(re.search(r"\*\*Test fixture\*\*[^:]*:\s*(\d+)", qr).group(1))
    return total - fixture


def test_readme_hero_count_matches_canonical_registry() -> None:
    n = _public_skill_count()
    readme = _read("README.md")
    assert f"{n} Public Skills" in readme
    index = _read("docs/index.md")
    assert f"{n} Skills" in index


def test_no_unexplained_alternate_skill_counts() -> None:
    n = _public_skill_count()
    for rel in ("README.md", "docs/index.md"):
        text = _read(rel)
        for line in text.split("\n"):
            for m in re.finditer(r"\b2,?4[89]\d\b", line):
                shown = int(m.group(0).replace(",", ""))
                if shown == n:
                    continue
                assert "fixture" in line.lower(), (
                    f"{rel}: bare alternate count {shown} without fixture explanation: {line[:160]}"
                )


def test_no_contradictory_python_api_claims() -> None:
    readme = _read("README.md")
    assert "| CLI + Python API | ✅ Both |" not in readme
    for line in readme.split("\n"):
        if "Python API" in line or "skills_tree." in line:
            assert re.search(r"planned|not currently implemented|not implemented|Not yet|docs/api\.md|\*", line, re.IGNORECASE), (
                f"README Python-API line without an honest status marker: {line[:160]}"
            )
    assert "does not contain a verified implementation" in _read("docs/api.md")


def test_roadmap_scale_targets_retired() -> None:
    for rel in ("README.md", "docs/roadmap.md"):
        text = _read(rel)
        assert "500+" not in text, f"{rel}: retired '500+' scale target still present"
        assert "1000+ skills" not in text, f"{rel}: retired '1000+ skills' scale target still present"


def _readme_benchmark_rows() -> list[tuple[str, str, str]]:
    """(name, margin, relative link) rows of the README Benchmarks table."""
    readme = _read("README.md")
    section = readme.split("## 📊 Benchmarks", 1)[1]
    rows = []
    for line in section.split("\n"):
        if not line.startswith("| ") or "[→](" not in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        m = re.search(r"\]\(([^)]+)\)", cells[3])
        rows.append((cells[0], cells[2], m.group(1)))
    return rows


def test_readme_benchmark_links_exist_and_margins_match_source() -> None:
    for name, margin, link in _readme_benchmark_rows():
        target = ROOT / link
        assert target.is_file(), f"README benchmark row '{name}' links missing file: {link}"
        source = target.read_text(encoding="utf-8")
        for num in re.findall(r"\d+(?:\.\d+)?", margin):
            assert num in source, (
                f"README benchmark row '{name}' margin '{margin}': number {num} not found in {link}"
            )
        if re.search(r"\d", margin):
            assert "points" in margin, (
                f"README benchmark row '{name}' must express margins as percentage points: '{margin}'"
            )


def test_benchmark_pages_winner_claims_match_sources() -> None:
    db = _read("docs/benchmarks.md")
    assert "Claude 3.7" not in db, "docs/benchmarks.md still names a model absent from its source document"
    assert "ToolBench" not in db, "docs/benchmarks.md still claims a dataset its source document does not use"
    fc = _read("benchmarks/tool-use/function-calling-comparison.md")
    assert "Claude Opus 4.5" in fc and "Claude Opus 4.5" in db
    br = _read("benchmarks/README.md")
    for m in re.finditer(r"\]\(([a-zA-Z0-9_./-]+\.md)\)", br):
        target = ROOT / "benchmarks" / m.group(1)
        assert target.is_file(), f"benchmarks/README.md links missing file: {m.group(1)}"


def test_documented_cli_commands_exist_in_cli_reference() -> None:
    cli = _read("docs/cli.md")
    documented = set(re.findall("^## " + BT + "skills-tree (\\w[\\w-]*)" + BT, cli, re.MULTILINE))
    assert {"search", "recommend", "blueprint", "goals", "skills", "validate"} <= documented
    for rel in ("README.md", "docs/quickstart.md"):
        for cmd in set(re.findall("skills-tree ([a-z][a-z-]*)", _read(rel))):
            assert cmd in documented, f"{rel}: documents 'skills-tree {cmd}' which is absent from docs/cli.md"
