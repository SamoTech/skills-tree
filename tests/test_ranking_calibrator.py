#!/usr/bin/env python3
"""
Unit tests for RankingCalibrator — Sprint C-08.
Verifies all four calibration layers (global penalties, global boosts,
goal-specific adjustments, keyword layer) and integration metrics.
"""

import sys
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.ranking_calibrator import (
    RankingCalibrator,
    GLOBAL_PENALTIES, GLOBAL_BOOSTS, GOAL_ADJUSTMENTS, KEYWORD_ADJUSTMENTS,
)

ALL_SKILLS = [
    "skill:code-generation", "skill:prompt-engineering", "skill:function-calling",
    "skill:web-scraping", "skill:browser-automation", "skill:vector-search",
    "skill:rag-retrieval", "skill:embedding-generation", "skill:llm-orchestration",
    "skill:multi-agent-coordination", "skill:workflow-automation", "skill:error-recovery",
    "skill:context-management", "skill:api-integration", "skill:data-extraction",
]


class TestGlobalPenalties(unittest.TestCase):
    def setUp(self):
        self.cal = RankingCalibrator()

    def test_llm_orchestration_demoted(self):
        """skill:llm-orchestration must not rank top-1 after penalty."""
        skills = ["skill:llm-orchestration"] + [s for s in ALL_SKILLS if s != "skill:llm-orchestration"]
        result = self.cal.calibrate_ids(skills)
        self.assertNotEqual(result[0], "skill:llm-orchestration")

    def test_context_management_demoted(self):
        skills = ["skill:context-management"] + [s for s in ALL_SKILLS if s != "skill:context-management"]
        result = self.cal.calibrate_ids(skills)
        self.assertNotEqual(result[0], "skill:context-management")

    def test_penalty_is_negative(self):
        for sid, delta in GLOBAL_PENALTIES.items():
            self.assertLess(delta, 0.0, f"{sid} penalty should be negative")


class TestGlobalBoosts(unittest.TestCase):
    def setUp(self):
        self.cal = RankingCalibrator()

    def test_prompt_engineering_boosted(self):
        """skill:prompt-engineering should move up in ranking after boost."""
        skills = ALL_SKILLS.copy()  # prompt-engineering starts at rank 1 (index 1)
        base_rank = ALL_SKILLS.index("skill:prompt-engineering")
        result = self.cal.calibrate_ids(ALL_SKILLS)
        new_rank = result.index("skill:prompt-engineering")
        self.assertLessEqual(new_rank, base_rank)

    def test_rag_retrieval_boosted(self):
        result = self.cal.calibrate_ids(ALL_SKILLS)
        rag_rank = result.index("skill:rag-retrieval")
        self.assertLessEqual(rag_rank, 5)

    def test_boost_is_positive(self):
        for sid, delta in GLOBAL_BOOSTS.items():
            self.assertGreater(delta, 0.0, f"{sid} boost should be positive")


class TestGoalSpecificAdjustments(unittest.TestCase):
    def setUp(self):
        self.cal = RankingCalibrator()

    def test_G10_rag_boosted(self):
        """In G10, rag-retrieval should rank higher than without calibration."""
        base = self.cal.calibrate_ids(ALL_SKILLS, goal_id="")
        g10  = self.cal.calibrate_ids(ALL_SKILLS, goal_id="G10")
        rag_base = base.index("skill:rag-retrieval")
        rag_g10  = g10.index("skill:rag-retrieval")
        self.assertLessEqual(rag_g10, rag_base)

    def test_G07_browser_automation_boosted(self):
        g07 = self.cal.calibrate_ids(ALL_SKILLS, goal_id="G07")
        self.assertLessEqual(g07.index("skill:browser-automation"), 4)

    def test_G11_web_scraping_demoted(self):
        base = self.cal.calibrate_ids(ALL_SKILLS, goal_id="")
        g11  = self.cal.calibrate_ids(ALL_SKILLS, goal_id="G11")
        ws_base = base.index("skill:web-scraping")
        ws_g11  = g11.index("skill:web-scraping")
        self.assertGreaterEqual(ws_g11, ws_base)

    def test_goal_ids_covered(self):
        expected_goal_ids = {"G01", "G03", "G07", "G10", "G11"}
        self.assertEqual(expected_goal_ids, set(GOAL_ADJUSTMENTS.keys()))


