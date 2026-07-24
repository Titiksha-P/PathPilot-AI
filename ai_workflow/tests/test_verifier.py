from app.local_parser import parse_known_demo
from app.matcher import rank_pathways
from app.verifier import verify_guidance


def test_valid_recommendations_are_approved() -> None:
    profile = parse_known_demo("college_demo")
    result = verify_guidance(profile, rank_pathways(profile))
    assert result.approved is True
    assert result.issues == []


def test_high_score_without_matched_attributes_is_rejected() -> None:
    profile = parse_known_demo("college_demo")
    recommendations = rank_pathways(profile)
    bad_first = recommendations.matches[0].model_copy(update={"matched_attributes": []})
    bad = recommendations.model_copy(update={"matches": [bad_first, *recommendations.matches[1:]]})
    result = verify_guidance(profile, bad)
    assert result.approved is False
    assert any("high score without matched attributes" in issue for issue in result.issues)
