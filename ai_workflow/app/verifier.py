from __future__ import annotations

from .datasets import all_pathway_ids
from .schemas import PathwayRecommendations, StudentProfile, VerificationResult


def verify_guidance(profile: StudentProfile, recommendations: PathwayRecommendations) -> VerificationResult:
    issues: list[str] = []
    matches = recommendations.matches
    scores = [match.score for match in matches]

    if len(matches) != 3:
        issues.append("Exactly three pathways are required")
    if scores != sorted(scores, reverse=True):
        issues.append("Scores are not ordered from highest to lowest")
    if len({match.pathway_id for match in matches}) != len(matches):
        issues.append("Duplicate pathways were returned")

    expected_roles = ["best_fit", "strong_alternative", "safe_backup"]
    if [match.rank_role for match in matches] != expected_roles:
        issues.append("Rank roles must be best_fit, strong_alternative, and safe_backup")

    known_ids = all_pathway_ids()
    expected_type = {"class10": "stream", "class12": "course", "college": "career"}[profile.stage]

    for match in matches:
        if match.pathway_id not in known_ids:
            issues.append(f"{match.title} is an unknown pathway")
        if match.pathway_type != expected_type:
            issues.append(f"{match.title} has the wrong pathway type for {profile.stage}")
        if not match.evidence:
            issues.append(f"{match.title} has no supporting evidence")
        if not match.reasons:
            issues.append(f"{match.title} has no explanation")
        if not match.eligibility_reasons:
            issues.append(f"{match.title} has no eligibility explanation")
        if match.eligibility_status == "not_eligible" and not match.missing_requirements:
            issues.append(f"{match.title} is marked not eligible without missing requirements")
        if not match.next_actions:
            issues.append(f"{match.title} has no next actions")
        if not match.estimated_duration:
            issues.append(f"{match.title} has no duration")
        if not match.cost_category:
            issues.append(f"{match.title} has no cost category")
        if match.score > 70 and not match.matched_attributes:
            issues.append(f"{match.title} has a high score without matched attributes")

    return VerificationResult(
        approved=not issues,
        issues=issues,
        final_recommendations=recommendations,
    )


# Backward-compatible wrapper retained for old imports.
def verify_recommendations(profile: StudentProfile, recommendations: PathwayRecommendations) -> VerificationResult:
    return verify_guidance(profile, recommendations)
