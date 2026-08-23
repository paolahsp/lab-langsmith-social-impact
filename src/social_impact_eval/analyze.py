from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Any


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate scores overall and by variant, category, and difficulty."""
    if not rows:
        raise ValueError("Cannot analyze an empty result set")
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        for dimension in ("variant", "category", "difficulty"):
            grouped[(dimension, str(row[dimension]))].append(row)

    def metrics(items: list[dict[str, Any]]) -> dict[str, float | int]:
        return {
            "n": len(items),
            "decision_accuracy": round(mean(float(item["decision_correctness"]) for item in items), 3),
            "mean_consulting_quality": round(mean(float(item["consulting_quality"]) for item in items), 3),
            "pass_rate": round(
                mean(
                    float(
                        item["decision_correctness"] == 1
                        and float(item["consulting_quality"]) >= 0.75
                    )
                    for item in items
                ),
                3,
            ),
        }

    return {
        "overall": metrics(rows),
        "segments": {
            f"{dimension}:{value}": metrics(items)
            for (dimension, value), items in sorted(grouped.items())
        },
        "failures": [
            {
                "id": row["id"],
                "variant": row["variant"],
                "expected": row["expected_decision"],
                "actual": row["output"]["decision"],
                "category": row["category"],
                "difficulty": row["difficulty"],
            }
            for row in rows
            if row["decision_correctness"] == 0
        ],
    }

