from __future__ import annotations

import re
from collections.abc import Iterable

from .career_data import CAREERS, get_career
from .datasets import COURSE_PATHWAYS, STREAM_PATHWAYS, get_course
from .schemas import PathwayMatch, PathwayRecommendations, StudentProfile

ALIASES = {
    "llama 3.2": "llm",
    "ollama": "local llm",
    "generative ai tools": "llm",
    "gmail api": "api integration",
    "microsoft copilot": "ai agents",
    "copilot agents": "ai agents",
    "n8n workflows": "n8n",
    "data science fundamentals": "data science",
    "ux analysis": "user research",
    "power bi": "data visualization",
    "pandas": "data analysis",
    "sqlite": "database",
    "science (pcm)": "science pcm",
    "science (pcb)": "science pcb",
    "science (pcmb)": "science pcmb",
}


def normalize(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9+#. ]+", " ", value.lower())
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return ALIASES.get(cleaned, cleaned)


def _tokens(values: Iterable[str]) -> set[str]:
    return {normalize(value) for value in values if value and normalize(value)}


def _contains(feature_set: set[str], target: str) -> bool:
    target_norm = normalize(target)
    if target_norm in feature_set:
        return True

    def phrase_contains(haystack: str, needle: str) -> bool:
        if not haystack or not needle:
            return False
        pattern = rf"(?<![a-z0-9+#.]){re.escape(needle)}(?![a-z0-9+#.])"
        return re.search(pattern, haystack) is not None

    return any(
        phrase_contains(item, target_norm) or phrase_contains(target_norm, item)
        for item in feature_set
        if item
    )


def _value_by_normalized_key(values: dict[str, float], key: str) -> float | None:
    target = normalize(key)
    for raw_key, score in values.items():
        if normalize(raw_key) == target:
            return score
    return None


def _weighted_percentage(values: dict[str, float], weights: dict[str, float]) -> float:
    weighted_sum = 0.0
    total_weight = 0.0
    for key, weight in weights.items():
        score = _value_by_normalized_key(values, key)
        if score is not None:
            weighted_sum += score * weight
            total_weight += weight
    return weighted_sum / total_weight if total_weight else 0.0


def _overlap_score(values: Iterable[str], targets: Iterable[str]) -> tuple[float, list[str]]:
    value_set = _tokens(values)
    target_list = list(targets)
    matched = [target for target in target_list if _contains(value_set, target)]
    return len(matched) / max(1, len(target_list)), matched


def _budget_score(profile_budget: str, pathway_cost: str) -> float:
    budget_order = {"low": 1, "medium": 2, "high": 3}
    cost_level = {
        "low": 1,
        "low-medium": 1.5,
        "medium": 2,
        "high": 3,
    }.get(pathway_cost, 2)
    available = budget_order.get(profile_budget, 2)
    if cost_level <= available:
        return 1.0
    if cost_level - available <= 1:
        return 0.45
    return 0.1


def _select_top_three(ranked: list[PathwayMatch]) -> PathwayRecommendations:
    if len(ranked) < 3:
        raise ValueError("At least three pathways are required")

    ranked = sorted(ranked, key=lambda item: (-item.score, item.title))
    selected = ranked[:2]
    remaining = ranked[2:]
    affordable = [
        item
        for item in remaining
        if item.cost_category in {"low", "low-medium", "medium"}
        and item.eligibility_status != "not_eligible"
    ]
    selected.append(affordable[0] if affordable else remaining[0])

    roles = ["best_fit", "strong_alternative", "safe_backup"]
    selected = [item.model_copy(update={"rank_role": role}) for item, role in zip(selected, roles, strict=True)]
    return PathwayRecommendations(matches=selected)


def _score_stream(profile: StudentProfile, pathway: dict) -> PathwayMatch:
    academic = _weighted_percentage(profile.marks, pathway["subject_weights"]) / 100
    aptitude = _weighted_percentage(profile.aptitude, pathway["aptitude_weights"]) / 100
    interest, matched_interests = _overlap_score(profile.interests, pathway["interest_tags"])
    work_style, matched_styles = _overlap_score(profile.preferences.work_styles, pathway["work_styles"])
    budget = _budget_score(profile.preferences.budget, pathway["cost"])

    missing: list[str] = []
    for subject, minimum in pathway["min_subjects"].items():
        actual = _value_by_normalized_key(profile.marks, subject)
        if actual is None:
            missing.append(f"Provide {subject.title()} marks")
        elif actual < minimum:
            missing.append(f"Raise {subject.title()} from {actual:g}% toward {minimum}%+")

    status = "eligible" if not missing else "conditionally_eligible"
    eligibility_reasons = [
        "Current Class 10 subject profile meets this prototype's guidance threshold"
        if not missing
        else "The path remains possible, but the listed academic gaps should be addressed"
    ]

    raw = academic * 35 + aptitude * 30 + interest * 20 + work_style * 5 + budget * 10
    if status == "conditionally_eligible":
        raw -= 8
    score = round(max(0, min(100, raw)))

    evidence = []
    strongest_marks = sorted(profile.marks.items(), key=lambda item: item[1], reverse=True)[:2]
    if strongest_marks:
        evidence.append("Academic evidence: " + ", ".join(f"{name} {value:g}%" for name, value in strongest_marks))
    strongest_aptitude = sorted(profile.aptitude.items(), key=lambda item: item[1], reverse=True)[:2]
    if strongest_aptitude:
        evidence.append("Aptitude evidence: " + ", ".join(f"{name} {value:g}%" for name, value in strongest_aptitude))
    if matched_interests:
        evidence.append("Interest evidence: " + ", ".join(matched_interests))

    reasons = [f"Academic alignment contributes {round(academic * 35)} of 35 points"]
    if matched_interests:
        reasons.append("Interests align with " + ", ".join(matched_interests))
    if matched_styles:
        reasons.append("Preferred work style aligns with " + ", ".join(matched_styles))

    return PathwayMatch(
        pathway_id=pathway["id"],
        pathway_type="stream",
        title=pathway["title"],
        score=score,
        reasons=reasons,
        evidence=evidence or ["Profile contains preliminary academic and aptitude evidence"],
        matched_attributes=[*matched_interests, *matched_styles],
        eligibility_status=status,
        eligibility_reasons=eligibility_reasons,
        missing_requirements=missing,
        risks_tradeoffs=pathway["tradeoffs"],
        estimated_duration=pathway["duration"],
        cost_category=pathway["cost"],
        next_actions=pathway["next_actions"],
        related_outcomes=pathway["outcomes"],
    )


def evaluate_course_eligibility(profile: StudentProfile, course_id: str) -> tuple[str, list[str], list[str]]:
    course = get_course(course_id)
    missing: list[str] = []
    reasons: list[str] = []
    profile_stream = normalize(profile.stream)
    allowed_streams = {normalize(item) for item in course["required_streams"]}

    if "any" not in allowed_streams and profile_stream not in allowed_streams:
        missing.append(f"Required stream: {', '.join(course['required_streams']).upper()}")

    for subject in course["required_subjects"]:
        if _value_by_normalized_key(profile.marks, subject) is None:
            missing.append(f"Required subject: {subject.title()}")

    overall = _value_by_normalized_key(profile.marks, "overall")
    if overall is not None and overall < course["min_overall"]:
        missing.append(f"Overall marks should be at least {course['min_overall']}%")

    for subject, minimum in course["min_subject_marks"].items():
        actual = _value_by_normalized_key(profile.marks, subject)
        if actual is not None and actual < minimum:
            missing.append(f"{subject.title()} should be at least {minimum}%")

    hard_missing = [item for item in missing if "Required" in item or "at least" in item]
    if hard_missing:
        status = "not_eligible"
        reasons.append("Current academic profile does not meet one or more prototype eligibility rules")
    else:
        missing_exams = [
            exam.upper()
            for exam in course["entrance_exams"]
            if _value_by_normalized_key(profile.entrance_readiness, exam) is None
        ]
        if missing_exams:
            status = "conditionally_eligible"
            missing.extend(f"Prepare for entrance exam: {exam}" for exam in missing_exams)
            reasons.append("Academic requirements are met, but entrance preparation is not recorded")
        else:
            status = "eligible"
            reasons.append("Current academic subjects and recorded entrance readiness satisfy the prototype rules")

    return status, reasons, missing


def _score_course(profile: StudentProfile, course: dict) -> PathwayMatch:
    status, eligibility_reasons, missing = evaluate_course_eligibility(profile, course["id"])

    required_marks = list(course["min_subject_marks"])
    mark_values = [
        score
        for subject in required_marks
        if (score := _value_by_normalized_key(profile.marks, subject)) is not None
    ]
    overall = _value_by_normalized_key(profile.marks, "overall")
    academic = (sum(mark_values) / len(mark_values) if mark_values else (overall or 50)) / 100

    aptitude_values = [
        score
        for tag in course["aptitude_tags"]
        if (score := _value_by_normalized_key(profile.aptitude, tag)) is not None
    ]
    aptitude = (sum(aptitude_values) / len(aptitude_values) if aptitude_values else 50) / 100
    interest, matched_interests = _overlap_score(profile.interests, course["interest_tags"])
    budget = _budget_score(profile.preferences.budget, course["cost"])

    entrance_scores = [
        score
        for exam in course["entrance_exams"]
        if (score := _value_by_normalized_key(profile.entrance_readiness, exam)) is not None
    ]
    entrance = (sum(entrance_scores) / len(entrance_scores) / 100) if entrance_scores else (1.0 if not course["entrance_exams"] else 0.25)

    raw = academic * 35 + aptitude * 25 + interest * 20 + entrance * 10 + budget * 10
    if status == "not_eligible":
        raw -= 35
    elif status == "conditionally_eligible":
        raw -= 10
    score = round(max(0, min(100, raw)))

    evidence = []
    relevant_marks = [(subject, _value_by_normalized_key(profile.marks, subject)) for subject in course["required_subjects"]]
    relevant_marks = [(subject, value) for subject, value in relevant_marks if value is not None]
    if relevant_marks:
        evidence.append("Relevant marks: " + ", ".join(f"{subject.title()} {value:g}%" for subject, value in relevant_marks))
    if matched_interests:
        evidence.append("Interest evidence: " + ", ".join(matched_interests))
    if entrance_scores:
        evidence.append("Recorded entrance readiness: " + ", ".join(f"{exam.upper()} {_value_by_normalized_key(profile.entrance_readiness, exam):g}%" for exam in course["entrance_exams"] if _value_by_normalized_key(profile.entrance_readiness, exam) is not None))

    reasons = [f"Academic profile contributes {round(academic * 35)} of 35 points"]
    if matched_interests:
        reasons.append("Interests align with " + ", ".join(matched_interests))
    reasons.append(f"Eligibility check: {status.replace('_', ' ')}")

    return PathwayMatch(
        pathway_id=course["id"],
        pathway_type="course",
        title=course["title"],
        score=score,
        reasons=reasons,
        evidence=evidence or ["Current stream and overall marks provide preliminary evidence"],
        matched_attributes=matched_interests,
        eligibility_status=status,
        eligibility_reasons=eligibility_reasons,
        missing_requirements=missing,
        risks_tradeoffs=course["tradeoffs"],
        estimated_duration=course["duration"],
        cost_category=course["cost"],
        next_actions=course["next_actions"],
        related_outcomes=course["outcomes"],
    )


def _profile_features(profile: StudentProfile) -> dict[str, set[str]]:
    skills = _tokens(skill.name for skill in profile.skills)
    contexts = _tokens(context for skill in profile.skills for context in skill.contexts)
    project_tech = _tokens(tech for project in profile.projects for tech in project.technologies)
    capabilities = _tokens(capability for project in profile.projects for capability in project.capabilities)
    project_text = _tokens([project.name for project in profile.projects] + [project.summary for project in profile.projects])
    interests = _tokens(profile.interests)
    education = _tokens([item.field for item in profile.education] + [item.qualification for item in profile.education])
    return {
        "skills": skills | project_tech,
        "contexts": contexts | capabilities | project_text,
        "interests": interests,
        "education": education,
        "searchable": skills | contexts | project_tech | capabilities | project_text,
    }


def _score_career(profile: StudentProfile, career: dict) -> PathwayMatch:
    features = _profile_features(profile)
    required = career["required_skills"]
    matched_skills = [skill for skill in required if _contains(features["searchable"], skill)]
    missing_skills = [skill for skill in required if skill not in matched_skills]
    skill_score = len(matched_skills) / max(1, len(required))

    context_targets = career["preferred_contexts"] + career["project_types"]
    matched_contexts = [item for item in context_targets if _contains(features["contexts"], item)]
    evidence_score = min(1.0, len(matched_contexts) / max(1, min(4, len(context_targets))))

    matched_interests = [item for item in career["interest_tags"] if _contains(features["interests"], item)]
    interest_score = len(matched_interests) / max(1, len(career["interest_tags"]))
    matched_education = [item for item in career["education_terms"] if _contains(features["education"], item)]
    education_score = 1.0 if matched_education else 0.0

    score = round(max(0, min(100, skill_score * 40 + evidence_score * 30 + interest_score * 15 + education_score * 15)))

    reasons = []
    if matched_skills:
        reasons.append("Demonstrated relevant skills: " + ", ".join(matched_skills[:4]))
    if matched_contexts:
        reasons.append("Portfolio aligns with: " + ", ".join(matched_contexts[:3]))
    if matched_interests:
        reasons.append("Interests align with: " + ", ".join(matched_interests[:3]))
    if matched_education:
        reasons.append("Education aligns with: " + ", ".join(matched_education[:2]))
    if not reasons:
        reasons.append("Only weak broad-profile similarity was found")

    evidence = []
    for project in profile.projects:
        project_blob = _tokens([project.name, project.summary, *project.technologies, *project.capabilities])
        if any(_contains(project_blob, term) for term in matched_skills + matched_contexts):
            evidence.append(f"Project: {project.name} — {project.summary}")
    for skill in profile.skills:
        if any(normalize(match) == normalize(skill.name) or normalize(match) in _tokens(skill.contexts) for match in matched_skills):
            evidence.append(f"Skill evidence: {skill.name} — {skill.evidence}")
    if not evidence:
        evidence.append("Education and interests provide preliminary alignment; stronger project evidence is needed")

    status = "eligible" if matched_skills or matched_education else "conditionally_eligible"
    eligibility_reasons = [
        "Portfolio contains at least one relevant skill or education signal"
        if status == "eligible"
        else "This remains an exploratory path until stronger skill or project evidence is added"
    ]

    return PathwayMatch(
        pathway_id=career["id"],
        pathway_type="career",
        title=career["title"],
        score=score,
        reasons=reasons,
        evidence=list(dict.fromkeys(evidence))[:4],
        matched_attributes=[*matched_skills, *matched_contexts, *matched_interests, *matched_education],
        eligibility_status=status,
        eligibility_reasons=eligibility_reasons,
        missing_requirements=missing_skills,
        risks_tradeoffs=career["tradeoffs"],
        estimated_duration=career["duration"],
        cost_category=career["cost"],
        next_actions=career["next_actions"],
        related_outcomes=[career["category"], *career.get("common_job_roles", [])],
    )


def score_career(profile: StudentProfile, career_id: str) -> PathwayMatch:
    """Score one curated career against a college-stage student profile."""

    if profile.stage != "college":
        raise ValueError("Career scoring requires a college-stage profile")
    return _score_career(profile, get_career(career_id))


def rank_pathways(profile: StudentProfile) -> PathwayRecommendations:
    if profile.stage == "class10":
        ranked = [_score_stream(profile, pathway) for pathway in STREAM_PATHWAYS]
    elif profile.stage == "class12":
        ranked = [_score_course(profile, course) for course in COURSE_PATHWAYS]
    elif profile.stage == "college":
        ranked = [_score_career(profile, career) for career in CAREERS]
    else:
        raise ValueError(f"Unsupported student stage: {profile.stage}")
    return _select_top_three(ranked)


# Backward-compatible name retained for the original Week 1 demo.
def rank_careers(profile: StudentProfile) -> PathwayRecommendations:
    if profile.stage != "college":
        raise ValueError("rank_careers supports college profiles only")
    return rank_pathways(profile)
