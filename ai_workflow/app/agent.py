from __future__ import annotations

import os

from google.adk import Agent
from google.adk.models.google_llm import Gemini
from google.genai import types

from .schemas import StudentProfile

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

profile_parser_agent = Agent(
    name="adaptive_profile_parser",
    model=Gemini(
        model=MODEL_NAME,
        # App-level retry handling in run_adk.py owns the maximum three attempts.
        retry_options=types.HttpRetryOptions(attempts=1),
    ),
    description="Parses school or college profile text into one evidence-backed StudentProfile.",
    instruction="""
You are the Profile Parser Agent for SIH25094, a one-stop personalized career
and education advisor.

The user message begins with an explicit stage: class10, class12, or college.
Return the exact StudentProfile schema for that stage.

Rules:
- Preserve marks, aptitude scores, entrance readiness, education, skills,
  projects, interests, goals, and preferences only when the text supports them.
- For college profiles, every skill must include evidence and practical contexts.
- Do not invent marks, qualifications, projects, entrance scores, or skills.
- Ignore phone numbers, email addresses, and other contact information.
- Use empty fields when information is unavailable.
- Return structured data only; do not add advice or career recommendations.
""",
    output_schema=StudentProfile,
    mode="single_turn",
)

# ADK discovers this symbol for local playgrounds and runners.
root_agent = profile_parser_agent
