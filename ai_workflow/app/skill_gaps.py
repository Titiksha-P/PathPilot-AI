from __future__ import annotations

from .career_data import get_career
from .matcher import score_career
from .schemas import SkillGap, SkillGapAnalysis, StudentProfile


def analyze_skill_gaps(profile: StudentProfile, career_id: str) -> SkillGapAnalysis:
    """Turn required-but-unproven career skills into prioritized learning gaps."""

    career = get_career(career_id)
    match = score_career(profile, career_id)
    missing = list(match.missing_requirements)
    matched = [skill for skill in career["required_skills"] if skill not in set(missing)]

    gaps: list[SkillGap] = []
    for index, skill in enumerate(missing):
        if index < 2:
            priority = "high"
        elif index < 4:
            priority = "medium"
        else:
            priority = "low"
        gaps.append(
            SkillGap(
                skill=skill,
                priority=priority,
                current_evidence=[],
                why_needed=f"{skill.title()} is listed as a required skill for {career['title']} in the curated career record.",
                recommended_action=f"Complete a focused {skill} learning module and demonstrate it in a small project artifact.",
            )
        )

    strengths = [
        attribute
        for attribute in match.matched_attributes
        if attribute in matched or attribute in career["preferred_contexts"]
    ]
    if not strengths:
        strengths = matched

    return SkillGapAnalysis(
        career_id=career["id"],
        career_title=career["title"],
        readiness_score=match.score,
        matched_skills=matched,
        gaps=gaps,
        strengths_to_use=list(dict.fromkeys(strengths))[:6],
    )
