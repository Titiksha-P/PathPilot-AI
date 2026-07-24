from __future__ import annotations

from .comparison import compare_careers
from .matcher import rank_pathways
from .roadmap import generate_90_day_roadmap
from .schemas import CareerDecisionSimulation, GuidanceResult, StudentProfile
from .skill_gaps import analyze_skill_gaps
from .verifier import verify_guidance


def run_guidance(profile: StudentProfile) -> GuidanceResult:
    """Run deterministic matching, eligibility, ranking and verification."""

    recommendations = rank_pathways(profile)
    verification = verify_guidance(profile, recommendations)
    return GuidanceResult(
        profile=profile,
        recommendations=recommendations,
        verification=verification,
    )



def run_decision_simulator(
    profile: StudentProfile,
    career_id_1: str | None = None,
    career_id_2: str | None = None,
    roadmap_career_id: str | None = None,
) -> CareerDecisionSimulation:
    """Run the complete career decision flow for a college-stage profile."""

    if profile.stage != "college":
        raise ValueError("The career decision simulator currently requires a college-stage profile")

    guidance = run_guidance(profile)
    first, second = guidance.recommendations.matches[:2]
    comparison = compare_careers(
        profile,
        career_id_1 or first.pathway_id,
        career_id_2 or second.pathway_id,
    )
    target_career_id = roadmap_career_id or first.pathway_id
    gaps = analyze_skill_gaps(profile, target_career_id)
    roadmap = generate_90_day_roadmap(profile, target_career_id)
    return CareerDecisionSimulation(
        profile=profile,
        recommendations=guidance.recommendations,
        comparison=comparison,
        skill_gap_analysis=gaps,
        roadmap_90_days=roadmap,
        verification=guidance.verification,
    )
