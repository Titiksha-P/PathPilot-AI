from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import ValidationError

# Load local environment configuration before importing the Google ADK agent.
load_dotenv()

from app.orchestrator import run_decision_simulator, run_guidance
from app.retry import RetryExhaustedError, retry_async
from app.schemas import StudentProfile

APP_NAME = "adaptive_career_guidance_demo"
USER_ID = "demo_user"


async def _run_parser_once(profile_text: str, stage: str) -> StudentProfile:
    try:
        from google.adk.runners import InMemoryRunner
        from google.genai import types

        from app.agent import root_agent
    except ModuleNotFoundError as error:
        raise RuntimeError(
            "Google ADK dependencies are not installed. Run: pip install -r requirements.txt"
        ) from error

    runner = InMemoryRunner(agent=root_agent, app_name=APP_NAME)
    session = await runner.session_service.create_session(app_name=APP_NAME, user_id=USER_ID)
    prompt = (
        f"Student stage: {stage}\n\n"
        "Convert the following profile text into StudentProfile.\n\n"
        f"{profile_text}"
    )
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    final_text = ""

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response() and event.content:
            final_text = "".join(part.text or "" for part in (event.content.parts or []))

    if not final_text.strip():
        raise RuntimeError("The ADK parser returned no structured profile")

    try:
        payload: Any = json.loads(final_text)
        return StudentProfile.model_validate(payload)
    except (json.JSONDecodeError, ValidationError) as error:
        raise RuntimeError("The ADK parser returned invalid StudentProfile JSON") from error


async def parse_profile_with_adk(profile_text: str, stage: str) -> StudentProfile:
    return await retry_async(
        lambda: _run_parser_once(profile_text, stage),
        attempts=3,
        initial_delay=2.0,
    )


async def run(profile_path: Path, stage: str, full_flow: bool = False) -> dict:
    if not profile_path.exists():
        raise FileNotFoundError(f"Profile file not found: {profile_path}")
    profile_text = profile_path.read_text(encoding="utf-8")
    profile = await parse_profile_with_adk(profile_text, stage)
    if full_flow:
        if profile.stage != "college":
            raise RuntimeError("The complete career comparison and roadmap flow currently requires a college-stage profile")
        result = run_decision_simulator(profile)
    else:
        result = run_guidance(profile)
    return result.model_dump(mode="json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run one Gemini/Google ADK parsing call, then deterministic matching and verification"
    )
    parser.add_argument("resume", type=Path, nargs="?", help="Backward-compatible positional profile file")
    parser.add_argument("--profile", type=Path, help="Path to an unstructured student profile or resume text file")
    parser.add_argument("--stage", choices=["class10", "class12", "college"], default="college")
    parser.add_argument("--full-flow", action="store_true", help="After parsing a college profile, include comparison, skill gaps, and a 90-day roadmap")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    profile_path = args.profile or args.resume or Path("data/profile_college_demo.txt")
    try:
        output = asyncio.run(run(profile_path, args.stage, full_flow=args.full_flow))
    except RetryExhaustedError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    except (FileNotFoundError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
