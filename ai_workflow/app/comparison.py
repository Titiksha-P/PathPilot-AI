from __future__ import annotations

from .career_data import get_career
from .matcher import score_career
from .schemas import CareerComparison, CareerComparisonOption, PathwayMatch, StudentProfile


def _comparison_option(match: PathwayMatch, career: dict) -> CareerComparisonOption:
    required_skills = list(career["required_skills"])
    missing = set(match.missing_requirements)
    matched = [skill for skill in required_skills if skill not in missing]
    return CareerComparisonOption(
        career_id=career["id"],
        title=career["title"],
        match_score=match.score,
        matched_skills=matched,
        missing_skills=match.missing_requirements,
        supporting_evidence=match.evidence,
        estimated_learning_time=career["duration"],
        cost_category=career["cost"],
        salary_range=career.get("salary_range"),
        future_scope=career.get("future_scope"),
        minimum_qualification=career.get("minimum_qualification", ""),
        certifications=career.get("certifications", []),
        relevant_courses=career.get("relevant_courses", []),
        entrance_exams=career.get("entrance_exams", []),
        common_job_roles=career.get("common_job_roles", []),
        learning_resources=career.get("learning_resources", []),
        data_source=career.get("source", ""),
        risks_tradeoffs=career["tradeoffs"],
    )


def compare_careers(
    profile: StudentProfile,
    career_id_1: str,
    career_id_2: str,
) -> CareerComparison:
    """Compare two curated careers using the same evidence-based scoring engine."""

    if career_id_1 == career_id_2:
        raise ValueError("Career comparison requires two different careers")

    career_1 = get_career(career_id_1)
    career_2 = get_career(career_id_2)
    match_1 = score_career(profile, career_id_1)
    match_2 = score_career(profile, career_id_2)
    option_1 = _comparison_option(match_1, career_1)
    option_2 = _comparison_option(match_2, career_2)

    ranking_1 = (option_1.match_score, -len(option_1.missing_skills), len(option_1.matched_skills))
    ranking_2 = (option_2.match_score, -len(option_2.missing_skills), len(option_2.matched_skills))
    winner, alternative = (option_1, option_2) if ranking_1 >= ranking_2 else (option_2, option_1)

    score_difference = abs(option_1.match_score - option_2.match_score)
    decision_factors = [
        f"Match-score difference: {score_difference} points",
        f"{option_1.title}: {len(option_1.matched_skills)} matched and {len(option_1.missing_skills)} missing required skills",
        f"{option_2.title}: {len(option_2.matched_skills)} matched and {len(option_2.missing_skills)} missing required skills",
        f"Learning-time comparison: {option_1.estimated_learning_time} versus {option_2.estimated_learning_time}",
        f"Cost comparison: {option_1.cost_category} versus {option_2.cost_category}",
    ]
    recommendation_reason = (
        f"{winner.title} is the stronger current fit because it scores {winner.match_score}% "
        f"against {alternative.match_score}% and requires fewer or comparable skill gaps. "
        "This is a profile-fit recommendation, not a guarantee of admission or employment."
    )

    return CareerComparison(
        career_1=option_1,
        career_2=option_2,
        better_fit_career_id=winner.career_id,
        recommendation_reason=recommendation_reason,
        decision_factors=decision_factors,
    )
