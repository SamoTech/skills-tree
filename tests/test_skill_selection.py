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


def test_routes_missing_prerequisite_before_dependent_skill():
    result = engine().select(
        "run agentic retrieval",
        ["capability/knowledge-retrieval"],
        ["09-agentic-patterns/agentic-rag"],
    )
    assert result["selected_skill"]["id"] == "09-agentic-patterns/agentic-rag"
    assert result["next_action"] == {
        "type": "invoke_prerequisite",
        "skill_id": "03-memory/rag",
    }


def test_invokes_dependent_skill_after_prerequisites_complete():
    result = engine().select(
        "run agentic retrieval",
        ["capability/knowledge-retrieval"],
        ["09-agentic-patterns/agentic-rag"],
        completed_skills=["03-memory/rag", "09-agentic-patterns/react"],
    )
    assert result["next_action"]["type"] == "invoke"


def test_failure_without_recovery_candidate_blocks():
    result = engine().next_after_failure(
        "review code",
        ["capability/code-quality"],
        ["05-code/code-review"],
        "05-code/code-review",
    )
    assert result["status"] == "BLOCKED"
    assert result["next_action"]["type"] == "escalate"