class TestKeywordLayer(unittest.TestCase):
    def setUp(self):
        self.cal = RankingCalibrator()

    def test_memory_keyword_boosts_context(self):
        result = self.cal.calibrate_ids(ALL_SKILLS, goal_text="Memory Agent")
        cm_rank = result.index("skill:context-management")
        self.assertLessEqual(cm_rank, 3)

    def test_security_keyword_boosts_browser(self):
        result = self.cal.calibrate_ids(ALL_SKILLS, goal_text="Security Audit Agent", goal_id="G07")
        ba_rank = result.index("skill:browser-automation")
        self.assertLessEqual(ba_rank, 3)

    def test_analytics_keyword_boosts_rag(self):
        result = self.cal.calibrate_ids(ALL_SKILLS, goal_text="Analytics Agent", goal_id="G10")
        rag_rank = result.index("skill:rag-retrieval")
        self.assertLessEqual(rag_rank, 3)

    def test_sales_keyword_boosts_rag(self):
        result = self.cal.calibrate_ids(ALL_SKILLS, goal_text="Sales Assistant Agent", goal_id="G01")
        rag_rank = result.index("skill:rag-retrieval")
        self.assertLessEqual(rag_rank, 4)

    def test_keyword_count(self):
        self.assertGreaterEqual(len(KEYWORD_ADJUSTMENTS), 10)


class TestCalibratorAPI(unittest.TestCase):
    def setUp(self):
        self.cal = RankingCalibrator()

    def test_returns_tuples(self):
        result = self.cal.calibrate(ALL_SKILLS)
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], tuple)
        self.assertEqual(len(result[0]), 2)

    def test_sorted_descending(self):
        result = self.cal.calibrate(ALL_SKILLS)
        scores = [s for _, s in result]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_accepts_tuples_input(self):
        scored = [(sid, 10.0 - i) for i, sid in enumerate(ALL_SKILLS)]
        result = self.cal.calibrate(scored)
        self.assertEqual(len(result), len(ALL_SKILLS))

    def test_describe_adjustments(self):
        adj = self.cal.describe_adjustments(goal_id="G10", goal_text="Analytics Agent")
        self.assertIn("skill:rag-retrieval", adj)
        self.assertGreater(adj["skill:rag-retrieval"], 0)

    def test_calibrate_ids_returns_strings(self):
        result = self.cal.calibrate_ids(ALL_SKILLS, goal_id="G04", goal_text="RAG Assistant")
        self.assertTrue(all(isinstance(s, str) for s in result))

    def test_no_skills_lost(self):
        result = self.cal.calibrate_ids(ALL_SKILLS)
        self.assertEqual(set(result), set(ALL_SKILLS))


class TestCalibrationReport(unittest.TestCase):
    def setUp(self):
        report_path = Path(__file__).resolve().parent.parent / "evaluation" / "calibration_report.json"
        if report_path.exists():
            with open(report_path) as f:
                self.report = json.load(f)
            self.available = True
        else:
            self.available = False

    def test_report_exists(self):
        if not self.available:
            self.skipTest("calibration_report.json not found")
        self.assertIn("after_calibration", self.report)

    def test_precision_at_5_passes(self):
        if not self.available:
            self.skipTest("calibration_report.json not found")
        self.assertGreater(self.report["after_calibration"]["precision_at_5"], 0.80)

    def test_recall_at_10_passes(self):
        if not self.available:
            self.skipTest("calibration_report.json not found")
        self.assertGreaterEqual(self.report["after_calibration"]["recall_at_10"], 0.90)

    def test_overall_pass(self):
        if not self.available:
            self.skipTest("calibration_report.json not found")
        self.assertTrue(self.report["after_calibration"]["overall_pass"])

    def test_delta_precision_positive(self):
        if not self.available:
            self.skipTest("calibration_report.json not found")
        self.assertGreater(self.report["deltas"]["precision_at_5"], 0)


if __name__ == "__main__":
    unittest.main()
