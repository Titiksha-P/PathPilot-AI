from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping


PHASES = (
    (1, 30, "Foundation"),
    (31, 60, "Applied Practice"),
    (61, 90, "Portfolio & Readiness"),
)


def build_90_day_roadmap(
    career_name: str,
    missing_skills: Iterable[str],
    learning_resources: Mapping[str, List[Dict[str, Any]]],
) -> Dict[str, Any]:
    skills = [skill.strip() for skill in missing_skills if skill and skill.strip()]
    if not skills:
        raise ValueError("At least one missing skill is required")

    milestones: List[Dict[str, Any]] = []
    for index, (start_day, end_day, phase_name) in enumerate(PHASES):
        selected_skills = skills[index::len(PHASES)] or [skills[index % len(skills)]]
        resources = []
        for skill in selected_skills:
            resources.extend(learning_resources.get(skill, [])[:2])

        milestones.append(
            {
                "phase": phase_name,
                "start_day": start_day,
                "end_day": end_day,
                "focus_skills": selected_skills,
                "recommended_resources": resources,
                "deliverable": _deliverable_for_phase(index, career_name),
                "success_check": _success_check_for_phase(index),
            }
        )

    return {
        "career_name": career_name,
        "duration_days": 90,
        "milestones": milestones,
        "review_points": [30, 60, 90],
        "adaptation_rule": (
            "Recalculate priorities after each review using completed milestones and student feedback."
        ),
    }


def _deliverable_for_phase(index: int, career_name: str) -> str:
    deliverables = (
        f"Complete core foundations required for {career_name}",
        f"Finish one guided practical project related to {career_name}",
        f"Publish one portfolio-ready outcome and prepare an evidence-based next-step plan",
    )
    return deliverables[index]


def _success_check_for_phase(index: int) -> str:
    checks = (
        "Can explain the foundational concepts and complete a short assessment.",
        "Can apply the skills independently to a realistic task.",
        "Can demonstrate the work, reflect on gaps, and select the next milestone.",
    )
    return checks[index]
