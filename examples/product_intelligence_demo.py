from pprint import pprint

from src.product_intelligence import (
    build_90_day_roadmap,
    build_explanation,
    calculate_career_score,
    compare_careers,
    create_frontend_response,
    rank_careers,
    validate_student_profile,
)


student = {
    "student_id": "STU-001",
    "education_level": "Class 12",
    "interests": ["technology", "design"],
    "skills": ["creativity", "basic coding"],
    "preferred_subjects": ["computer science"],
    "career_goals": ["high-growth career"],
    "learning_preferences": {"format": "project-based"},
    "constraints": {"weekly_hours": 8},
}
validate_student_profile(student)

uiux = calculate_career_score(
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

data = calculate_career_score(
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

ranked = rank_careers([uiux, data], limit=2)
recommendations = [
    {
        "career_id": item.career_id,
        "career_name": item.career_name,
        "match_score": item.total_score,
        "confidence": item.confidence,
        "reasons": build_explanation(item),
        "matched_skills": ["creativity", "basic coding"],
        "missing_skills": ["Figma", "user research", "prototyping"],
        "recommended_courses": ["Figma Fundamentals", "UX Research Basics"],
        "next_steps": ["Create a wireframe", "Run one user interview"],
    }
    for item in ranked
]

comparison = compare_careers(
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

roadmap = build_90_day_roadmap(
    "UI/UX Designer",
    ["Figma", "user research", "prototyping"],
    {
        "Figma": [{"title": "Figma Fundamentals", "type": "course"}],
        "user research": [{"title": "Interview Practice", "type": "exercise"}],
        "prototyping": [{"title": "Prototype Sprint", "type": "project"}],
    },
)

pprint(
    create_frontend_response(
        student_id=student["student_id"],
        recommendations=recommendations,
        comparison=comparison,
        roadmap=roadmap,
    )
)
