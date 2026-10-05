from pathlib import Path

from registry.runtime import UniversalRegistry
from registry.skill_selection import SkillSelectionEngine
from tools.architect import SkillsGraph


ROOT = Path(__file__).resolve().parents[1]


def engine():
    return SkillSelectionEngine(
        UniversalRegistry(ROOT / "registry" / "universal_registry.json"),
        SkillsGraph(ROOT / "data" / "SKILLS_GRAPH.json"),
    )


def test_selects_capability_match_over_unrelated_candidate():
    result = engine().select(
        "retrieve knowledge",
        ["capability/knowledge-retrieval"],
        ["03-memory/rag", "05-code/code-review"],
    )
    assert result["selected_skill"]["id"] == "03-memory/rag"
    assert result["next_action"]["type"] == "invoke"


def test_selects_code_quality_skill_over_unrelated_candidate():
    result = engine().select(
        "review code",
        ["capability/code-quality"],
        ["05-code/code-review", "11-web/web-search"],
    )
    assert result["selected_skill"]["id"] == "05-code/code-review"


def test_selects_web_retrieval_skill_over_unrelated_candidate():
    result = engine().select(
        "search web",
        ["capability/web-retrieval"],
        ["11-web/web-search", "05-code/code-review"],
    )
    assert result["selected_skill"]["id"] == "11-web/web-search"


def test_unknown_candidate_fails_closed():
    result = engine().select(
        "agentic retrieval",
        ["capability/knowledge-retrieval"],
        ["09-agentic-patterns/agentic-rag", "03-memory/rag"],
    )
    assert result["status"] == "BLOCKED"
    assert result["next_action"]["type"] == "escalate"


def test_failure_without_recovery_candidate_blocks():
    result = engine().next_after_failure(
        "review code",
        ["capability/code-quality"],
        ["05-code/code-review"],
        "05-code/code-review",
    )
    assert result["status"] == "BLOCKED"
    assert result["next_action"]["type"] == "escalate"


def test_no_candidate_covers_required_capability():
    result = engine().select(
        "search web",
        ["capability/web-retrieval"],
        ["05-code/code-review"],
    )
    assert result["status"] == "BLOCKED"
    assert result["next_action"]["type"] == "escalate"
