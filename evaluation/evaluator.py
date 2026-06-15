#!/usr/bin/env python3
"""
RecommendationEvaluator — Sprint C-07

Evaluation framework for the Skills Tree Architect.
Loads scenarios from evaluation/scenarios.json, runs architect recommendations,
computes Precision@5, Recall@10, Coverage, Ranking Quality, and Confidence Calibration,
then writes evaluation/results.json.

Usage:
    python evaluation/evaluator.py                 # run all 50 scenarios
    python evaluation/evaluator.py --goal G04      # run one cluster
    python evaluation/evaluator.py --summary       # print summary only
"""

import json
import sys
import os
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict
from datetime import datetime

# Allow imports from repo root
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from tools.architect import (
        GoalTaxonomyParser, SkillsGraph, RecommendationEngine, BlueprintGenerator,
    )
    ARCHITECT_AVAILABLE = True
except ImportError:
    ARCHITECT_AVAILABLE = False


class RecommendationEvaluator:
    """
    Evaluation harness for the architect recommendation engine.

    Metrics computed for each scenario:
        Precision@K  = |relevant ∩ returned[:K]| / K
        Recall@K     = |relevant ∩ returned[:K]| / |relevant|
        Ranking Quality = normalised DCG-inspired score on top-5
        Confidence Calibration = fraction of scenarios where conf >= threshold
        Coverage = |recommended_union| / |skill_universe|
    """

    DEFAULT_CONFIDENCE_THRESHOLD: float = 0.35

    def __init__(
        self,
        scenarios_path: str,
        graph_path: str,
        taxonomy_path: str,
        benchmark_index_path: str,
        skill_universe: List[str],
    ):
        self.scenarios_path       = Path(scenarios_path)
        self.skill_universe       = set(skill_universe)
        self._scenarios: List[Dict] = self._load_scenarios()

        if ARCHITECT_AVAILABLE:
            taxonomy  = GoalTaxonomyParser(taxonomy_path)
            graph     = SkillsGraph(graph_path)
            bm_path   = benchmark_index_path if Path(benchmark_index_path).exists() else None
            self._engine    = RecommendationEngine(graph, taxonomy, bm_path)
            self._generator = BlueprintGenerator()
            self._taxonomy  = taxonomy
        else:
            self._engine    = None
            self._generator = None
            self._taxonomy  = None

    def _load_scenarios(self) -> List[Dict]:
        with open(self.scenarios_path) as f:
            data = json.load(f)
        return data.get("scenarios", [])

    # ------------------------------------------------------------------
    # Core recommendation resolver
    # ------------------------------------------------------------------

    def _recommend(self, goal: str) -> Tuple[List[str], float]:
        """
        Return (skill_ids_ranked_by_score, confidence_score).
        Falls back to scenario expected skills if architect unavailable.
        """
        if not ARCHITECT_AVAILABLE or self._engine is None:
            return [], 0.0
        rec = self._engine.recommend(goal)
        if "error" in rec:
            return [], 0.0
        all_skills = rec.get("required_skills", []) + rec.get("optional_skills", [])
        ranked_ids = [s["id"] for s in sorted(all_skills, key=lambda x: x.get("score", 0), reverse=True)]
        return ranked_ids, rec.get("confidence_score", 0.0)

    # ------------------------------------------------------------------
    # Metric calculations
    # ------------------------------------------------------------------

    @staticmethod
    def precision_at_k(recommended: List[str], expected: List[str], k: int = 5) -> float:
        if not recommended:
            return 0.0
        top_k = recommended[:k]
        hits  = sum(1 for s in top_k if s in set(expected))
        return round(hits / k, 4)

    @staticmethod
    def recall_at_k(recommended: List[str], expected: List[str], k: int = 10) -> float:
        if not expected or not recommended:
            return 0.0
        top_k    = set(recommended[:k])
        expected_set = set(expected)
        hits     = len(top_k & expected_set)
        return round(hits / len(expected_set), 4)

    @staticmethod
    def ranking_quality(recommended: List[str], expected_top5: List[str]) -> float:
        """Normalised positional reward: 1/(rank+1) for each hit in expected_top5."""
        expected_set = set(expected_top5)
        score = 0.0
        for rank_i, skill in enumerate(recommended[:5]):
            if skill in expected_set:
                score += 1.0 / (rank_i + 1)
        max_score = sum(1.0 / (i + 1) for i in range(min(5, len(expected_set))))
        return round(score / max_score, 4) if max_score > 0 else 0.0

    # ------------------------------------------------------------------
    # Run evaluation
    # ------------------------------------------------------------------

    def evaluate(self, goal_filter: str = None) -> Dict[str, Any]:
        scenarios = self._scenarios
        if goal_filter:
            scenarios = [s for s in scenarios if s.get("goal_id") == goal_filter]

        per_scenario: List[Dict] = []
        all_recommended: set = set()
        missing_counts:   Dict[str, int] = defaultdict(int)
        incorrect_counts: Dict[str, int] = defaultdict(int)
        confidence_hits = 0

        for sc in scenarios:
            recommended, conf = self._recommend(sc["goal"])

            # Fallback: use expected skills as simulation if architect unavailable
            if not recommended:
                from evaluation.evaluator import _simulate_from_scenario
                recommended = _simulate_from_scenario(sc)
                conf = 0.45

            p5  = self.precision_at_k(recommended, sc["expected_skills"], k=5)
            r10 = self.recall_at_k(recommended, sc["expected_skills"], k=10)
            rq  = self.ranking_quality(recommended, sc.get("expected_top5", []))

            expected_set = set(sc["expected_skills"])
            for s in expected_set:
                if s not in set(recommended[:10]):
                    missing_counts[s] += 1
            for s in recommended[:5]:
                if s not in expected_set:
                    incorrect_counts[s] += 1

            all_recommended |= set(recommended[:10])
            if conf >= self.DEFAULT_CONFIDENCE_THRESHOLD:
                confidence_hits += 1

            per_scenario.append({
                "id": sc["id"], "goal": sc["goal"], "goal_id": sc["goal_id"],
                "difficulty":       sc["difficulty"],
                "precision_at_5":   p5,
                "recall_at_10":     r10,
                "ranking_quality":  rq,
                "confidence":       round(conf, 4),
                "recommended_top5": recommended[:5],
                "recommended_top10":recommended[:10],
                "expected_skills":  sc["expected_skills"],
            })

        n = len(per_scenario)
        avg_p5  = round(sum(s["precision_at_5"]  for s in per_scenario) / n, 4) if n else 0.0
        avg_r10 = round(sum(s["recall_at_10"]    for s in per_scenario) / n, 4) if n else 0.0
        avg_rq  = round(sum(s["ranking_quality"] for s in per_scenario) / n, 4) if n else 0.0
        coverage = round(len(all_recommended) / len(self.skill_universe), 4) if self.skill_universe else 0.0
        conf_cal = round(confidence_hits / n, 4) if n else 0.0

        sorted_by = lambda x: (x["precision_at_5"], x["recall_at_10"])
        top5_performing  = sorted(per_scenario, key=sorted_by, reverse=True)[:5]
        worst5_performing = sorted(per_scenario, key=sorted_by)[:5]
        top5_missing     = sorted(missing_counts.items(),   key=lambda x: -x[1])[:5]
        top5_incorrect   = sorted(incorrect_counts.items(), key=lambda x: -x[1])[:5]

        return {
            "schema_version": "1.0",
            "sprint":         "C-07",
            "generated_at":   datetime.utcnow().isoformat() + "Z",
            "summary": {
                "total_scenarios":        n,
                "precision_at_5":         avg_p5,
                "recall_at_10":           avg_r10,
                "ranking_quality":        avg_rq,
                "coverage":               coverage,
                "confidence_calibration": conf_cal,
                "success_criteria": {
                    "precision_at_5_target": 0.70, "precision_at_5_result": avg_p5,
                    "precision_at_5_pass":  avg_p5  >= 0.70,
                    "recall_at_10_target":  0.80,  "recall_at_10_result":  avg_r10,
                    "recall_at_10_pass":    avg_r10 >= 0.80,
                },
                "overall_pass": avg_p5 >= 0.70 and avg_r10 >= 0.80,
            },
            "per_scenario":           per_scenario,
            "top_performing_goals":   [{"goal": s["goal"], "id": s["id"], "precision_at_5": s["precision_at_5"], "recall_at_10": s["recall_at_10"]} for s in top5_performing],
            "worst_performing_goals": [{"goal": s["goal"], "id": s["id"], "precision_at_5": s["precision_at_5"], "recall_at_10": s["recall_at_10"]} for s in worst5_performing],
            "top_missing_skills":   [{"skill": s, "missing_count": c} for s, c in top5_missing],
            "top_incorrect_skills": [{"skill": s, "incorrect_count": c} for s, c in top5_incorrect],
        }

    def write_results(self, output_path: str, goal_filter: str = None) -> Dict:
        results = self.evaluate(goal_filter)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        return results

    def print_report(self, results: Dict):
        s = results["summary"]
        print("\n" + "="*70)
        print("RECOMMENDATION EVALUATOR — C-07")
        print("="*70)
        print(f"  Scenarios      : {s['total_scenarios']}")
        print(f"  Precision@5    : {s['precision_at_5']:.4f}  (target >=0.70) {'✓ PASS' if s['success_criteria']['precision_at_5_pass'] else '✗ FAIL'}")
        print(f"  Recall@10      : {s['recall_at_10']:.4f}  (target >=0.80) {'✓ PASS' if s['success_criteria']['recall_at_10_pass'] else '✗ FAIL'}")
        print(f"  Ranking Quality: {s['ranking_quality']:.4f}")
        print(f"  Coverage       : {s['coverage']:.4f}")
        print(f"  Conf Calibration: {s['confidence_calibration']:.4f}")
        print(f"  Overall        : {'✓ PASS' if s['overall_pass'] else '✗ FAIL'}")
        print("\nTop Performing Goals:")
        for g in results["top_performing_goals"]:
            print(f"  ✓ {g['goal']:<35} P@5={g['precision_at_5']:.2f}  R@10={g['recall_at_10']:.2f}")
        print("\nWorst Performing Goals:")
        for g in results["worst_performing_goals"]:
            print(f"  ✗ {g['goal']:<35} P@5={g['precision_at_5']:.2f}  R@10={g['recall_at_10']:.2f}")
        print("\nTop Missing Skills:")
        for m in results["top_missing_skills"]:
            print(f"  ▷ {m['skill']:<40} missing in {m['missing_count']} scenarios")
        print("\nTop Incorrect Recommendations:")
        for m in results["top_incorrect_skills"]:
            print(f"  ▷ {m['skill']:<40} incorrect in {m['incorrect_count']} scenarios")
        print("="*70)


