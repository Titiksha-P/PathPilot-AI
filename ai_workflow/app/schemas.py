from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

StudentStage = Literal["class10", "class12", "college"]
EligibilityStatus = Literal["eligible", "conditionally_eligible", "not_eligible"]
PathwayType = Literal["stream", "course", "career"]
RankRole = Literal["best_fit", "strong_alternative", "safe_backup"]


class EducationItem(BaseModel):
    qualification: str
    field: str
    institution: str = ""
    status: str = ""
    evidence: str


class SkillEvidence(BaseModel):
    name: str
    level: str = "unknown"
    evidence: str
    contexts: list[str] = Field(default_factory=list)


class ProjectEvidence(BaseModel):
    name: str
    summary: str
    technologies: list[str] = Field(default_factory=list)
    capabilities: list[str] = Field(default_factory=list)
    status: str = ""


class StudentPreferences(BaseModel):
    location: str = ""
    budget: Literal["low", "medium", "high"] = "medium"
    language: str = "English"
    preferred_course_type: str = ""
    work_styles: list[str] = Field(default_factory=list)


class StudentProfile(BaseModel):
    """One normalized profile used by all three adaptive guidance flows."""

    name: str = "Unknown"
    stage: StudentStage
    current_class_or_program: str = ""
    stream: str = ""
    marks: dict[str, float] = Field(default_factory=dict)
    aptitude: dict[str, float] = Field(default_factory=dict)
    entrance_readiness: dict[str, float] = Field(default_factory=dict)
    education: list[EducationItem] = Field(default_factory=list)
    skills: list[SkillEvidence] = Field(default_factory=list)
    projects: list[ProjectEvidence] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    career_goal: str = ""
    preferences: StudentPreferences = Field(default_factory=StudentPreferences)

    @field_validator("marks", "aptitude", "entrance_readiness")
    @classmethod
    def percentages_must_be_valid(cls, value: dict[str, float]) -> dict[str, float]:
        invalid = {key: score for key, score in value.items() if not 0 <= score <= 100}
        if invalid:
            raise ValueError(f"Scores must be between 0 and 100: {invalid}")
        return value


class PathwayMatch(BaseModel):
    pathway_id: str
    pathway_type: PathwayType
    title: str
    rank_role: RankRole = "best_fit"
    score: int = Field(ge=0, le=100)
    reasons: list[str] = Field(min_length=1)
    evidence: list[str] = Field(min_length=1)
    matched_attributes: list[str] = Field(default_factory=list)
    eligibility_status: EligibilityStatus
    eligibility_reasons: list[str] = Field(min_length=1)
    missing_requirements: list[str] = Field(default_factory=list)
    risks_tradeoffs: list[str] = Field(default_factory=list)
    estimated_duration: str
    cost_category: str
    next_actions: list[str] = Field(min_length=1)
    related_outcomes: list[str] = Field(default_factory=list)


class PathwayRecommendations(BaseModel):
    matches: list[PathwayMatch] = Field(min_length=3, max_length=3)

    @field_validator("matches")
    @classmethod
    def matches_must_be_ranked(cls, value: list[PathwayMatch]) -> list[PathwayMatch]:
        scores = [item.score for item in value]
        if scores != sorted(scores, reverse=True):
            raise ValueError("Pathway matches must be ordered by descending score")
        return value


class VerificationResult(BaseModel):
    approved: bool
    issues: list[str] = Field(default_factory=list)
    final_recommendations: PathwayRecommendations


class GuidanceResult(BaseModel):
    profile: StudentProfile
    recommendations: PathwayRecommendations
    verification: VerificationResult


class CareerComparisonOption(BaseModel):
    career_id: str
    title: str
    match_score: int = Field(ge=0, le=100)
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    supporting_evidence: list[str] = Field(min_length=1)
    estimated_learning_time: str
    cost_category: str
    salary_range: str | None = None
    future_scope: str | None = None
    minimum_qualification: str = ""
    certifications: list[str] = Field(default_factory=list)
    relevant_courses: list[str] = Field(default_factory=list)
    entrance_exams: list[str] = Field(default_factory=list)
    common_job_roles: list[str] = Field(default_factory=list)
    learning_resources: list[str] = Field(default_factory=list)
    data_source: str = ""
    risks_tradeoffs: list[str] = Field(default_factory=list)


class CareerComparison(BaseModel):
    career_1: CareerComparisonOption
    career_2: CareerComparisonOption
    better_fit_career_id: str
    recommendation_reason: str
    decision_factors: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def careers_must_be_distinct_and_winner_valid(self) -> "CareerComparison":
        ids = {self.career_1.career_id, self.career_2.career_id}
        if len(ids) != 2:
            raise ValueError("Career comparison requires two different careers")
        if self.better_fit_career_id not in ids:
            raise ValueError("Better-fit career must be one of the compared careers")
        return self


class SkillGap(BaseModel):
    skill: str
    priority: Literal["high", "medium", "low"]
    current_evidence: list[str] = Field(default_factory=list)
    why_needed: str
    recommended_action: str


class SkillGapAnalysis(BaseModel):
    career_id: str
    career_title: str
    readiness_score: int = Field(ge=0, le=100)
    matched_skills: list[str] = Field(default_factory=list)
    gaps: list[SkillGap] = Field(default_factory=list)
    strengths_to_use: list[str] = Field(default_factory=list)


class RoadmapTask(BaseModel):
    title: str
    objective: str
    actions: list[str] = Field(min_length=1)
    deliverable: str
    related_skills: list[str] = Field(default_factory=list)


class RoadmapPhase(BaseModel):
    phase_id: Literal["foundations", "applied_project", "portfolio_readiness"]
    day_range: str
    focus: str
    tasks: list[RoadmapTask] = Field(min_length=1)
    success_check: str


class LearningRoadmap90Day(BaseModel):
    career_id: str
    career_title: str
    starting_readiness_score: int = Field(ge=0, le=100)
    target_outcome: str
    phases: list[RoadmapPhase] = Field(min_length=3, max_length=3)

    @field_validator("phases")
    @classmethod
    def phases_must_cover_all_three_stages(cls, value: list[RoadmapPhase]) -> list[RoadmapPhase]:
        expected = ["foundations", "applied_project", "portfolio_readiness"]
        actual = [phase.phase_id for phase in value]
        if actual != expected:
            raise ValueError(f"Roadmap phases must be ordered as {expected}")
        return value


class CareerDecisionSimulation(BaseModel):
    profile: StudentProfile
    recommendations: PathwayRecommendations
    comparison: CareerComparison
    skill_gap_analysis: SkillGapAnalysis
    roadmap_90_days: LearningRoadmap90Day
    verification: VerificationResult
