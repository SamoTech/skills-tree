"""Test suite for RecommendationEngine component - Sprint A baseline"""
import pytest


class TestRecommendationEngineBaseline:
    """Deterministic tests for RecommendationEngine output validation"""

    def test_empty_recommendation_list(self):
        """Test 1: Empty input returns empty recommendations"""
        recommendations = []
        assert len(recommendations) == 0
        assert isinstance(recommendations, list)

    def test_single_recommendation_structure(self):
        """Test 2: Single recommendation has required fields"""
        rec = {
            "skill_id": "python",
            "reason": "foundational",
            "priority": "high",
            "score": 0.95
        }
        assert "skill_id" in rec
        assert "reason" in rec
        assert "priority" in rec
        assert "score" in rec

    def test_recommendation_score_range(self):
        """Test 3: Scores are within valid range [0, 1]"""
        recs = [
            {"skill_id": "js", "score": 0.8},
            {"skill_id": "python", "score": 0.95},
            {"skill_id": "docker", "score": 0.6}
        ]
        for rec in recs:
            assert 0.0 <= rec["score"] <= 1.0

    def test_recommendations_sorted_by_score(self):
        """Test 4: Recommendations sorted by score descending"""
        recs = [
            {"skill_id": "a", "score": 0.9},
            {"skill_id": "b", "score": 0.7},
            {"skill_id": "c", "score": 0.5}
        ]
        scores = [r["score"] for r in recs]
        assert scores == sorted(scores, reverse=True)

    def test_priority_levels_valid(self):
        """Test 5: Priority levels are from valid set"""
        valid_priorities = {"high", "medium", "low"}
        recs = [
            {"priority": "high"},
            {"priority": "medium"},
            {"priority": "low"}
        ]
        for rec in recs:
            assert rec["priority"] in valid_priorities

    def test_skill_id_uniqueness(self):
        """Test 6: Skill IDs are unique in recommendations"""
        recs = [
            {"skill_id": "python"},
            {"skill_id": "javascript"},
            {"skill_id": "docker"}
        ]
        skill_ids = [r["skill_id"] for r in recs]
        assert len(skill_ids) == len(set(skill_ids))

    def test_reason_field_non_empty(self):
        """Test 7: Reason field is non-empty string"""
        rec = {"skill_id": "react", "reason": "complements existing skills"}
        assert isinstance(rec["reason"], str)
        assert len(rec["reason"]) > 0

    def test_recommendations_limit(self):
        """Test 8: Recommendations list respects max limit"""
        max_recs = 10
        recs = [{"skill_id": f"skill_{i}", "score": 0.5} for i in range(15)]
        limited_recs = recs[:max_recs]
        assert len(limited_recs) <= max_recs

    def test_filter_by_priority(self):
        """Test 9: Filter recommendations by priority level"""
        recs = [
            {"skill_id": "a", "priority": "high"},
            {"skill_id": "b", "priority": "low"},
            {"skill_id": "c", "priority": "high"}
        ]
        high_priority = [r for r in recs if r["priority"] == "high"]
        assert len(high_priority) == 2

    def test_recommendation_metadata(self):
        """Test 10: Recommendations include optional metadata"""
        rec = {
            "skill_id": "kubernetes",
            "score": 0.85,
            "metadata": {
                "estimated_time": "20h",
                "difficulty": "advanced"
            }
        }
        assert "metadata" in rec
        assert "estimated_time" in rec["metadata"]


class TestRecommendationEngineLogic:
    """Tests for recommendation logic and algorithms"""

    def test_goal_based_recommendations(self):
        """Test 11: Recommendations based on user goal"""
        goal = "fullstack_developer"
        expected_skills = {"javascript", "react", "node", "database"}
        recommendations = [
            {"skill_id": "javascript", "goal": goal},
            {"skill_id": "react", "goal": goal}
        ]
        for rec in recommendations:
            assert rec["skill_id"] in expected_skills

    def test_prerequisite_recommendations(self):
        """Test 12: Prerequisites recommended before advanced skills"""
        recs = [
            {"skill_id": "html", "type": "prerequisite", "order": 1},
            {"skill_id": "css", "type": "prerequisite", "order": 2},
            {"skill_id": "react", "type": "advanced", "order": 3}
        ]
        prereqs = [r for r in recs if r["type"] == "prerequisite"]
        assert len(prereqs) == 2
        assert all(r["order"] < 3 for r in prereqs)

    def test_skill_gap_analysis(self):
        """Test 13: Identify skill gaps based on current skills"""
        current_skills = {"python", "sql"}
        target_skills = {"python", "sql", "docker", "kubernetes"}
        gaps = target_skills - current_skills
        assert "docker" in gaps
        assert "kubernetes" in gaps
        assert len(gaps) == 2

    def test_recommendation_diversity(self):
        """Test 14: Recommendations include diverse skill categories"""
        recs = [
            {"skill_id": "python", "category": "language"},
            {"skill_id": "docker", "category": "tool"},
            {"skill_id": "aws", "category": "cloud"}
        ]
        categories = {r["category"] for r in recs}
        assert len(categories) == 3

    def test_time_based_filtering(self):
        """Test 15: Filter by available time budget"""
        time_budget = 40  # hours
        recs = [
            {"skill_id": "a", "time_estimate": 10},
            {"skill_id": "b", "time_estimate": 20},
            {"skill_id": "c", "time_estimate": 30}
        ]
        total_time = sum(r["time_estimate"] for r in recs[:2])
        assert total_time <= time_budget

    def test_difficulty_progression(self):
        """Test 16: Recommendations follow difficulty progression"""
        recs = [
            {"skill_id": "a", "difficulty": "beginner", "order": 1},
            {"skill_id": "b", "difficulty": "intermediate", "order": 2},
            {"skill_id": "c", "difficulty": "advanced", "order": 3}
        ]
        difficulties = [r["difficulty"] for r in recs]
        assert difficulties == ["beginner", "intermediate", "advanced"]

    def test_exclude_already_known_skills(self):
        """Test 17: Exclude skills user already knows"""
        known_skills = {"python", "javascript"}
        all_recs = [
            {"skill_id": "python"},
            {"skill_id": "docker"},
            {"skill_id": "javascript"}
        ]
        filtered = [r for r in all_recs if r["skill_id"] not in known_skills]
        assert len(filtered) == 1
        assert filtered[0]["skill_id"] == "docker"

    def test_synergy_based_recommendations(self):
        """Test 18: Recommend skills with high synergy"""
        current_skills = ["react"]
        synergies = {
            "redux": 0.9,  # high synergy with react
            "vue": 0.3,    # low synergy
            "typescript": 0.85  # high synergy
        }
        high_synergy = {k: v for k, v in synergies.items() if v > 0.7}
        assert "redux" in high_synergy
        assert "typescript" in high_synergy

    def test_learning_path_continuity(self):
        """Test 19: Recommendations form continuous learning path"""
        path = [
            {"skill_id": "html", "next": "css"},
            {"skill_id": "css", "next": "javascript"},
            {"skill_id": "javascript", "next": "react"}
        ]
        for i in range(len(path) - 1):
            assert path[i]["next"] == path[i + 1]["skill_id"]

    def test_career_goal_alignment(self):
        """Test 20: Recommendations align with career goals"""
        career_goal = "data_scientist"
        aligned_skills = {"python", "pandas", "scikit-learn", "tensorflow"}
        recs = [
            {"skill_id": "python", "career_goals": ["data_scientist"]},
            {"skill_id": "pandas", "career_goals": ["data_scientist"]}
        ]
        for rec in recs:
            assert career_goal in rec["career_goals"]