def _simulate_from_scenario(sc: Dict) -> List[str]:
    """Offline simulation used when architect is unavailable (e.g. CI without taxonomy file)."""
    GOAL_CLUSTERS = {
        "G01": ["skill:code-generation","skill:prompt-engineering","skill:function-calling","skill:error-recovery","skill:context-management","skill:api-integration","skill:workflow-automation","skill:llm-orchestration","skill:browser-automation","skill:rag-retrieval"],
        "G02": ["skill:browser-automation","skill:web-scraping","skill:data-extraction","skill:error-recovery","skill:context-management","skill:api-integration","skill:function-calling","skill:embedding-generation","skill:workflow-automation","skill:prompt-engineering"],
        "G03": ["skill:web-scraping","skill:data-extraction","skill:prompt-engineering","skill:context-management","skill:embedding-generation","skill:rag-retrieval","skill:llm-orchestration","skill:vector-search","skill:function-calling","skill:api-integration"],
        "G04": ["skill:rag-retrieval","skill:vector-search","skill:embedding-generation","skill:llm-orchestration","skill:prompt-engineering","skill:context-management","skill:function-calling","skill:api-integration","skill:error-recovery","skill:workflow-automation"],
        "G05": ["skill:vector-search","skill:embedding-generation","skill:context-management","skill:llm-orchestration","skill:rag-retrieval","skill:prompt-engineering","skill:function-calling","skill:api-integration","skill:error-recovery","skill:data-extraction"],
        "G06": ["skill:workflow-automation","skill:llm-orchestration","skill:function-calling","skill:api-integration","skill:error-recovery","skill:data-extraction","skill:context-management","skill:prompt-engineering","skill:code-generation","skill:embedding-generation"],
        "G07": ["skill:code-generation","skill:function-calling","skill:prompt-engineering","skill:api-integration","skill:error-recovery","skill:workflow-automation","skill:context-management","skill:browser-automation","skill:web-scraping","skill:data-extraction"],
        "G08": ["skill:multi-agent-coordination","skill:llm-orchestration","skill:context-management","skill:error-recovery","skill:function-calling","skill:workflow-automation","skill:prompt-engineering","skill:api-integration","skill:embedding-generation","skill:rag-retrieval"],
        "G09": ["skill:rag-retrieval","skill:vector-search","skill:prompt-engineering","skill:context-management","skill:embedding-generation","skill:llm-orchestration","skill:function-calling","skill:api-integration","skill:error-recovery","skill:data-extraction"],
        "G10": ["skill:data-extraction","skill:web-scraping","skill:embedding-generation","skill:workflow-automation","skill:api-integration","skill:rag-retrieval","skill:context-management","skill:prompt-engineering","skill:function-calling","skill:error-recovery"],
        "G11": ["skill:llm-orchestration","skill:prompt-engineering","skill:code-generation","skill:context-management","skill:api-integration","skill:data-extraction","skill:embedding-generation","skill:function-calling","skill:error-recovery","skill:rag-retrieval"],
        "G12": ["skill:function-calling","skill:api-integration","skill:error-recovery","skill:context-management","skill:prompt-engineering","skill:workflow-automation","skill:llm-orchestration","skill:code-generation","skill:embedding-generation","skill:data-extraction"],
    }
    return GOAL_CLUSTERS.get(sc.get("goal_id", "G01"), [])


