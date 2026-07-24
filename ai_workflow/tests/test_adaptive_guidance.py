from __future__ import annotations

import asyncio
import os

from app.datasets import all_pathway_ids
from app.local_parser import parse_known_demo
from app.matcher import evaluate_course_eligibility, rank_pathways
from app.orchestrator import run_guidance
from app.retry import RetryExhaustedError, retry_async
from app.schemas import PathwayMatch, PathwayRecommendations
from app.verifier import verify_guidance


def test_class10_gets_three_explainable_stream_paths() -> None:
    profile = parse_known_demo("class10")
    result = run_guidance(profile)

    assert result.verification.approved is True
    assert len(result.recommendations.matches) == 3
    assert result.recommendations.matches[0].pathway_type == "stream"
    assert result.recommendations.matches[0].title == "Science (PCM)"
    for match in result.recommendations.matches:
        assert match.evidence
        assert match.next_actions
        assert match.eligibility_status in {"eligible", "conditionally_eligible", "not_eligible"}


def test_class12_gets_degree_paths_with_eligibility() -> None:
    profile = parse_known_demo("class12")
    result = run_guidance(profile)

    assert result.verification.approved is True
    assert len(result.recommendations.matches) == 3
    assert result.recommendations.matches[0].pathway_type == "course"
    assert result.recommendations.matches[0].title in {"MBBS", "B.Sc. Biotechnology", "B.Sc. Nursing"}
    assert all(match.eligibility_reasons for match in result.recommendations.matches)


def test_college_resume_uses_portfolio_evidence_not_only_skill_tags() -> None:
    profile = parse_known_demo("college_demo")
    result = run_guidance(profile)
    titles = [match.title for match in result.recommendations.matches]

    assert result.verification.approved is True
    assert "Data Scientist" in titles
    assert "Business Analyst" in titles
    assert any("Campus Placement" in evidence for match in result.recommendations.matches for evidence in match.evidence)


def test_different_profiles_produce_different_top_pathways() -> None:
    names = ["class10", "class12", "college_demo", "dashboard", "ux"]
    top_titles = [run_guidance(parse_known_demo(name)).recommendations.matches[0].title for name in names]

    assert len(set(top_titles)) == len(top_titles)


def test_ranked_results_are_descending_and_have_required_fields() -> None:
    for profile_name in ["class10", "class12", "college_demo", "dashboard", "ux"]:
        recommendations = rank_pathways(parse_known_demo(profile_name))
        scores = [match.score for match in recommendations.matches]
        assert scores == sorted(scores, reverse=True)
        assert [match.rank_role for match in recommendations.matches] == [
            "best_fit",
            "strong_alternative",
            "safe_backup",
        ]
        for match in recommendations.matches:
            assert 0 <= match.score <= 100
            assert match.pathway_id in all_pathway_ids()
            assert match.reasons
            assert match.evidence
            assert match.estimated_duration
            assert match.cost_category
            assert match.next_actions


def test_ineligible_course_reports_missing_requirements() -> None:
    profile = parse_known_demo("class12_arts")
    status, reasons, missing = evaluate_course_eligibility(profile, "btech_cse_ai")

    assert status == "not_eligible"
    assert reasons
    assert any("PCM" in item or "Mathematics" in item for item in missing)


def test_verifier_rejects_unknown_pathway_and_missing_evidence() -> None:
    profile = parse_known_demo("college_demo")
    valid = rank_pathways(profile)
    bad_first = valid.matches[0].model_copy(
        update={"pathway_id": "invented_pathway", "evidence": []}
    )
    bad = PathwayRecommendations(matches=[bad_first, *valid.matches[1:]])

    result = verify_guidance(profile, bad)

    assert result.approved is False
    assert any("unknown pathway" in issue.lower() for issue in result.issues)
    assert any("no supporting evidence" in issue.lower() for issue in result.issues)


def test_retry_async_retries_429_then_succeeds() -> None:
    attempts = 0

    async def operation() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise RuntimeError("429 RESOURCE_EXHAUSTED")
        return "ok"

    async def no_sleep(_: float) -> None:
        return None

    result = asyncio.run(retry_async(operation, attempts=3, sleep=no_sleep))

    assert result == "ok"
    assert attempts == 3


def test_retry_async_returns_clean_error_after_final_429() -> None:
    async def operation() -> str:
        raise RuntimeError("429 RESOURCE_EXHAUSTED")

    async def no_sleep(_: float) -> None:
        return None

    try:
        asyncio.run(retry_async(operation, attempts=3, sleep=no_sleep))
    except RetryExhaustedError as exc:
        assert exc.status_code == 429
        assert "temporarily unavailable" in str(exc).lower()
        assert "traceback" not in str(exc).lower()
    else:
        raise AssertionError("RetryExhaustedError was not raised")


def test_offline_guidance_does_not_require_api_key(monkeypatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_CLOUD_PROJECT", raising=False)

    result = run_guidance(parse_known_demo("class10"))

    assert result.verification.approved is True
    assert "GEMINI_API_KEY" not in os.environ
