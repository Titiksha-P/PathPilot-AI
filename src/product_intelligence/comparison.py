from __future__ import annotations

from typing import Any, Dict, Mapping


COMPARISON_DIMENSIONS = (
    "personal_fit",
    "current_readiness",
    "learning_effort",
    "education_compatibility",
    "future_opportunity",
    "constraint_fit",
)


def compare_careers(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
) -> Dict[str, Any]:
    for career in (left, right):
        missing = set(COMPARISON_DIMENSIONS) - set(career.get("comparison_scores", {}))
        if missing:
            raise ValueError(f"Missing comparison dimensions: {sorted(missing)}")

    left_scores = left["comparison_scores"]
    right_scores = right["comparison_scores"]

    dimension_results = []
    left_wins = 0
    right_wins = 0

    for dimension in COMPARISON_DIMENSIONS:
        left_value = float(left_scores[dimension])
        right_value = float(right_scores[dimension])
        if left_value > right_value:
            winner = left["career_name"]
            left_wins += 1
        elif right_value > left_value:
            winner = right["career_name"]
            right_wins += 1
        else:
            winner = "tie"

        dimension_results.append(
            {
                "dimension": dimension,
                "left_score": left_value,
                "right_score": right_value,
                "winner": winner,
            }
        )

    if left_wins > right_wins:
        overall = left["career_name"]
    elif right_wins > left_wins:
        overall = right["career_name"]
    else:
        overall = "balanced"

    return {
        "left_career": left["career_name"],
        "right_career": right["career_name"],
        "dimension_results": dimension_results,
        "overall_recommendation": overall,
        "decision_note": (
            "The result supports decision-making; it does not replace the student's final choice."
        ),
    }
