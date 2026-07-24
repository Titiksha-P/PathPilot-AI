from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from app.career_data import get_career
from app.comparison import compare_careers
from app.integration import (
    analyze_student,
    compare_two_careers,
    generate_roadmap,
    get_skill_gap_analysis,
    run_complete_flow,
)
from app.local_parser import parse_known_demo
from app.orchestrator import run_decision_simulator
from app.roadmap import generate_90_day_roadmap
from app.schemas import CareerComparison, LearningRoadmap90Day
from app.skill_gaps import analyze_skill_gaps


def test_get_career_rejects_unknown_id() -> None:
    with pytest.raises(ValueError, match="Unknown career"):
        get_career("invented-career")


def test_comparison_schema_rejects_same_career() -> None:
    option = {
        "career_id": "data_scientist",
        "title": "Data Scientist",
        "match_score": 75,
        "matched_skills": ["python"],
        "missing_skills": ["sql"],
        "supporting_evidence": ["Python project"],
        "estimated_learning_time": "Not specified in dataset",
        "cost_category": "Not specified in dataset",
        "salary_range": "6-18 LPA",
        "future_scope": "Dataset-provided trend note",
        "risks_tradeoffs": ["Qualification requirement applies"],
    }
    with pytest.raises(ValidationError):
        CareerComparison(
            career_1=option,
            career_2=option,
            better_fit_career_id="data_scientist",
            recommendation_reason="Same career should be rejected",
            decision_factors=["score"],
        )


def test_roadmap_schema_requires_exactly_three_phases() -> None:
    with pytest.raises(ValidationError):
        LearningRoadmap90Day(
            career_id="data_scientist",
            career_title="Data Scientist",
            starting_readiness_score=60,
            target_outcome="Portfolio-ready beginner",
            phases=[],
        )


def test_compare_careers_prefers_stronger_profile_match() -> None:
    profile = parse_known_demo("college_demo")
    result = compare_careers(profile, "data_scientist", "business_analyst")

    assert result.career_1.career_id == "data_scientist"
    assert result.career_2.career_id == "business_analyst"
    assert result.career_1.match_score > result.career_2.match_score
    assert result.better_fit_career_id == "data_scientist"
    assert result.recommendation_reason
    assert result.decision_factors
    assert result.career_1.salary_range == "6-18 LPA (fresher-mid)"
    assert result.career_1.future_scope
    assert result.career_1.learning_resources


def test_compare_careers_rejects_duplicate_ids() -> None:
    with pytest.raises(ValueError, match="different careers"):
        compare_careers(parse_known_demo("college_demo"), "data_scientist", "data_scientist")


def test_skill_gap_analysis_identifies_missing_engineering_skills() -> None:
    result = analyze_skill_gaps(parse_known_demo("college_demo"), "ai_ml_engineer")

    assert result.career_id == "ai_ml_engineer"
    assert result.readiness_score >= 0
    assert result.gaps
    missing_names = {gap.skill for gap in result.gaps}
    assert {"TensorFlow/PyTorch", "Deep Learning", "NLP", "MLOps"} & missing_names
    assert all(gap.recommended_action for gap in result.gaps)


def test_roadmap_has_three_personalized_phases_and_deliverables() -> None:
    result = generate_90_day_roadmap(parse_known_demo("college_demo"), "ai_ml_engineer")

    assert [phase.day_range for phase in result.phases] == ["Days 1–30", "Days 31–60", "Days 61–90"]
    assert [phase.phase_id for phase in result.phases] == ["foundations", "applied_project", "portfolio_readiness"]
    assert all(phase.tasks for phase in result.phases)
    assert all(task.deliverable for phase in result.phases for task in phase.tasks)
    roadmap_text = json.dumps(result.model_dump()).lower()
    assert "deep learning" in roadmap_text
    assert "salary" not in roadmap_text


def test_complete_simulator_uses_top_two_and_best_fit_roadmap_by_default() -> None:
    result = run_decision_simulator(parse_known_demo("college_demo"))
    top_two = result.recommendations.matches[:2]

    assert result.comparison.career_1.career_id == top_two[0].pathway_id
    assert result.comparison.career_2.career_id == top_two[1].pathway_id
    assert result.skill_gap_analysis.career_id == top_two[0].pathway_id
    assert result.roadmap_90_days.career_id == top_two[0].pathway_id
    assert result.verification.approved is True


def test_backend_adapters_accept_dict_and_return_json_serializable_data() -> None:
    profile_dict = parse_known_demo("college_demo").model_dump()

    recommendations = analyze_student(profile_dict)
    comparison = compare_two_careers(profile_dict, "data_scientist", "business_analyst")
    gaps = get_skill_gap_analysis(profile_dict, "ai_ml_engineer")
    roadmap = generate_roadmap(profile_dict, "ai_ml_engineer")
    complete = run_complete_flow(profile_dict)

    assert recommendations["verification"]["approved"] is True
    assert comparison["better_fit_career_id"] == "data_scientist"
    assert comparison["career_1"]["data_source"] == "career_dataset.csv"
    assert gaps["gaps"]
    assert len(roadmap["phases"]) == 3
    assert complete["comparison"]
    json.dumps(complete)
