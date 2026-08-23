from __future__ import annotations

from collections import Counter

from .common import load_examples

VALID_DECISIONS = {"proceed", "clarify", "escalate"}
REQUIRED_METADATA = {"category", "difficulty", "source", "evidence_terms"}


def validate_examples(examples: list[dict]) -> dict[str, object]:
    """Fail fast on incomplete, duplicated, or weakly diversified examples."""
    errors: list[str] = []
    ids = [row.get("id") for row in examples]
    if not 10 <= len(examples) <= 20:
        errors.append("dataset must contain between 10 and 20 examples")
    if len(ids) != len(set(ids)):
        errors.append("example IDs must be unique")

    for index, row in enumerate(examples, start=1):
        prefix = f"example {index}"
        inputs, outputs, metadata = (
            row.get("inputs", {}), row.get("outputs", {}), row.get("metadata", {})
        )
        if not inputs.get("brief") or not inputs.get("question"):
            errors.append(f"{prefix}: brief and question are required")
        if outputs.get("decision") not in VALID_DECISIONS:
            errors.append(f"{prefix}: invalid decision")
        if not outputs.get("answer") or not outputs.get("next_action"):
            errors.append(f"{prefix}: answer and next_action are required")
        if not REQUIRED_METADATA.issubset(metadata):
            errors.append(f"{prefix}: incomplete metadata")
        if not metadata.get("evidence_terms"):
            errors.append(f"{prefix}: at least one evidence term is required")

    if len({row["metadata"]["category"] for row in examples}) < 5:
        errors.append("dataset must cover at least five categories")
    if len({row["metadata"]["difficulty"] for row in examples}) < 3:
        errors.append("dataset must cover three difficulty levels")
    if errors:
        raise ValueError("Dataset validation failed:\n- " + "\n- ".join(errors))

    return {
        "examples": len(examples),
        "decisions": dict(Counter(row["outputs"]["decision"] for row in examples)),
        "categories": dict(Counter(row["metadata"]["category"] for row in examples)),
        "difficulties": dict(Counter(row["metadata"]["difficulty"] for row in examples)),
    }


def main() -> None:
    summary = validate_examples(load_examples())
    print(f"Dataset valid: {summary}")


if __name__ == "__main__":
    main()