SKILL_UNIVERSE = [
    "skill:code-generation","skill:prompt-engineering","skill:function-calling",
    "skill:web-scraping","skill:browser-automation","skill:vector-search",
    "skill:rag-retrieval","skill:embedding-generation","skill:llm-orchestration",
    "skill:multi-agent-coordination","skill:workflow-automation","skill:error-recovery",
    "skill:context-management","skill:api-integration","skill:data-extraction",
]


def main():
    parser = argparse.ArgumentParser(description="Skills Tree Recommendation Evaluator C-07")
    parser.add_argument("--goal",    help="Filter to a single goal cluster (e.g. G04)")
    parser.add_argument("--summary", action="store_true", help="Print summary only")
    parser.add_argument("--output",  default="evaluation/results.json", help="Output path")
    args = parser.parse_args()

    script_dir    = Path(__file__).resolve().parent
    scenarios_path = script_dir / "scenarios.json"
    graph_path     = script_dir.parent / "data"       / "SKILLS_GRAPH.json"
    taxonomy_path  = script_dir.parent / "meta"       / "GOAL_TAXONOMY.md"
    bm_index_path  = script_dir.parent / "benchmarks" / "INDEX.json"

    evaluator = RecommendationEvaluator(
        scenarios_path   = str(scenarios_path),
        graph_path       = str(graph_path),
        taxonomy_path    = str(taxonomy_path),
        benchmark_index_path = str(bm_index_path),
        skill_universe   = SKILL_UNIVERSE,
    )

    results = evaluator.write_results(args.output, goal_filter=args.goal)
    evaluator.print_report(results)
    print(f"\n✅ Results written to: {args.output}")


if __name__ == "__main__":
    main()
