from __future__ import annotations

import csv
import re
from pathlib import Path

_DATASET_PATH = Path(__file__).resolve().parents[1] / "data" / "career_dataset.csv"


def _slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return re.sub(r"_+", "_", value).strip("_")


def _split_list(value: str) -> list[str]:
    if not value or value.strip().lower() in {"none", "n/a", "na", "not exam-gated"}:
        return []
    parts = re.split(r"\s*,\s*|\s*;\s*", value.strip())
    return [part.strip() for part in parts if part.strip()]


def _terms(value: str) -> list[str]:
    if not value:
        return []
    pieces = re.split(r"[/,&()]|\bor\b|\band\b", value, flags=re.IGNORECASE)
    return [piece.strip() for piece in pieces if piece.strip()]


def _next_actions(row: dict[str, str], skills: list[str], resources: list[str]) -> list[str]:
    actions: list[str] = []
    if skills:
        actions.append("Build evidence for the core skills: " + ", ".join(skills[:4]))
    courses = row.get("Relevant Courses / Degrees", "").strip()
    if courses:
        actions.append("Review relevant study routes: " + courses)
    if resources:
        actions.append("Start with the dataset resources: " + ", ".join(resources[:3]))
    exams = row.get("Entrance Exams", "").strip()
    if exams and exams.lower() not in {"none", "n/a", "not exam-gated, portfolio based"}:
        actions.append("Check applicable entrance or qualifying exams: " + exams)
    return actions or ["Create one evidence-based portfolio artifact for this career"]


def _load_careers(path: Path = _DATASET_PATH) -> list[dict]:
    if not path.exists():
        raise RuntimeError(f"Career dataset not found: {path}")

    careers: list[dict] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            title = row["Career Option"].strip()
            category = row["Field / Domain"].strip()
            skills = _split_list(row["Required Skills"])
            resources = _split_list(row["Recommended Learning Resources"])
            job_roles = _split_list(row["Common Job Roles"])
            courses = _split_list(row["Relevant Courses / Degrees"])
            exams = _split_list(row["Entrance Exams"])
            certifications = _split_list(row["Certifications (Optional/Recommended)"])
            minimum_qualification = row["Minimum Qualification"].strip()
            salary_range = row["Salary Range (India, per annum)"].strip()
            future_scope = row["Why It's Trending (2026)"].strip()

            career_id = _slugify(title)
            interest_tags = list(dict.fromkeys([category, *_terms(category), *_terms(title)]))
            education_terms = list(
                dict.fromkeys(
                    [
                        minimum_qualification,
                        *_terms(minimum_qualification),
                        *courses,
                        *(term for course in courses for term in _terms(course)),
                    ]
                )
            )
            project_types = [f"{title} project", f"{category} project", *job_roles[:2]]
            preferred_contexts = list(dict.fromkeys([*skills, category, *job_roles[:3]]))

            qualification_note = (
                f"Minimum qualification in dataset: {minimum_qualification}"
                if minimum_qualification
                else "Minimum qualification is not specified in the dataset"
            )
            exam_note = (
                f"Entrance/qualifying exams in dataset: {row['Entrance Exams'].strip()}"
                if row["Entrance Exams"].strip()
                else "Entrance/qualifying exams are not specified in the dataset"
            )

            careers.append(
                {
                    "id": career_id,
                    "title": title,
                    "category": category,
                    "required_skills": skills,
                    "preferred_contexts": preferred_contexts,
                    "project_types": project_types,
                    "interest_tags": interest_tags,
                    "education_terms": education_terms,
                    "duration": "Not specified in the supplied career dataset",
                    "cost": "Not specified in the supplied career dataset",
                    "tradeoffs": [qualification_note, exam_note],
                    "next_actions": _next_actions(row, skills, resources),
                    "salary_range": salary_range or None,
                    "future_scope": future_scope or None,
                    "minimum_qualification": minimum_qualification,
                    "certifications": certifications,
                    "relevant_courses": courses,
                    "entrance_exams": exams,
                    "common_job_roles": job_roles,
                    "learning_resources": resources,
                    "source": path.name,
                }
            )

    if not careers:
        raise RuntimeError(f"Career dataset contains no records: {path}")
    return careers


CAREERS: list[dict] = _load_careers()

# Temporary aliases keep older backend calls from crashing while the team migrates
# to the stable IDs generated from the shared CSV career titles.
CAREER_ID_ALIASES = {
    "ai_agent_developer": "prompt_engineer_genai_specialist",
    "ai_automation_engineer": "prompt_engineer_genai_specialist",
    "workflow_automation_specialist": "prompt_engineer_genai_specialist",
    "data_analyst": "data_scientist",
    "junior_data_scientist": "data_scientist",
    "machine_learning_engineer": "ai_ml_engineer",
    "python_backend_developer": "full_stack_developer",
    "product_analyst": "business_analyst",
}


def get_career(career_id: str) -> dict:
    """Return one career record from the bundled team CSV by stable ID."""

    canonical_id = CAREER_ID_ALIASES.get(career_id, career_id)
    for career in CAREERS:
        if career["id"] == canonical_id:
            return career
    raise ValueError(f"Unknown career: {career_id}")
