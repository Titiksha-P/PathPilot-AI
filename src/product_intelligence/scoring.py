from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Sequence


DEFAULT_WEIGHTS: Dict[str, float] = {
    "interest_match": 0.25,
    "skill_match": 0.20,
    "education_match": 0.15,
    "goal_match": 0.15,
    "learning_preference_match": 0.10,
    "future_demand": 0.10,
    "constraint_fit": 0.05,
}


@dataclass(frozen=True)
class CareerScore:
    career_id: str
    career_name: str
    total_score: float
    component_scores: Dict[str, float]
    confidence: float


def _normalise_score(value: float) -> float:
    return max(0.0, min(100.0, float(value)))


def validate_weights(weights: Mapping[str, float]) -> None:
    missing = set(DEFAULT_WEIGHTS) - set(weights)
    if missing:
        raise ValueError(f"Missing scoring weights: {sorted(missing)}")

    total = sum(weights.values())
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Weights must total 1.0, received {total:.4f}")


def calculate_career_score(
    career_id: str,
    career_name: str,
    component_scores: Mapping[str, float],
    weights: Mapping[str, float] | None = None,
) -> CareerScore:
    selected_weights = dict(weights or DEFAULT_WEIGHTS)
    validate_weights(selected_weights)

    missing = set(selected_weights) - set(component_scores)
    if missing:
        raise ValueError(f"Missing component scores: {sorted(missing)}")

    normalised = {
        key: _normalise_score(component_scores[key]) for key in selected_weights
    }
    total = sum(normalised[key] * selected_weights[key] for key in selected_weights)

    # Confidence reflects both score strength and agreement between components.
    spread = max(normalised.values()) - min(normalised.values())
    confidence = _normalise_score((0.75 * total) + (0.25 * (100.0 - spread)))

    return CareerScore(
        career_id=career_id,
        career_name=career_name,
        total_score=round(total, 2),
        component_scores={key: round(value, 2) for key, value in normalised.items()},
        confidence=round(confidence, 2),
    )


def rank_careers(careers: Iterable[CareerScore], limit: int = 3) -> List[CareerScore]:
    if limit <= 0:
        raise ValueError("limit must be greater than zero")
    return sorted(careers, key=lambda item: (item.total_score, item.confidence), reverse=True)[:limit]


def build_explanation(score: CareerScore, strongest: int = 3) -> List[str]:
    labels = {
        "interest_match": "Your interests strongly align with this path",
        "skill_match": "Your current skills provide a useful starting point",
        "education_match": "Your education level is compatible with the entry path",
        "goal_match": "This career supports your stated goals",
        "learning_preference_match": "The learning journey fits how you prefer to learn",
        "future_demand": "The field shows promising future demand",
        "constraint_fit": "The path fits your current practical constraints",
    }
    ordered = sorted(
        score.component_scores.items(), key=lambda item: item[1], reverse=True
    )[:strongest]
    return [f"{labels[key]} ({value:.0f}/100)." for key, value in ordered]
