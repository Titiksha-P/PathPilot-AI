from __future__ import annotations

from typing import Any, Dict, List


REQUIRED_STUDENT_FIELDS = {
    "student_id",
    "education_level",
    "interests",
    "skills",
    "preferred_subjects",
    "career_goals",
    "learning_preferences",
    "constraints",
}

REQUIRED_RECOMMENDATION_FIELDS = {
    "career_id",
    "career_name",
    "match_score",
    "confidence",
    "reasons",
    "matched_skills",
    "missing_skills",
    "recommended_courses",
    "next_steps",
}


def validate_student_profile(profile: Dict[str, Any]) -> None:
    missing = REQUIRED_STUDENT_FIELDS - set(profile)
    if missing:
        raise ValueError(f"Student profile is missing fields: {sorted(missing)}")

    for key in ("interests", "skills", "preferred_subjects", "career_goals"):
        if not isinstance(profile[key], list):
            raise TypeError(f"{key} must be a list")


def validate_recommendation_payload(payload: Dict[str, Any]) -> None:
    recommendations = payload.get("recommendations")
    if not isinstance(recommendations, list) or not recommendations:
        raise ValueError("recommendations must be a non-empty list")

    for index, recommendation in enumerate(recommendations):
        missing = REQUIRED_RECOMMENDATION_FIELDS - set(recommendation)
        if missing:
            raise ValueError(
                f"Recommendation {index} is missing fields: {sorted(missing)}"
            )


def create_frontend_response(
    student_id: str,
    recommendations: List[Dict[str, Any]],
    comparison: Dict[str, Any] | None = None,
    roadmap: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    response = {
        "student_id": student_id,
        "recommendations": recommendations,
        "comparison": comparison,
        "roadmap": roadmap,
        "meta": {
            "schema_version": "1.0.0",
            "explainable": True,
        },
    }
    validate_recommendation_payload(response)
    return response
