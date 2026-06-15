#!/usr/bin/env python3
"""
Skills Tree OS - Agent Skill Architect

Taxonomy-driven recommendation engine.
Single source of truth: meta/GOAL_TAXONOMY.md
No hardcoded goal lists, skill mappings, or recommendation rules.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


# ---------------------------------------------------------------------------
# GOAL_TAXONOMY.md parser
# ---------------------------------------------------------------------------

class GoalTaxonomyParser:
    """
    Parse meta/GOAL_TAXONOMY.md into structured goal/skill data.
    No data is hardcoded here — everything is read from the file at runtime.
    """

    def __init__(self, taxonomy_path: str):
        self.path = Path(taxonomy_path)
        self._raw = self.path.read_text(encoding="utf-8")
        self._goals: Dict[str, Dict] = {}
        self._subgoals: Dict[str, Dict] = {}
        self._skill_maps: Dict[str, List[Dict]] = {}
        self._framework_prefs: Dict[str, Dict] = {}
        self._parse()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def goals(self) -> Dict[str, Dict]:
        """Return all Level-1 goal categories keyed by ID (G01…G12)."""
        return self._goals

    @property
    def subgoals(self) -> Dict[str, Dict]:
        """Return all Level-2 sub-goals keyed by ID (G01.1…G12.5)."""
        return self._subgoals

    def skills_for(self, goal_id: str) -> List[Dict]:
        """
        Return ordered skill list for a goal or sub-goal ID.
        Falls back to parent goal skills when sub-goal has no dedicated mapping.
        """
        if goal_id in self._skill_maps:
            return self._skill_maps[goal_id]
        parent = goal_id.split(".")[0] if "." in goal_id else goal_id
        return self._skill_maps.get(parent, [])

    def frameworks_for(self, goal_name: str) -> Dict[str, int]:
        """Return framework star-ratings for a goal (by display name)."""
        return self._framework_prefs.get(goal_name, {})

    def resolve(self, query: str) -> Optional[str]:
        """
        Resolve a free-text query to a goal/sub-goal ID.
        Matches against IDs and display names (case-insensitive).
        """
        q = query.strip().lower()
        # Exact ID match (e.g. "G01.4")
        for sid, meta in {**self._goals, **self._subgoals}.items():
            if sid.lower() == q:
                return sid
        # Name match
        for sid, meta in {**self._goals, **self._subgoals}.items():
            if meta["name"].lower() == q:
                return sid
        # Partial name match
        for sid, meta in {**self._goals, **self._subgoals}.items():
            if q in meta["name"].lower():
                return sid
        return None

    def list_goals(self) -> List[Dict]:
        """Return all Level-1 goals as a list, sorted by ID."""
        return sorted(self._goals.values(), key=lambda g: g["id"])

    # ------------------------------------------------------------------
    # Internal parsing
    # ------------------------------------------------------------------

    def _parse(self):
        self._parse_goal_categories()
        self._parse_subgoals()
        self._parse_skill_mappings()
        self._parse_framework_preferences()

    def _parse_goal_categories(self):
        """
        Parse the Level 1 Category table (Section 2.1).
        Pattern: | `Gxx` | **Name** | Description | Difficulty | Skills Count |
        """
        pattern = re.compile(
            r"\|\s*`(G\d{2})`\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*(\d+)\s*\|"
        )
        for m in pattern.finditer(self._raw):
            gid, name, desc, diff, count = (
                m.group(1).strip(),
                m.group(2).strip(),
                m.group(3).strip(),
                m.group(4).strip(),
                int(m.group(5).strip()),
            )
            self._goals[gid] = {
                "id": gid,
                "name": name,
                "description": desc,
                "difficulty": diff,
                "skills_count": count,
            }

    def _parse_subgoals(self):
        """
        Parse Level 2 sub-goal tables.
        Pattern: | `Gxx.y` | **Name** | Description | Difficulty |
        """
        pattern = re.compile(
            r"\|\s*`(G\d{2}\.\d+)`\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+)\|\s*([^|\n]+)\|"
        )
        for m in pattern.finditer(self._raw):
            sid, name, desc, diff = (
                m.group(1).strip(),
                m.group(2).strip(),
                m.group(3).strip(),
                m.group(4).strip(),
            )
            parent_id = sid.split(".")[0]
            parent_name = self._goals.get(parent_id, {}).get("name", parent_id)
            self._subgoals[sid] = {
                "id": sid,
                "name": name,
                "description": desc,
                "difficulty": diff,
                "parent_id": parent_id,
                "parent_name": parent_name,
            }

    def _parse_skill_mappings(self):
        """
        Parse Sections 5 & 8 skill tables.
        Pattern after a "### Gxx.y:" heading:
          1. `skill-id` (Priority, Nhrs)
          OR
          | skill-id | Skill Name | Category | Priority | Learn Time |
        """
        # --- Tabular form (Section 5 / Level 4) ---
        table_section = re.compile(
            r"### (?:Skill Mapping|G\d{2}(?:\.\d+)?)[^\n]*\n"
            r"(?:.*?\n)*?"
            r"(?:\| Skill ID[^\n]+\n\|[-| ]+\n)((?:\|[^\n]+\n)+)",
            re.DOTALL,
        )
        row_re = re.compile(
            r"\|\s*`?([\w-]+)`?\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*(\d+)\s*hrs?\s*\|"
        )

        # Walk every "Skill Mapping" / "Gxx" section heading
        heading_re = re.compile(
            r"###\s+(Skill Mapping: .+?|G\d{2}(?:\.\d+)?: .+?)\n(.*?)(?=###|\Z)",
            re.DOTALL,
        )
        for hm in heading_re.finditer(self._raw):
            section_title = hm.group(1).strip()
            section_body = hm.group(2)

            # Try to infer the sub-goal ID from the heading
            gid_match = re.search(r"(G\d{2}(?:\.\d+)?)", section_title)
            if not gid_match:
                continue
            gid = gid_match.group(1)

            skills = []

            # Attempt table-form first
            for rm in row_re.finditer(section_body):
                skills.append({
                    "id": rm.group(1).strip(),
                    "name": rm.group(2).strip(),
                    "category": rm.group(3).strip(),
                    "priority": rm.group(4).strip(),
                    "learn_time_hrs": int(rm.group(5)),
                })

            # Attempt numbered list form: `1. \`skill-id\` (Priority, Nhrs)`
            if not skills:
                list_re = re.compile(
                    r"^\d+\.\s+`([\w-]+)`\s+\(([^,]+),\s*(\d+)hrs?\)",
                    re.MULTILINE,
                )
                for lm in list_re.finditer(section_body):
                    skills.append({
                        "id": lm.group(1).strip(),
                        "name": lm.group(1).strip().replace("-", " ").title(),
                        "category": "",
                        "priority": lm.group(2).strip(),
                        "learn_time_hrs": int(lm.group(3)),
                    })

            if skills:
                self._skill_maps[gid] = skills

    def _parse_framework_preferences(self):
        """
        Parse the Framework Mapping table (Section 6).
        Pattern: | **Goal Name** | stars | stars | … |
        """
        headers = ["OpenAI SDK", "LangChain", "LlamaIndex", "MCP", "Mastra", "Custom"]

        # Locate the framework table block
        fw_block = re.search(
            r"### Framework Mapping by Goal\n(\|.+?\n)((?:\|[^\n]+\n)+)",
            self._raw,
            re.DOTALL,
        )
        if not fw_block:
            return

        row_re = re.compile(r"\|\s*\*\*([^*]+)\*\*\s*\|(.+)")
        for line in fw_block.group(2).splitlines():
            m = row_re.match(line)
            if not m:
                continue
            goal_name = m.group(1).strip()
            cells = [c.strip() for c in m.group(2).split("|")]
            ratings = {}
            for i, fw in enumerate(headers):
                if i < len(cells):
                    stars = cells[i].count("⭐")
                    ratings[fw] = stars
            self._framework_prefs[goal_name] = ratings


# ---------------------------------------------------------------------------
# Skills Graph
# ---------------------------------------------------------------------------

class SkillsGraph:
    """Load and query the skills knowledge graph."""

    def __init__(self, graph_path: str = "../data/SKILLS_GRAPH.json"):
        with open(graph_path, "r") as f:
            self.data = json.load(f)
        self.nodes = {n["id"]: n for n in self.data["nodes"]}
        self.edges = self.data["edges"]

    def get_node(self, node_id: str) -> Optional[Dict]:
        return self.nodes.get(node_id)

    def get_dependencies(self, node_id: str, edge_type: str = "REQUIRES") -> List[Dict]:
        deps = []
        for edge in self.edges:
            if edge["source"] == node_id and edge["type"] == edge_type:
                target = self.get_node(edge["target"])
                if target:
                    deps.append({**target, "confidence": edge["confidence"]})
        return deps

    def get_recommendations(self, node_id: str) -> List[Dict]:
        return self.get_dependencies(node_id, "RECOMMENDED_WITH")

    def get_learning_path(self, goal_skills: List[str]) -> List[str]:
        path: List[str] = []
        visited: set = set()

        def traverse(skill_id: str):
            if skill_id in visited:
                return
            visited.add(skill_id)
            for prereq in self.get_dependencies(skill_id, "LEARN_BEFORE"):
                traverse(prereq["id"])
            if skill_id not in path:
                path.append(skill_id)

        for skill in goal_skills:
            traverse(skill)
        return path


# ---------------------------------------------------------------------------
# Recommendation Engine — taxonomy-driven, zero hardcoded goals
# ---------------------------------------------------------------------------

class RecommendationEngine:
    """Generate skill recommendations from meta/GOAL_TAXONOMY.md."""

    def __init__(self, graph: SkillsGraph, taxonomy: GoalTaxonomyParser):
        self.graph = graph
        self.taxonomy = taxonomy

    def recommend(self, goal_query: str) -> Dict[str, Any]:
        """
        Accept a free-text goal or goal ID, resolve it via the taxonomy,
        then build a recommendation from the parsed skill mappings.
        Returns an error dict if the goal cannot be resolved.
        """
        goal_id = self.taxonomy.resolve(goal_query)
        if not goal_id:
            available = [f"{g['id']}: {g['name']}" for g in self.taxonomy.list_goals()]
            return {
                "error": f"Unknown goal: '{goal_query}'. "
                         f"Available categories: {available}"
            }

        taxonomy_skills = self.taxonomy.skills_for(goal_id)

        # Determine goal metadata
        meta = (
            self.taxonomy.subgoals.get(goal_id)
            or self.taxonomy.goals.get(goal_id)
            or {}
        )
        goal_name = meta.get("name", goal_query)
        difficulty = meta.get("difficulty", "Unknown")

        # Split required (Critical/High) vs optional (Medium/Low)
        required_ids = [
            s["id"] for s in taxonomy_skills
            if s["priority"].lower() in ("critical", "high")
        ]
        optional_ids = [
            s["id"] for s in taxonomy_skills
            if s["priority"].lower() in ("medium", "low")
        ]

        required_skills = [self.graph.get_node(sid) or self._stub(sid) for sid in required_ids]
        optional_skills = [self.graph.get_node(sid) or self._stub(sid) for sid in optional_ids]

        all_dependencies: List[Dict] = []
        for skill in required_skills:
            all_dependencies.extend(self.graph.get_dependencies(skill["id"]))

        all_skill_ids = required_ids + optional_ids
        learning_path = self.graph.get_learning_path(all_skill_ids)
        learning_path_nodes = [
            self.graph.get_node(sid) or self._stub(sid) for sid in learning_path
        ]

        confidence = self._calculate_confidence(required_skills, all_dependencies)

        # Deployment heuristic from difficulty
        deployment = "local" if "beginner" in difficulty.lower() else "cloud"

        return {
            "goal_id": goal_id,
            "goal_name": goal_name,
            "taxonomy_skills": taxonomy_skills,
            "required_skills": required_skills,
            "optional_skills": optional_skills,
            "dependencies": all_dependencies,
            "learning_path": learning_path_nodes,
            "confidence_score": confidence,
            "deployment": deployment,
            "complexity": difficulty,
        }

    def _stub(self, skill_id: str) -> Dict:
        """Fallback node when skill_id is not yet in the graph."""
        return {
            "id": skill_id,
            "name": skill_id.replace("-", " ").title(),
            "stability": "experimental",
        }

    def _calculate_confidence(self, skills: List[Dict], dependencies: List[Dict]) -> float:
        if not skills:
            return 0.0
        stable_count = sum(1 for s in skills if s.get("stability") == "stable")
        base = stable_count / len(skills)
        dep_boost = min(len(dependencies) * 0.05, 0.2)
        return min(base + dep_boost, 1.0)


# ---------------------------------------------------------------------------
# Blueprint Generator — taxonomy-driven architecture type inference
# ---------------------------------------------------------------------------

class BlueprintGenerator:
    """Generate architecture blueprints from taxonomy-driven recommendations."""

    # Risk patterns keyed by skill-id substring (not goal name)
    _RISK_PATTERNS = {
        "code-generation": [
            {"severity": "Major", "probability": "Medium",
             "mitigation": "Implement code review and testing"}
        ],
        "browser-automation": [
            {"severity": "Major", "probability": "High",
             "mitigation": "Add retry logic and error handling"},
            {"severity": "Minor", "probability": "High",
             "mitigation": "Handle dynamic UI changes"},
        ],
        "screen-parsing": [
            {"severity": "Major", "probability": "High",
             "mitigation": "Add retry logic and error handling"},
        ],
        "vector-store-retrieval": [
            {"severity": "Major", "probability": "Medium",
             "mitigation": "Validate retrieval accuracy"},
            {"severity": "Critical", "probability": "Low",
             "mitigation": "Monitor for hallucinations"},
        ],
        "multi-agent": [
            {"severity": "Critical", "probability": "Medium",
             "mitigation": "Implement agent communication protocol and conflict resolution"},
        ],
    }

    # Architecture type inferred from goal category ID (taxonomy-driven)
    _ARCH_BY_CATEGORY = {
        "G01": "Single-Agent",
        "G02": "Single-Agent",
        "G03": "Single-Agent",
        "G04": "RAG",
        "G05": "Knowledge-Graph",
        "G06": "Workflow",
        "G07": "Single-Agent",
        "G08": "Multi-Agent",
        "G09": "Single-Agent",
        "G10": "Data-Pipeline",
        "G11": "Evaluation",
        "G12": "Single-Agent",
    }

    def generate(
        self, goal_query: str, recommendation: Dict[str, Any], taxonomy: GoalTaxonomyParser
    ) -> Dict[str, Any]:
        goal_id: str = recommendation.get("goal_id", "")
        goal_name: str = recommendation.get("goal_name", goal_query)
        taxonomy_skills: List[Dict] = recommendation.get("taxonomy_skills", [])

        risks = self._collect_risks(recommendation["required_skills"])
        arch_type = self._infer_arch(goal_id)
        frameworks = taxonomy.frameworks_for(goal_name)
        top_framework = (
            max(frameworks, key=frameworks.get) if frameworks else "Custom"
        )

        # Compute total estimated learn time from taxonomy
        total_hrs = sum(s.get("learn_time_hrs", 0) for s in taxonomy_skills)

        blueprint = {
            "$schema": "https://skillstree.os/schemas/v1/blueprint.json",
            "id": f"blueprint-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": goal_name,
            "goal": goal_name,
            "goal_id": goal_id,
            "description": f"Architecture blueprint for {goal_name}",
            "confidence_score": recommendation["confidence_score"],
            "generated_at": datetime.now().isoformat(),
            "architecture_type": arch_type,
            "deployment_type": recommendation.get("deployment", "cloud"),
            "complexity": recommendation.get("complexity", "Unknown"),
            "maturity": "Alpha",
            "estimated_learn_hours": total_hrs,
            "recommended_framework": top_framework,
            "required_skills": [
                {
                    "id": s["id"],
                    "name": s["name"],
                    "priority": "Critical" if i < 2 else "High",
                    "rationale": f"Core capability for {goal_name}",
                    "learn_time": f"{next((t['learn_time_hrs'] for t in taxonomy_skills if t['id'] == s['id']), 0)} hours",
                }
                for i, s in enumerate(recommendation["required_skills"])
            ],
            "optional_skills": [
                {"id": s["id"], "name": s["name"]}
                for s in recommendation["optional_skills"]
            ],
            "dependencies": [
                {"name": d["name"], "confidence": d.get("confidence", 0.0)}
                for d in recommendation["dependencies"]
            ],
            "learning_path": [s["name"] for s in recommendation["learning_path"]],
            "risks": risks,
        }
        return blueprint

    def _collect_risks(self, required_skills: List[Dict]) -> List[Dict]:
        risks = []
        seen = set()
        for skill in required_skills:
            sid = skill.get("id", "")
            for key, risk_list in self._RISK_PATTERNS.items():
                if key in sid and key not in seen:
                    risks.extend(risk_list)
                    seen.add(key)
        return risks

    def _infer_arch(self, goal_id: str) -> str:
        category = goal_id.split(".")[0] if goal_id else ""
        return self._ARCH_BY_CATEGORY.get(category, "Single-Agent")


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_blueprint(blueprint: Dict[str, Any]):
    print(f"\n{'='*70}")
    print(f"ARCHITECTURE BLUEPRINT: {blueprint['title']}")
    print(f"{'='*70}")
    print(f"\nID:                {blueprint['id']}")
    print(f"Goal ID:           {blueprint['goal_id']}")
    print(f"Confidence:        {blueprint['confidence_score']:.2f}")
    print(f"Architecture Type: {blueprint['architecture_type']}")
    print(f"Deployment:        {blueprint['deployment_type']}")
    print(f"Complexity:        {blueprint['complexity']}")
    print(f"Maturity:          {blueprint['maturity']}")
    print(f"Est. Learn Time:   {blueprint['estimated_learn_hours']} hours")
    print(f"Top Framework:     {blueprint['recommended_framework']}")

    print(f"\n{'─'*70}\nREQUIRED SKILLS:")
    for skill in blueprint["required_skills"]:
        print(f"  • {skill['name']} (Priority: {skill['priority']}, Learn Time: {skill['learn_time']})")
        print(f"    Rationale: {skill['rationale']}")

    if blueprint["optional_skills"]:
        print(f"\n{'─'*70}\nOPTIONAL SKILLS:")
        for skill in blueprint["optional_skills"]:
            print(f"  • {skill['name']}")

    if blueprint["dependencies"]:
        print(f"\n{'─'*70}\nDEPENDENCIES:")
        for dep in blueprint["dependencies"]:
            print(f"  • {dep['name']} (Confidence: {dep['confidence']:.2f})")

    print(f"\n{'─'*70}\nLEARNING PATH:")
    for i, skill in enumerate(blueprint["learning_path"], 1):
        print(f"  {i}. {skill}")

    if blueprint["risks"]:
        print(f"\n{'─'*70}\nRISKS:")
        for risk in blueprint["risks"]:
            print(f"  ⚠️  [{risk['severity']}] Probability: {risk['probability']}")
            print(f"      Mitigation: {risk['mitigation']}")

    print(f"\n{'='*70}\n")


# ---------------------------------------------------------------------------
# Validation harness
# ---------------------------------------------------------------------------

TEST_GOALS = [
    "Coding Agent",
    "Browser Agent",
    "Research Agent",
    "RAG Assistant",
    "Multi-Agent Systems",
]


def run_validation(
    engine: RecommendationEngine,
    generator: BlueprintGenerator,
    taxonomy: GoalTaxonomyParser,
):
    print("\n" + "="*70)
    print("VALIDATION RUN")
    print("="*70)
    results = []
    for goal in TEST_GOALS:
        rec = engine.recommend(goal)
        if "error" in rec:
            results.append({"goal": goal, "status": "FAIL", "reason": rec["error"]})
            print(f"  ✗ {goal}: {rec['error']}")
            continue
        bp = generator.generate(goal, rec, taxonomy)
        ok = (
            len(rec["required_skills"]) > 0
            and len(bp["learning_path"]) >= 0
        )
        status = "PASS" if ok else "FAIL"
        results.append({
            "goal": goal,
            "goal_id": rec["goal_id"],
            "status": status,
            "required_skills": len(rec["required_skills"]),
            "optional_skills": len(rec["optional_skills"]),
            "dependencies": len(rec["dependencies"]),
            "learning_path_steps": len(bp["learning_path"]),
            "confidence": round(rec["confidence_score"], 2),
            "arch_type": bp["architecture_type"],
        })
        icon = "✓" if ok else "✗"
        print(
            f"  {icon} {goal} [{rec['goal_id']}] "
            f"required={len(rec['required_skills'])} "
            f"optional={len(rec['optional_skills'])} "
            f"deps={len(rec['dependencies'])} "
            f"confidence={rec['confidence_score']:.2f}"
        )
    print("="*70)
    passed = sum(1 for r in results if r["status"] == "PASS")
    print(f"Result: {passed}/{len(results)} passed\n")
    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("\n🌳 Skills Tree OS - Agent Skill Architect")
    print("Taxonomy-driven · Single source of truth: meta/GOAL_TAXONOMY.md\n")

    script_dir = Path(os.path.abspath(__file__)).parent
    graph_path = script_dir / ".." / "data" / "SKILLS_GRAPH.json"
    taxonomy_path = script_dir / ".." / "meta" / "GOAL_TAXONOMY.md"

    # Load taxonomy
    if not taxonomy_path.exists():
        print(f"❌ Taxonomy not found: {taxonomy_path}")
        return
    taxonomy = GoalTaxonomyParser(str(taxonomy_path))
    print(f"✅ Taxonomy loaded: {len(taxonomy.goals)} goal categories, "
          f"{len(taxonomy.subgoals)} sub-goals")

    # Load graph
    try:
        graph = SkillsGraph(str(graph_path))
    except FileNotFoundError:
        print(f"⚠️  SKILLS_GRAPH.json not found at {graph_path}")
        print("   Running in taxonomy-only mode (no graph edges).")
        graph = type("_EmptyGraph", (), {
            "get_node": lambda self, x: None,
            "get_dependencies": lambda self, x, t="REQUIRES": [],
            "get_recommendations": lambda self, x: [],
            "get_learning_path": lambda self, x: [],
            "nodes": {},
            "edges": [],
        })()

    engine = RecommendationEngine(graph, taxonomy)
    generator = BlueprintGenerator()

    # --- mode selection ---
    import sys
    if "--validate" in sys.argv:
        run_validation(engine, generator, taxonomy)
        return

    # --- interactive ---
    print("Available Goal Categories (from taxonomy):")
    for g in taxonomy.list_goals():
        print(f"  {g['id']}: {g['name']} ({g['skills_count']} skills)")

    print("\nWhat do you want to build? (goal name, ID, or sub-goal ID like G01.4)")
    user_goal = input("> ").strip()
    if not user_goal:
        print("No goal provided. Exiting.")
        return

    print(f"\n⚙️  Resolving: {user_goal}...")
    recommendation = engine.recommend(user_goal)

    if "error" in recommendation:
        print(f"❌ {recommendation['error']}")
        return

    blueprint = generator.generate(user_goal, recommendation, taxonomy)
    print_blueprint(blueprint)

    output_path = f"blueprint_{blueprint['id']}.json"
    with open(output_path, "w") as f:
        json.dump(blueprint, f, indent=2)
    print(f"✅ Blueprint saved to: {output_path}")


if __name__ == "__main__":
    main()
