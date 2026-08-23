from __future__ import annotations

import os

from . import DATASET_NAME
from .common import load_examples
from .validate import validate_examples


def upload_dataset() -> object:
    """Create the LangSmith dataset once and avoid duplicate example uploads."""
    if not os.getenv("LANGSMITH_API_KEY"):
        raise RuntimeError("LANGSMITH_API_KEY is required")
    from langsmith import Client

    examples = load_examples()
    validate_examples(examples)
    client = Client()
    dataset_name = os.getenv("LANGSMITH_DATASET", DATASET_NAME)

    if client.has_dataset(dataset_name=dataset_name):
        dataset = client.read_dataset(dataset_name=dataset_name)
        existing = list(client.list_examples(dataset_id=dataset.id))
        if len(existing) != len(examples):
            raise RuntimeError(
                f"Existing dataset has {len(existing)} examples; expected {len(examples)}. "
                "Use a new versioned dataset name rather than appending duplicates."
            )
        print(f"Dataset already exists and is valid: {dataset_name} ({dataset.id})")
        return dataset

    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description=(
            "Fifteen synthetic, evidence-grounded consulting decisions for social-impact "
            "programs; evaluates routing, grounded explanations, and operational actions."
        ),
    )
    client.create_examples(
        dataset_id=dataset.id,
        examples=[
            {
                "inputs": row["inputs"],
                "outputs": row["outputs"],
                "metadata": {**row["metadata"], "case_id": row["id"]},
            }
            for row in examples
        ],
    )
    print(f"Created dataset: {dataset_name} ({dataset.id})")
    return dataset


def main() -> None:
    upload_dataset()


if __name__ == "__main__":
    main()

