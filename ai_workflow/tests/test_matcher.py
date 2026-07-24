from app.career_data import CAREERS
from app.datasets import COURSE_PATHWAYS, STREAM_PATHWAYS
from app.local_parser import parse_known_demo
from app.matcher import rank_careers, rank_pathways


def test_datasets_are_diverse() -> None:
    assert len(CAREERS) == 40
    assert len({career["category"] for career in CAREERS}) >= 15
    assert len(STREAM_PATHWAYS) >= 5
    assert len(COURSE_PATHWAYS) >= 8


def test_generic_college_profile_gets_data_and_business_roles() -> None:
    result = rank_careers(parse_known_demo("college_demo"))
    titles = [match.title for match in result.matches]
    assert "Data Scientist" in titles
    assert "Business Analyst" in titles


def test_different_college_portfolios_get_different_top_results() -> None:
    demo_top = rank_pathways(parse_known_demo("college_demo")).matches[0].title
    dashboard_top = rank_pathways(parse_known_demo("dashboard")).matches[0].title
    ux_top = rank_pathways(parse_known_demo("ux")).matches[0].title
    assert len({demo_top, dashboard_top, ux_top}) == 3


def test_every_match_has_evidence_and_missing_requirements_field() -> None:
    result = rank_pathways(parse_known_demo("college_demo"))
    assert len(result.matches) == 3
    for match in result.matches:
        assert match.evidence
        assert isinstance(match.missing_requirements, list)
        assert 0 <= match.score <= 100
