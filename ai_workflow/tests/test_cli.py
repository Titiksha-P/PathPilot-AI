from __future__ import annotations

import subprocess
import sys


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "local_demo.py", *args],
        check=False,
        capture_output=True,
        text=True,
    )


def test_class10_cli_command() -> None:
    result = run_cli("--class10")
    assert result.returncode == 0
    assert "Science (PCM)" in result.stdout
    assert "Approved: True" in result.stdout


def test_class12_cli_command() -> None:
    result = run_cli("--class12")
    assert result.returncode == 0
    assert "Pathway Ranking Engine" in result.stdout
    assert "Approved: True" in result.stdout


def test_college_cli_command() -> None:
    result = run_cli("--college")
    assert result.returncode == 0
    assert "Data Scientist" in result.stdout
    assert "Approved: True" in result.stdout


def test_compare_cli_command() -> None:
    result = run_cli("--compare")
    assert result.returncode == 0
    assert result.stdout.count("Approved: True") >= 5


def test_full_flow_cli_command() -> None:
    result = run_cli("--college", "--full-flow")
    assert result.returncode == 0
    assert "Compare Two Careers" in result.stdout
    assert "90-Day Learning Roadmap" in result.stdout


def test_career_compare_cli_command() -> None:
    result = run_cli(
        "--profile",
        "college_demo",
        "--career-compare",
        "data_scientist",
        "business_analyst",
    )
    assert result.returncode == 0
    assert "Data Scientist" in result.stdout
    assert "Business Analyst" in result.stdout
    assert "Better fit" in result.stdout


def test_roadmap_cli_command() -> None:
    result = run_cli("--profile", "college_demo", "--roadmap", "ai_ml_engineer")
    assert result.returncode == 0
    assert "Days 1-30" in result.stdout
    assert "Days 31-60" in result.stdout
    assert "Days 61-90" in result.stdout
