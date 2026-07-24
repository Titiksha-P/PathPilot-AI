from __future__ import annotations

from .career_data import get_career
from .schemas import LearningRoadmap90Day, RoadmapPhase, RoadmapTask, StudentProfile
from .skill_gaps import analyze_skill_gaps


def _skills_or_strengths(gaps: list[str], strengths: list[str]) -> list[str]:
    selected = gaps[:3] or strengths[:3]
    return selected or ["career fundamentals"]


def generate_90_day_roadmap(profile: StudentProfile, career_id: str) -> LearningRoadmap90Day:
    """Generate a deterministic, profile-grounded 90-day learning roadmap."""

    career = get_career(career_id)
    analysis = analyze_skill_gaps(profile, career_id)
    gap_names = [gap.skill for gap in analysis.gaps]
    focus_skills = _skills_or_strengths(gap_names, analysis.matched_skills)
    primary_skill = focus_skills[0]
    secondary_skills = focus_skills[1:] or analysis.matched_skills[:2]
    project_action = career["next_actions"][0]
    evidence_source = profile.projects[0].name if profile.projects else profile.current_class_or_program or "current profile"

    phases = [
        RoadmapPhase(
            phase_id="foundations",
            day_range="Days 1–30",
            focus=f"Build foundations in {', '.join(focus_skills)}.",
            tasks=[
                RoadmapTask(
                    title=f"Learn {primary_skill} fundamentals",
                    objective=f"Close the highest-priority gap for {career['title']}.",
                    actions=[
                        f"Study the core concepts and terminology of {primary_skill}.",
                        f"Complete at least three hands-on exercises using {primary_skill}.",
                        "Record mistakes, corrections, and evidence of progress in a learning log.",
                    ],
                    deliverable=f"A reviewed fundamentals notebook or mini-demo proving basic {primary_skill} ability.",
                    related_skills=[primary_skill],
                ),
                RoadmapTask(
                    title="Connect new learning to existing strengths",
                    objective=f"Reuse evidence from {evidence_source} instead of starting from zero.",
                    actions=[
                        "List the current skills and project evidence that transfer to this career.",
                        f"Add one small feature that combines an existing strength with {primary_skill}.",
                    ],
                    deliverable="A one-page skill map linking existing evidence to the target career.",
                    related_skills=analysis.matched_skills[:3],
                ),
            ],
            success_check=f"Explain the basics of {primary_skill} and show one working artifact without unsupported claims.",
        ),
        RoadmapPhase(
            phase_id="applied_project",
            day_range="Days 31–60",
            focus=f"Apply {', '.join(focus_skills)} in one evidence-based project.",
            tasks=[
                RoadmapTask(
                    title=f"Build a {career['title']} portfolio project",
                    objective="Convert learning into demonstrable portfolio evidence.",
                    actions=[
                        project_action,
                        f"Include at least one measurable use of {primary_skill}.",
                        "Add input validation, failure handling, and a short test checklist.",
                    ],
                    deliverable="A working project repository with README, screenshots or output, and test evidence.",
                    related_skills=focus_skills,
                ),
                RoadmapTask(
                    title="Evaluate the project against career requirements",
                    objective="Check whether the project proves the required skills rather than only mentioning them.",
                    actions=[
                        "Map each required career skill to a concrete project file, feature, or result.",
                        "Identify one remaining weak skill and improve the project to address it.",
                    ],
                    deliverable="A requirement-to-evidence checklist with no invented experience.",
                    related_skills=career["required_skills"],
                ),
            ],
            success_check="A reviewer can run or inspect the project and find evidence for the mapped skills.",
        ),
        RoadmapPhase(
            phase_id="portfolio_readiness",
            day_range="Days 61–90",
            focus="Package evidence, validate readiness, and prepare the next application or education step.",
            tasks=[
                RoadmapTask(
                    title="Create the final portfolio case study",
                    objective="Explain the problem, decisions, implementation, evidence, limitations, and outcome.",
                    actions=[
                        "Write a concise case study using the completed project.",
                        "Add a skills section that links every claim to evidence.",
                        "Document limitations, risks, and the next technical improvement.",
                    ],
                    deliverable="A publishable portfolio case study and updated resume/project section.",
                    related_skills=analysis.matched_skills + focus_skills,
                ),
                RoadmapTask(
                    title="Run a readiness review",
                    objective=f"Test readiness for the next {career['title']} opportunity.",
                    actions=[
                        "Repeat the career match using the updated profile evidence.",
                        "Practice explaining the project and three technical decisions.",
                        "Choose one verified next step from the career dataset or backend-provided resources.",
                    ],
                    deliverable="A final readiness score, remaining-gap list, and next 30-day action decision.",
                    related_skills=secondary_skills,
                ),
            ],
            success_check="The profile contains a tested project, an evidence-backed case study, and an updated remaining-gap list.",
        ),
    ]

    return LearningRoadmap90Day(
        career_id=career["id"],
        career_title=career["title"],
        starting_readiness_score=analysis.readiness_score,
        target_outcome=f"Evidence-ready beginner profile for the next {career['title']} learning, internship, or project opportunity.",
        phases=phases,
    )
