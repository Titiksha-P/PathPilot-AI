from __future__ import annotations

from typing import Any

from .comparison import compare_careers
from .orchestrator import run_decision_simulator, run_guidance
from .roadmap import generate_90_day_roadmap
from .schemas import StudentProfile
from .skill_gaps import analyze_skill_gaps

ProfileInput = StudentProfile | dict[str, Any]


def _profile(value: ProfileInput) -> StudentProfile:
    if isinstance(value, StudentProfile):
        return value
    return StudentProfile.model_validate(value)


def analyze_student(profile: ProfileInput) -> dict[str, Any]:
    """Backend adapter for profile analysis and ranked recommendations."""

    return run_guidance(_profile(profile)).model_dump(mode="json")


def compare_two_careers(
    profile: ProfileInput,
    career_id_1: str,
    career_id_2: str,
) -> dict[str, Any]:
    return compare_careers(_profile(profile), career_id_1, career_id_2).model_dump(mode="json")


def get_skill_gap_analysis(profile: ProfileInput, career_id: str) -> dict[str, Any]:
    return analyze_skill_gaps(_profile(profile), career_id).model_dump(mode="json")


def generate_roadmap(profile: ProfileInput, career_id: str) -> dict[str, Any]:
    return generate_90_day_roadmap(_profile(profile), career_id).model_dump(mode="json")


def run_complete_flow(
    profile: ProfileInput,
    career_id_1: str | None = None,
    career_id_2: str | None = None,
    roadmap_career_id: str | None = None,
) -> dict[str, Any]:
    return run_decision_simulator(
        _profile(profile),
        career_id_1=career_id_1,
        career_id_2=career_id_2,
        roadmap_career_id=roadmap_career_id,
    ).model_dump(mode="json")
