from __future__ import annotations

import argparse
import os
from functools import partial

from . import DATASET_NAME, PROJECT_NAME
from .evaluators import build_openevals_correctness, consulting_quality, decision_correctness
from .target import consulting_target


def run_experiment(variant: str, include_llm_judge: bool = True) -> object:
    """Run one traced configuration over the uploaded LangSmith dataset."""
    missing = [key for key in ("LANGSMITH_API_KEY", "OPENAI_API_KEY") if not os.getenv(key)]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    from langsmith import Client

    client = Client()
    dataset_name = os.getenv("LANGSMITH_DATASET", DATASET_NAME)
    evaluators = [decision_correctness, consulting_quality]
    if include_llm_judge:
        evaluators.append(build_openevals_correctness(os.getenv("OPENAI_MODEL")))

    target = partial(consulting_target, variant=variant)
    results = client.evaluate(
        target,
        data=dataset_name,
        evaluators=evaluators,
        experiment_prefix=f"{variant}-{os.getenv('OPENAI_MODEL', 'gpt-5.4-mini')}",
        description=f"Social-impact consulting assistant; prompt variant={variant}.",
        max_concurrency=2,
        metadata={
            "models": [f"openai:{os.getenv('OPENAI_MODEL', 'gpt-5.4-mini')}"],
            "prompt_variant": variant,
            "dataset_version": "1.0",
            "project": os.getenv("LANGSMITH_PROJECT", PROJECT_NAME),
        },
    )
    print(f"Completed experiment: {getattr(results, 'experiment_name', results)}")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=["concise", "evidence_first"], required=True)
    parser.add_argument("--no-llm-judge", action="store_true")
    args = parser.parse_args()
    run_experiment(args.variant, include_llm_judge=not args.no_llm_judge)


if __name__ == "__main__":
    main()

