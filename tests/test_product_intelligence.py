import unittest

from src.product_intelligence import (
    build_90_day_roadmap,
    build_explanation,
    calculate_career_score,
    compare_careers,
    create_frontend_response,
    rank_careers,
    validate_student_profile,
)


class ProductIntelligenceTests(unittest.TestCase):
    def test_student_profile_contract(self):
        validate_student_profile(
            {
                "student_id": "STU-001",
                "education_level": "Class 12",
                "interests": ["technology", "design"],
                "skills": ["creativity", "basic coding"],
                "preferred_subjects": ["computer science"],
                "career_goals": ["high-growth career"],
                "learning_preferences": {"format": "project-based"},
                "constraints": {"weekly_hours": 8},
            }
        )

    def test_scoring_and_ranking(self):
        design = calculate_career_score(
            "career-uiux",
            "UI/UX Designer",
            {
                "interest_match": 95,
                "skill_match": 78,
                "education_match": 88,
                "goal_match": 90,
                "learning_preference_match": 92,
                "future_demand": 84,
                "constraint_fit": 87,
            },
        )
        analyst = calculate_career_score(
            "career-data",
            "Data Analyst",
            {
                "interest_match": 76,
                "skill_match": 72,
                "education_match": 88,
                "goal_match": 85,
                "learning_preference_match": 74,
                "future_demand": 91,
                "constraint_fit": 80,
            },
        )
        ranked = rank_careers([analyst, design])
        self.assertEqual(ranked[0].career_name, "UI/UX Designer")
        self.assertEqual(len(build_explanation(design)), 3)

    def test_comparison(self):
        result = compare_careers(
            {
                "career_name": "UI/UX Designer",
                "comparison_scores": {
                    "personal_fit": 92,
                    "current_readiness": 76,
                    "learning_effort": 80,
                    "education_compatibility": 90,
                    "future_opportunity": 84,
                    "constraint_fit": 88,
                },
            },
            {
                "career_name": "Data Analyst",
                "comparison_scores": {
                    "personal_fit": 77,
                    "current_readiness": 73,
                    "learning_effort": 70,
                    "education_compatibility": 91,
                    "future_opportunity": 92,
                    "constraint_fit": 82,
                },
            },
        )
        self.assertIn(result["overall_recommendation"], {"UI/UX Designer", "Data Analyst", "balanced"})

    def test_roadmap_and_response(self):
        roadmap = build_90_day_roadmap(
            "UI/UX Designer",
            ["Figma", "user research", "prototyping"],
            {
                "Figma": [{"title": "Figma Fundamentals", "type": "course"}],
                "user research": [{"title": "Interview Practice", "type": "exercise"}],
                "prototyping": [{"title": "Prototype Sprint", "type": "project"}],
            },
        )
        self.assertEqual(len(roadmap["milestones"]), 3)

        response = create_frontend_response(
            "STU-001",
            [
                {
                    "career_id": "career-uiux",
                    "career_name": "UI/UX Designer",
                    "match_score": 91,
                    "confidence": 88,
                    "reasons": ["Strong creative alignment"],
                    "matched_skills": ["creativity"],
                    "missing_skills": ["Figma"],
                    "recommended_courses": ["Figma Fundamentals"],
                    "next_steps": ["Build one wireframe"],
                }
            ],
            roadmap=roadmap,
        )
        self.assertEqual(response["meta"]["schema_version"], "1.0.0")


if __name__ == "__main__":
    unittest.main()
