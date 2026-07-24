from __future__ import annotations

import argparse
import json

from app.comparison import compare_careers
from app.local_parser import parse_known_demo
from app.orchestrator import run_decision_simulator, run_guidance
from app.roadmap import generate_90_day_roadmap


def _ascii(value: str) -> str:
    return value.replace("–", "-").replace("—", "-")




def _print_career_details(label: str, option) -> None:
    print(f"      Qualification: {_ascii(option.minimum_qualification or 'Not specified')} ({label})")
    print(f"      Salary: {_ascii(option.salary_range or 'Not specified')} ({label})")
    if option.common_job_roles:
        print(f"      {label} roles: {_ascii(', '.join(option.common_job_roles[:3]))}")
    if option.learning_resources:
        print(f"      {label} resources: {_ascii(', '.join(option.learning_resources[:3]))}")
    print(f"      Career data source: {option.data_source or 'not specified'}")

def run(profile_name: str) -> dict:
    profile = parse_known_demo(profile_name)
    print(f"\n[1/4] Adaptive Profile Intake -> {profile.name} ({profile.stage})")
    if profile.stage == "college":
        print(f"      Found {len(profile.skills)} skills and {len(profile.projects)} projects")
    else:
        print(f"      Found {len(profile.marks)} academic scores and {len(profile.aptitude)} aptitude scores")

    print("[2/4] Pathway Ranking Engine -> deterministic evidence-based scoring")
    result = run_guidance(profile)
    for index, match in enumerate(result.recommendations.matches, 1):
        role = match.rank_role.replace("_", " ").title()
        print(f"      {index}. {match.title}: {match.score}% ({role})")
        print(f"         Eligibility: {match.eligibility_status.replace('_', ' ')}")

    print("[3/4] Eligibility Rules -> academic and pathway constraints applied")
    for match in result.recommendations.matches:
        if match.missing_requirements:
            print(f"      {match.title}: {len(match.missing_requirements)} missing/next requirement(s)")
        else:
            print(f"      {match.title}: no current hard requirement gap")

    print("[4/4] Verification -> evidence, ranking, IDs and completeness checks")
    print(f"      Approved: {result.verification.approved}")
    if result.verification.issues:
        for issue in result.verification.issues:
            print(f"      - {issue}")

    return result.model_dump(mode="json")


def print_comparison(profile_name: str, career_id_1: str, career_id_2: str) -> dict:
    profile = parse_known_demo(profile_name)
    result = compare_careers(profile, career_id_1, career_id_2)
    print("\n[5/6] Compare Two Careers")
    print(f"      {result.career_1.title}: {result.career_1.match_score}%")
    print(f"      {result.career_2.title}: {result.career_2.match_score}%")
    _print_career_details(result.career_1.title, result.career_1)
    _print_career_details(result.career_2.title, result.career_2)
    winner = result.career_1 if result.better_fit_career_id == result.career_1.career_id else result.career_2
    print(f"      Better fit: {winner.title}")
    print(f"      Reason: {_ascii(result.recommendation_reason)}")
    return result.model_dump(mode="json")


def print_roadmap(profile_name: str, career_id: str) -> dict:
    profile = parse_known_demo(profile_name)
    result = generate_90_day_roadmap(profile, career_id)
    print("\n[6/6] 90-Day Learning Roadmap")
    print(f"      Target career: {result.career_title}")
    print(f"      Starting readiness: {result.starting_readiness_score}%")
    for phase in result.phases:
        print(f"      {_ascii(phase.day_range)}: {_ascii(phase.focus)}")
        for task in phase.tasks:
            print(f"         - {_ascii(task.title)}")
    return result.model_dump(mode="json")


def print_full_flow(profile_name: str) -> dict:
    profile = parse_known_demo(profile_name)
    result = run_decision_simulator(profile)
    print("\n[5/6] Compare Two Careers")
    print(f"      {result.comparison.career_1.title}: {result.comparison.career_1.match_score}%")
    print(f"      {result.comparison.career_2.title}: {result.comparison.career_2.match_score}%")
    _print_career_details(result.comparison.career_1.title, result.comparison.career_1)
    _print_career_details(result.comparison.career_2.title, result.comparison.career_2)
    winner = (
        result.comparison.career_1
        if result.comparison.better_fit_career_id == result.comparison.career_1.career_id
        else result.comparison.career_2
    )
    print(f"      Better fit: {winner.title}")

    print("\n[6/6] 90-Day Learning Roadmap")
    print(f"      Target career: {result.roadmap_90_days.career_title}")
    for phase in result.roadmap_90_days.phases:
        print(f"      {_ascii(phase.day_range)}: {_ascii(phase.focus)}")
    return result.model_dump(mode="json")


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline adaptive career and education guidance demo")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--class10", action="store_true", help="Run the Class 10 stream guidance persona")
    selection.add_argument("--class12", action="store_true", help="Run the Class 12 course guidance persona")
    selection.add_argument("--college", action="store_true", help="Run the generic college-student demo persona")
    selection.add_argument("--profile", choices=["class10", "class12", "class12_arts", "college_demo", "dashboard", "ux"])
    selection.add_argument("--compare", action="store_true", help="Run all main personas and compare outputs")
    parser.add_argument("--full-flow", action="store_true", help="Run career recommendations, comparison, skill gaps, and roadmap")
    parser.add_argument(
        "--career-compare",
        nargs=2,
        metavar=("CAREER_1", "CAREER_2"),
        help="Compare two curated career IDs for the selected college profile",
    )
    parser.add_argument("--roadmap", metavar="CAREER_ID", help="Generate a 90-day roadmap for one career ID")
    parser.add_argument("--json", action="store_true", help="Print complete JSON output")
    args = parser.parse_args()

    if args.compare:
        profile_names = ["class10", "class12", "college_demo", "dashboard", "ux"]
    elif args.class10:
        profile_names = ["class10"]
    elif args.class12:
        profile_names = ["class12"]
    elif args.college:
        profile_names = ["college_demo"]
    else:
        profile_names = [args.profile or "college_demo"]

    if (args.full_flow or args.career_compare or args.roadmap) and len(profile_names) != 1:
        parser.error("Career comparison and roadmap options require one selected profile")

    outputs = {name: run(name) for name in profile_names}
    selected_name = profile_names[0]

    if args.full_flow:
        outputs[selected_name]["decision_simulation"] = print_full_flow(selected_name)
    else:
        if args.career_compare:
            outputs[selected_name]["career_comparison"] = print_comparison(
                selected_name,
                args.career_compare[0],
                args.career_compare[1],
            )
        if args.roadmap:
            outputs[selected_name]["roadmap_90_days"] = print_roadmap(selected_name, args.roadmap)

    if args.json:
        print("\n" + json.dumps(outputs, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
