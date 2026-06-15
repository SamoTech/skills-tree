#!/usr/bin/env python3
"""
Skills Tree OS - Agent Skill Architect

Taxonomy-driven recommendation engine.
Single source of truth: meta/GOAL_TAXONOMY.md
No hardcoded goal lists, skill mappings, or recommendation rules.

Sprint C-01: per-skill numeric scoring engine.
  score = priority_weight + centrality_bonus + framework_bonus - learn_time_penalty
  Skills sorted descending by score; rank injected into every skill dict.

Sprint C-02: real graph-aware ranking.
  Centrality metrics pre-computed at graph load time and embedded per-node.
  SkillScorer reads node-level centrality; live edge-scan fallback retained.

Sprint C-03: Explanation Engine.
  Every skill carries:
    score_breakdown  — {priority, centrality, framework, learn_time} components
    explanation      — human-readable list of sentences, one per signal
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

    @property
    def goals(self) -> Dict[str, Dict]:
        return self._goals

    @property
    def subgoals(self) -> Dict[str, Dict]:
        return self._subgoals

    def skills_for(self, goal_id: str) -> List[Dict]:
        if goal_id in self._skill_maps:
            return self._skill_maps[goal_id]
        parent = goal_id.split(".")[0] if "." in goal_id else goal_id
        return self._skill_maps.get(parent, [])

    def frameworks_for(self, goal_name: str) -> Dict[str, int]:
        return self._framework_prefs.get(goal_name, {})

    def resolve(self, query: str) -> Optional[str]:
        q = query.strip().lower()
        for sid, meta in {**self._goals, **self._subgoals}.items():
            if sid.lower() == q:
                return sid
        for sid, meta in {**self._goals, **self._subgoals}.items():
            if meta["name"].lower() == q:
                return sid
        for sid, meta in {**self._goals, **self._subgoals}.items():
            if q in meta["name"].lower():
                return sid
        return None

    def list_goals(self) -> List[Dict]:
        return sorted(self._goals.values(), key=lambda g: g["id"])

    def _parse(self):
        self._parse_goal_categories()
        self._parse_subgoals()
        self._parse_skill_mappings()
        self._parse_framework_preferences()

    def _parse_goal_categories(self):
        pattern = re.compile(
            r"\|\s*`(G\d{2})`\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*(\d+)\s*\|"
        )
        for m in pattern.finditer(self._raw):
            gid, name, desc, diff, count = (
                m.group(1).strip(), m.group(2).strip(),
                m.group(3).strip(), m.group(4).strip(),
                int(m.group(5).strip()),
            )
            self._goals[gid] = {
                "id": gid, "name": name, "description": desc,
                "difficulty": diff, "skills_count": count,
            }

    def _parse_subgoals(self):
        pattern = re.compile(
            r"\|\s*`(G\d{2}\.\d+)`\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+)\|\s*([^|\n]+)\|"
        )
        for m in pattern.finditer(self._raw):
            sid, name, desc, diff = (
                m.group(1).strip(), m.group(2).strip(),
                m.group(3).strip(), m.group(4).strip(),
            )
            parent_id = sid.split(".")[0]
            parent_name = self._goals.get(parent_id, {}).get("name", parent_id)
            self._subgoals[sid] = {
                "id": sid, "name": name, "description": desc,
                "difficulty": diff, "parent_id": parent_id, "parent_name": parent_name,
            }

    def _parse_skill_mappings(self):
        row_re = re.compile(
            r"\|\s*`?([\w-]+)`?\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*(\d+)\s*hrs?\s*\|"
        )
        heading_re = re.compile(
            r"###\s+(Skill Mapping: .+?|G\d{2}(?:\.\d+)?: .+?)\n(.*?)(?=###|\Z)",
            re.DOTALL,
        )
        for hm in heading_re.finditer(self._raw):
            section_title = hm.group(1).strip()
            section_body = hm.group(2)
            gid_match = re.search(r"(G\d{2}(?:\.\d+)?)", section_title)
            if not gid_match:
                continue
            gid = gid_match.group(1)
            skills = []
            for rm in row_re.finditer(section_body):
                skills.append({
                    "id": rm.group(1).strip(), "name": rm.group(2).strip(),
                    "category": rm.group(3).strip(), "priority": rm.group(4).strip(),
                    "learn_time_hrs": int(rm.group(5)),
                })
            if not skills:
                list_re = re.compile(
                    r"^\d+\.\s+`([\w-]+)`\s+\(([^,]+),\s*(\d+)hrs?\)", re.MULTILINE
                )
                for lm in list_re.finditer(section_body):
                    skills.append({
                        "id": lm.group(1).strip(),
                        "name": lm.group(1).strip().replace("-", " ").title(),
                        "category": "", "priority": lm.group(2).strip(),
                        "learn_time_hrs": int(lm.group(3)),
                    })
            if skills:
                self._skill_maps[gid] = skills

    def _parse_framework_preferences(self):
        headers = ["OpenAI SDK", "LangChain", "LlamaIndex", "MCP", "Mastra", "Custom"]
        fw_block = re.search(
            r"### Framework Mapping by Goal\n(\|.+?\n)((?:\|[^\n]+\n)+)",
            self._raw, re.DOTALL,
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
                    ratings[fw] = cells[i].count("⭐")
            self._framework_prefs[goal_name] = ratings


# ---------------------------------------------------------------------------
# Skills Graph
# ---------------------------------------------------------------------------

class SkillsGraph:
    """
    Load and query the skills knowledge graph.
    C-02: centrality metrics read from embedded node block; live fallback retained.
    """

    def __init__(self, graph_path: str = "../data/SKILLS_GRAPH.json"):
        with open(graph_path, "r") as f:
            self.data = json.load(f)
        self.nodes: Dict[str, Dict] = {n["id"]: n for n in self.data["nodes"]}
        self.edges: List[Dict] = self.data["edges"]
        self._in_degree: Dict[str, int] = {}
        self._out_degree: Dict[str, int] = {}
        self._degree_centrality: Dict[str, float] = {}
        self._build_centrality()

    def _build_centrality(self) -> None:
        n_nodes = len(self.nodes)
        if n_nodes < 2:
            return
        sample = next(iter(self.nodes.values()))
        if "centrality" in sample:
            for nid, node in self.nodes.items():
                c = node.get("centrality", {})
                self._in_degree[nid] = c.get("in_degree", 0)
                self._out_degree[nid] = c.get("out_degree", 0)
                self._degree_centrality[nid] = c.get("degree_centrality", 0.0)
        else:
            from collections import defaultdict
            ind, outd = defaultdict(int), defaultdict(int)
            for edge in self.edges:
                ind[edge["target"]] += 1
                outd[edge["source"]] += 1
            for nid in self.nodes:
                self._in_degree[nid] = ind[nid]
                self._out_degree[nid] = outd[nid]
                self._degree_centrality[nid] = round((ind[nid] + outd[nid]) / (n_nodes - 1), 4)

    def in_degree(self, node_id: str) -> int:
        return self._in_degree.get(node_id, 0)

    def out_degree(self, node_id: str) -> int:
        return self._out_degree.get(node_id, 0)

    def degree_centrality(self, node_id: str) -> float:
        return self._degree_centrality.get(node_id, 0.0)

    def centrality(self, node_id: str) -> int:
        """Alias for in_degree — used by SkillScorer."""
        return self.in_degree(node_id)

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

    def centrality_report(self) -> List[Dict]:
        rows = []
        for nid, node in self.nodes.items():
            rows.append({
                "id": nid, "name": node.get("name", nid),
                "in_degree": self._in_degree.get(nid, 0),
                "out_degree": self._out_degree.get(nid, 0),
                "degree_centrality": self._degree_centrality.get(nid, 0.0),
                "centrality_bonus": min(self._in_degree.get(nid, 0) * 5, 30),
            })
        return sorted(rows, key=lambda x: x["in_degree"], reverse=True)


# ---------------------------------------------------------------------------
# Sprint C-01/C-02: Skill Scoring Engine
# ---------------------------------------------------------------------------

class SkillScorer:
    """
    score = priority_weight + centrality_bonus + framework_bonus - learn_time_penalty

    priority_weight    : Critical=100, High=70, Medium=40, Low=10
    centrality_bonus   : min(in_degree * 5, 30)
    framework_bonus    : top_framework_stars * 2  (max 10)
    learn_time_penalty : min(learn_time_hrs * 0.5, 20)
    """

    PRIORITY_WEIGHTS: Dict[str, float] = {
        "critical": 100.0, "high": 70.0, "medium": 40.0, "low": 10.0,
    }
    CENTRALITY_BONUS_PER_EDGE:   float = 5.0
    CENTRALITY_BONUS_CAP:        float = 30.0
    FRAMEWORK_BONUS_PER_STAR:    float = 2.0
    FRAMEWORK_BONUS_CAP:         float = 10.0
    LEARN_TIME_PENALTY_PER_HOUR: float = 0.5
    LEARN_TIME_PENALTY_CAP:      float = 20.0

    def __init__(self, graph: Any, frameworks: Dict[str, int]):
        self._graph = graph
        self._top_fw_stars: int = max(frameworks.values()) if frameworks else 0

    def score_components(
        self, skill_id: str, priority: str, learn_time_hrs: int
    ) -> Dict[str, float]:
        """Return all four components as a dict (used by ExplanationEngine)."""
        pw  = self.PRIORITY_WEIGHTS.get(priority.strip().lower(), 0.0)
        ind = getattr(self._graph, "centrality", lambda x: 0)(skill_id)
        cb  = min(ind * self.CENTRALITY_BONUS_PER_EDGE, self.CENTRALITY_BONUS_CAP)
        fb  = min(self._top_fw_stars * self.FRAMEWORK_BONUS_PER_STAR, self.FRAMEWORK_BONUS_CAP)
        lp  = min(learn_time_hrs * self.LEARN_TIME_PENALTY_PER_HOUR, self.LEARN_TIME_PENALTY_CAP)
        return {
            "priority":    round(pw, 2),
            "centrality":  round(cb, 2),
            "framework":   round(fb, 2),
            "learn_time":  round(-lp, 2),
            "total":       round(pw + cb + fb - lp, 2),
        }

    def score(self, skill_id: str, priority: str, learn_time_hrs: int) -> float:
        return self.score_components(skill_id, priority, learn_time_hrs)["total"]

    def rank_skills(
        self,
        skills: List[Dict],
        taxonomy_map: Dict[str, Dict],
        rank_offset: int = 1,
    ) -> List[Dict]:
        scored = []
        for skill in skills:
            sid = skill.get("id", "")
            tax = taxonomy_map.get(sid, {})
            priority       = tax.get("priority", "low")
            learn_time_hrs = tax.get("learn_time_hrs", 0)
            comps = self.score_components(sid, priority, learn_time_hrs)
            scored.append({**skill, "score": comps["total"], "_score_components": comps})
        scored.sort(key=lambda x: x["score"], reverse=True)
        for i, skill in enumerate(scored):
            skill["rank"] = rank_offset + i
        return scored


# ---------------------------------------------------------------------------
# Sprint C-03: Explanation Engine
# ---------------------------------------------------------------------------

class ExplanationEngine:
    """
    Generate human-readable explanations and structured score_breakdown
    for every scored skill.

    Input  : skill dict produced by SkillScorer.rank_skills()  (carries
             ``score``, ``rank``, ``_score_components``).
    Output : same dict enriched with ``score_breakdown`` and ``explanation``.

    score_breakdown mirrors the four signal components:
        {
          "priority":   <float>,   # raw priority weight
          "centrality": <float>,   # centrality bonus
          "framework":  <float>,   # framework bonus
          "learn_time": <float>,   # penalty (negative number)
        }

    explanation is a list of 3–4 plain-English sentences, one per signal,
    derived solely from computed values — no hardcoded text per skill.
    """

    @staticmethod
    def explain(
        skill: Dict,
        taxonomy_entry: Dict,
    ) -> Dict:
        """
        Enrich ``skill`` in-place with ``score_breakdown`` and ``explanation``.
        Returns the mutated dict.
        """
        comps    = skill.get("_score_components", {})
        priority = taxonomy_entry.get("priority", "unknown")
        learn_hrs = taxonomy_entry.get("learn_time_hrs", 0)
        ind       = int(round(comps.get("centrality", 0) / 5))  # reverse-compute in_degree
        fw_bonus  = comps.get("framework", 0.0)
        lp_abs    = abs(comps.get("learn_time", 0.0))

        # --- score_breakdown (external contract) ---
        skill["score_breakdown"] = {
            "priority":   comps.get("priority",   0.0),
            "centrality": comps.get("centrality", 0.0),
            "framework":  comps.get("framework",  0.0),
            "learn_time": comps.get("learn_time", 0.0),
        }

        # --- explanation sentences ---
        sentences: List[str] = []

        # 1. Priority signal
        p = priority.lower()
        if p == "critical":
            sentences.append("Critical priority — must-have for this goal")
        elif p == "high":
            sentences.append("High priority skill")
        elif p == "medium":
            sentences.append("Medium priority — recommended but optional")
        else:
            sentences.append("Low priority — nice to have")

        # 2. Centrality signal
        if ind == 0:
            sentences.append("No other skills depend on this — standalone capability")
        elif ind == 1:
            sentences.append(f"Referenced by 1 dependent skill (+{int(comps['centrality'])} centrality bonus)")
        else:
            sentences.append(
                f"Referenced by {ind} dependent skills (+{int(comps['centrality'])} centrality bonus)"
            )

        # 3. Framework signal
        if fw_bonus > 0:
            stars = int(fw_bonus / 2)
            sentences.append(
                f"Preferred framework has {stars}-star alignment with this goal (+{int(fw_bonus)} framework bonus)"
            )
        else:
            sentences.append("No framework preference boost for this goal")

        # 4. Learn-time signal
        if lp_abs == 0:
            sentences.append("Zero estimated learning time — no penalty")
        elif lp_abs <= 5:
            sentences.append(f"Low learning effort ({learn_hrs}h, -{lp_abs} penalty)")
        elif lp_abs <= 10:
            sentences.append(f"Moderate learning effort ({learn_hrs}h, -{lp_abs} penalty)")
        else:
            sentences.append(f"High learning effort ({learn_hrs}h, -{lp_abs} penalty)")

        skill["explanation"] = sentences

        # Clean up internal key not part of the public contract
        skill.pop("_score_components", None)
        return skill

    @classmethod
    def explain_all(
        cls,
        skills: List[Dict],
        taxonomy_map: Dict[str, Dict],
    ) -> List[Dict]:
        """Apply explain() to every skill in the list; returns the list."""
        for skill in skills:
            tax = taxonomy_map.get(skill.get("id", ""), {})
            cls.explain(skill, tax)
        return skills


# ---------------------------------------------------------------------------
# Recommendation Engine
# ---------------------------------------------------------------------------

class RecommendationEngine:
    def __init__(self, graph: Any, taxonomy: GoalTaxonomyParser):
        self.graph = graph
        self.taxonomy = taxonomy

    def recommend(self, goal_query: str) -> Dict[str, Any]:
        goal_id = self.taxonomy.resolve(goal_query)
        if not goal_id:
            available = [f"{g['id']}: {g['name']}" for g in self.taxonomy.list_goals()]
            return {"error": f"Unknown goal: '{goal_query}'. Available categories: {available}"}

        taxonomy_skills = self.taxonomy.skills_for(goal_id)
        meta       = self.taxonomy.subgoals.get(goal_id) or self.taxonomy.goals.get(goal_id) or {}
        goal_name  = meta.get("name", goal_query)
        difficulty = meta.get("difficulty", "Unknown")
        taxonomy_map: Dict[str, Dict] = {s["id"]: s for s in taxonomy_skills}

        required_ids   = [s["id"] for s in taxonomy_skills if s["priority"].lower() in ("critical", "high")]
        optional_ids   = [s["id"] for s in taxonomy_skills if s["priority"].lower() in ("medium", "low")]
        required_nodes = [self.graph.get_node(sid) or self._stub(sid) for sid in required_ids]
        optional_nodes = [self.graph.get_node(sid) or self._stub(sid) for sid in optional_ids]

        frameworks = self.taxonomy.frameworks_for(goal_name)
        scorer     = SkillScorer(self.graph, frameworks)

        required_skills = scorer.rank_skills(required_nodes, taxonomy_map, rank_offset=1)
        optional_skills = scorer.rank_skills(optional_nodes, taxonomy_map, rank_offset=len(required_skills) + 1)

        # C-03: inject explanation + score_breakdown into every skill
        ExplanationEngine.explain_all(required_skills, taxonomy_map)
        ExplanationEngine.explain_all(optional_skills, taxonomy_map)

        all_dependencies: List[Dict] = []
        for skill in required_skills:
            all_dependencies.extend(self.graph.get_dependencies(skill["id"]))

        all_skill_ids       = [s["id"] for s in required_skills + optional_skills]
        learning_path       = self.graph.get_learning_path(all_skill_ids)
        learning_path_nodes = [self.graph.get_node(sid) or self._stub(sid) for sid in learning_path]

        confidence = self._calculate_confidence(required_skills, all_dependencies)
        deployment = "local" if "beginner" in difficulty.lower() else "cloud"

        return {
            "goal_id": goal_id, "goal_name": goal_name,
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
        return {"id": skill_id, "name": skill_id.replace("-", " ").title(), "stability": "experimental"}

    def _calculate_confidence(self, skills: List[Dict], dependencies: List[Dict]) -> float:
        if not skills:
            return 0.0
        stable_count = sum(1 for s in skills if s.get("stability") == "stable")
        base      = stable_count / len(skills)
        dep_boost = min(len(dependencies) * 0.05, 0.2)
        return min(base + dep_boost, 1.0)


# ---------------------------------------------------------------------------
# Blueprint Generator
# ---------------------------------------------------------------------------

class BlueprintGenerator:
    _RISK_PATTERNS = {
        "code-generation":     [{"severity": "Major",    "probability": "Medium", "mitigation": "Implement code review and testing"}],
        "browser-automation":  [{"severity": "Major",    "probability": "High",   "mitigation": "Add retry logic and error handling"},
                                {"severity": "Minor",    "probability": "High",   "mitigation": "Handle dynamic UI changes"}],
        "screen-parsing":      [{"severity": "Major",    "probability": "High",   "mitigation": "Add retry logic and error handling"}],
        "vector-store-retrieval": [{"severity": "Major", "probability": "Medium", "mitigation": "Validate retrieval accuracy"},
                                   {"severity": "Critical", "probability": "Low", "mitigation": "Monitor for hallucinations"}],
        "multi-agent":         [{"severity": "Critical",  "probability": "Medium", "mitigation": "Implement agent communication protocol and conflict resolution"}],
    }
    _ARCH_BY_CATEGORY = {
        "G01": "Single-Agent", "G02": "Single-Agent", "G03": "Single-Agent",
        "G04": "RAG",          "G05": "Knowledge-Graph", "G06": "Workflow",
        "G07": "Single-Agent", "G08": "Multi-Agent",   "G09": "Single-Agent",
        "G10": "Data-Pipeline","G11": "Evaluation",    "G12": "Single-Agent",
    }

    def generate(
        self, goal_query: str, recommendation: Dict[str, Any], taxonomy: GoalTaxonomyParser
    ) -> Dict[str, Any]:
        goal_id         = recommendation.get("goal_id", "")
        goal_name       = recommendation.get("goal_name", goal_query)
        taxonomy_skills = recommendation.get("taxonomy_skills", [])
        taxonomy_map    = {s["id"]: s for s in taxonomy_skills}
        risks           = self._collect_risks(recommendation["required_skills"])
        arch_type       = self._infer_arch(goal_id)
        frameworks      = taxonomy.frameworks_for(goal_name)
        top_framework   = max(frameworks, key=frameworks.get) if frameworks else "Custom"
        total_hrs       = sum(s.get("learn_time_hrs", 0) for s in taxonomy_skills)

        return {
            "$schema": "https://skillstree.os/schemas/v1/blueprint.json",
            "id": f"blueprint-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": goal_name, "goal": goal_name, "goal_id": goal_id,
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
                    "id": s["id"], "name": s["name"],
                    "rank": s["rank"], "score": s["score"],
                    "score_breakdown": s.get("score_breakdown", {}),
                    "explanation": s.get("explanation", []),
                    "priority": taxonomy_map.get(s["id"], {}).get("priority", "Unknown"),
                    "learn_time": f"{taxonomy_map.get(s['id'], {}).get('learn_time_hrs', 0)} hours",
                }
                for s in recommendation["required_skills"]
            ],
            "optional_skills": [
                {
                    "id": s["id"], "name": s["name"],
                    "rank": s["rank"], "score": s["score"],
                    "score_breakdown": s.get("score_breakdown", {}),
                    "explanation": s.get("explanation", []),
                    "priority": taxonomy_map.get(s["id"], {}).get("priority", "Unknown"),
                }
                for s in recommendation["optional_skills"]
            ],
            "dependencies": [
                {"name": d["name"], "confidence": d.get("confidence", 0.0)}
                for d in recommendation["dependencies"]
            ],
            "learning_path": [s["name"] for s in recommendation["learning_path"]],
            "risks": risks,
        }

    def _collect_risks(self, required_skills):
        risks, seen = [], set()
        for skill in required_skills:
            sid = skill.get("id", "")
            for key, risk_list in self._RISK_PATTERNS.items():
                if key in sid and key not in seen:
                    risks.extend(risk_list)
                    seen.add(key)
        return risks

    def _infer_arch(self, goal_id):
        return self._ARCH_BY_CATEGORY.get(goal_id.split(".")[0] if goal_id else "", "Single-Agent")


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

    print(f"\n{'\u2500'*70}\nREQUIRED SKILLS (sorted by score \u2193):")
    for skill in blueprint["required_skills"]:
        bd = skill.get("score_breakdown", {})
        print(
            f"  #{skill['rank']:>2}  {skill['name']:<32}  "
            f"score={skill['score']:>7.2f}  priority={skill['priority']:<8}  learn={skill['learn_time']}"
        )
        print(
            f"       Breakdown: priority={bd.get('priority',0):>6}  "
            f"centrality={bd.get('centrality',0):>5}  "
            f"framework={bd.get('framework',0):>5}  "
            f"learn_time={bd.get('learn_time',0):>6}"
        )
        for line in skill.get("explanation", []):
            print(f"       • {line}")

    if blueprint["optional_skills"]:
        print(f"\n{'\u2500'*70}\nOPTIONAL SKILLS (sorted by score \u2193):")
        for skill in blueprint["optional_skills"]:
            bd = skill.get("score_breakdown", {})
            print(
                f"  #{skill['rank']:>2}  {skill['name']:<32}  "
                f"score={skill['score']:>7.2f}  priority={skill['priority']}"
            )
            for line in skill.get("explanation", []):
                print(f"       • {line}")

    if blueprint["dependencies"]:
        print(f"\n{'\u2500'*70}\nDEPENDENCIES:")
        for dep in blueprint["dependencies"]:
            print(f"  \u2022 {dep['name']} (Confidence: {dep['confidence']:.2f})")

    print(f"\n{'\u2500'*70}\nLEARNING PATH:")
    for i, skill in enumerate(blueprint["learning_path"], 1):
        print(f"  {i}. {skill}")

    if blueprint["risks"]:
        print(f"\n{'\u2500'*70}\nRISKS:")
        for risk in blueprint["risks"]:
            print(f"  \u26a0\ufe0f  [{risk['severity']}] Probability: {risk['probability']}")
            print(f"      Mitigation: {risk['mitigation']}")

    print(f"\n{'='*70}\n")


# ---------------------------------------------------------------------------
# Validation harness
# ---------------------------------------------------------------------------

TEST_GOALS = [
    "Coding Agent", "Browser Agent", "Research Agent",
    "RAG Assistant", "Multi-Agent Systems",
]


def run_validation(engine, generator, taxonomy):
    print("\n" + "="*70)
    print("VALIDATION RUN (C-01 + C-02 + C-03)")
    print("="*70)
    results = []
    for goal in TEST_GOALS:
        rec = engine.recommend(goal)
        if "error" in rec:
            results.append({"goal": goal, "status": "FAIL", "reason": rec["error"]})
            print(f"  \u2717 {goal}: {rec['error']}")
            continue
        bp  = generator.generate(goal, rec, taxonomy)
        req = bp["required_skills"]

        scores_present   = all("score" in s and "rank" in s for s in req)
        scores_sorted    = all(req[i]["score"] >= req[i+1]["score"] for i in range(len(req)-1))
        has_breakdown    = all("score_breakdown" in s for s in req)
        has_explanation  = all("explanation" in s and len(s["explanation"]) >= 3 for s in req)

        ok     = len(req) > 0 and scores_present and scores_sorted and has_breakdown and has_explanation
        status = "PASS" if ok else "FAIL"
        results.append({
            "goal": goal, "goal_id": rec["goal_id"], "status": status,
            "required": len(req), "optional": len(bp["optional_skills"]),
            "scores_sorted": scores_sorted,
            "has_breakdown": has_breakdown, "has_explanation": has_explanation,
            "top_skill": f"{req[0]['name']} score={req[0]['score']} rank=#{req[0]['rank']}" if req else "n/a",
        })
        icon = "\u2713" if ok else "\u2717"
        print(
            f"  {icon} {goal} [{rec['goal_id']}]  sorted={scores_sorted}  "
            f"breakdown={has_breakdown}  explanation={has_explanation}  "
            f"top='{req[0]['name'] if req else 'n/a'}'"
        )
    print("="*70)
    passed = sum(1 for r in results if r["status"] == "PASS")
    print(f"Result: {passed}/{len(results)} passed\n")
    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("\n\U0001f333 Skills Tree OS - Agent Skill Architect")
    print("Taxonomy-driven \u00b7 Single source of truth: meta/GOAL_TAXONOMY.md\n")

    script_dir    = Path(os.path.abspath(__file__)).parent
    graph_path    = script_dir / ".." / "data" / "SKILLS_GRAPH.json"
    taxonomy_path = script_dir / ".." / "meta" / "GOAL_TAXONOMY.md"

    if not taxonomy_path.exists():
        print(f"\u274c Taxonomy not found: {taxonomy_path}")
        return
    taxonomy = GoalTaxonomyParser(str(taxonomy_path))
    print(f"\u2705 Taxonomy loaded: {len(taxonomy.goals)} goal categories, {len(taxonomy.subgoals)} sub-goals")

    try:
        graph  = SkillsGraph(str(graph_path))
        report = graph.centrality_report()
        print(f"\u2705 Graph loaded: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
        print("\nTop-10 Centrality (in-degree):")
        for i, r in enumerate(report[:10], 1):
            print(
                f"  #{i:<2} {r['name']:<30}  in={r['in_degree']}  out={r['out_degree']}  "
                f"dc={r['degree_centrality']:.4f}  bonus=+{r['centrality_bonus']}"
            )
    except FileNotFoundError:
        print(f"\u26a0\ufe0f  SKILLS_GRAPH.json not found at {graph_path}")
        print("   Running in taxonomy-only mode (no graph edges).")
        graph = type("_EmptyGraph", (), {
            "get_node": lambda self, x: None,
            "get_dependencies": lambda self, x, t="REQUIRES": [],
            "get_recommendations": lambda self, x: [],
            "get_learning_path": lambda self, x: [],
            "centrality": lambda self, x: 0,
            "centrality_report": lambda self: [],
            "nodes": {}, "edges": [],
        })()

    engine    = RecommendationEngine(graph, taxonomy)
    generator = BlueprintGenerator()

    import sys
    if "--validate" in sys.argv:
        run_validation(engine, generator, taxonomy)
        return

    print("\nAvailable Goal Categories (from taxonomy):")
    for g in taxonomy.list_goals():
        print(f"  {g['id']}: {g['name']} ({g['skills_count']} skills)")

    print("\nWhat do you want to build? (goal name, ID, or sub-goal ID like G01.4)")
    user_goal = input("> ").strip()
    if not user_goal:
        print("No goal provided. Exiting.")
        return

    print(f"\n\u2699\ufe0f  Resolving: {user_goal}...")
    recommendation = engine.recommend(user_goal)
    if "error" in recommendation:
        print(f"\u274c {recommendation['error']}")
        return

    blueprint = generator.generate(user_goal, recommendation, taxonomy)
    print_blueprint(blueprint)

    output_path = f"blueprint_{blueprint['id']}.json"
    with open(output_path, "w") as f:
        json.dump(blueprint, f, indent=2)
    print(f"\u2705 Blueprint saved to: {output_path}")


if __name__ == "__main__":
    main()
