"""Product intelligence primitives for PathPilot AI.

This package defines the deterministic decision rules and shared contracts that
connect the product, frontend, backend, career dataset, and AI workflow.
"""

from .comparison import compare_careers
from .contracts import (
    create_frontend_response,
    validate_recommendation_payload,
    validate_student_profile,
)
from .roadmap import build_90_day_roadmap
from .scoring import (
    CareerScore,
    build_explanation,
    calculate_career_score,
    rank_careers,
)

__all__ = [
    "CareerScore",
    "build_90_day_roadmap",
    "build_explanation",
    "calculate_career_score",
    "compare_careers",
    "create_frontend_response",
    "rank_careers",
    "validate_recommendation_payload",
    "validate_student_profile",
]
