from __future__ import annotations

import subprocess
import sys

from app.career_data import CAREERS, get_career
from app.comparison import compare_careers
from app.local_parser import parse_known_demo
from app.matcher import rank_careers


def test_uploaded_csv_is_the_college_career_source() -> None:
    assert len(CAREERS) == 40
    assert get_career("data_scientist")["salary_range"] == "6-18 LPA (fresher-mid)"
    assert "Kaggle" in " ".join(get_career("data_scientist")["learning_resources"])


def test_public_college_demo_is_generic() -> None:
    profile = parse_known_demo("college_demo")
    assert profile.name == "Demo College Student"
    assert profile.stage == "college"


def test_generic_demo_is_ranked_against_csv_careers() -> None:
    result = rank_careers(parse_known_demo("college_demo"))
    dataset_ids = {career["id"] for career in CAREERS}
    assert len(result.matches) == 3
    assert {match.pathway_id for match in result.matches} <= dataset_ids


def test_comparison_exposes_csv_details() -> None:
    result = compare_careers(parse_known_demo("college_demo"), "data_scientist", "ai_ml_engineer")
    assert result.career_1.salary_range
    assert result.career_1.future_scope
    assert result.career_1.minimum_qualification
    assert result.career_1.learning_resources


def test_college_cli_uses_generic_profile() -> None:
    result = subprocess.run(
        [sys.executable, "local_demo.py", "--college", "--full-flow"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Demo College Student" in result.stdout
    assert "Career data source: career_dataset.csv" in result.stdout
    assert "Salary:" in result.stdout


def test_short_or_partial_terms_do_not_create_false_matches() -> None:
    from app.matcher import _contains

    assert _contains({"model evaluation"}, "valuation") is False
    assert _contains({"technology"}, "biotechnology") is False
    assert _contains({"python"}, "Python basics") is True
