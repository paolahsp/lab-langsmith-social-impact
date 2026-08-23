from __future__ import annotations

import re
from typing import Any

from .analyze import summarize
from .common import RESULTS_DIR, load_examples, write_json
from .evaluators import consulting_quality, decision_correctness
from .validate import validate_examples


def _decision(brief: str, variant: str) -> str:
    text = brief.lower()
    obvious_escalation = (
        "safeguarding policy",
        "no separate consent",
        "suspected duplicate",
        "mandatory child-protection",
    )
    obvious_clarification = ("no baseline", "not yet been reconciled", "not disaggregated")
    if variant == "risk_aware":
        obvious_escalation += ("data-processing agreement is not signed",)
        obvious_clarification += ("has no indicators", "only four households")
    if any(term in text for term in obvious_escalation):
        return "escalate"
    if any(term in text for term in obvious_clarification):
        return "clarify"
    return "proceed"


def offline_target(inputs: dict[str, str], variant: str) -> dict[str, str]:
    """Transparent rule baseline for reproducible evaluation without API credentials."""
    decision = _decision(inputs["brief"], variant)
    first_sentence = re.split(r"(?<=[.!?])\s+", inputs["brief"].strip())[0]
    actions = {
        "proceed": "Document the cited evidence and approve the next controlled step.",
        "clarify": "Verify the missing evidence and document the result before making the claim.",
        "escalate": "Pause the activity, preserve the evidence, and escalate to the responsible lead.",
    }
    return {
        "decision": decision,
        "answer": first_sentence,
        "next_action": actions[decision],
    }


def run() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    examples = load_examples()
    validate_examples(examples)
    rows: list[dict[str, Any]] = []
    for variant in ("keyword_baseline", "risk_aware"):
        for example in examples:
            output = offline_target(example["inputs"], variant)
            decision_eval = decision_correctness(example["inputs"], output, example["outputs"])
            quality_eval = consulting_quality(example["inputs"], output, example["outputs"])
            rows.append(
                {
                    "id": example["id"],
                    "variant": variant,
                    "category": example["metadata"]["category"],
                    "difficulty": example["metadata"]["difficulty"],
                    "expected_decision": example["outputs"]["decision"],
                    "output": output,
                    "decision_correctness": int(bool(decision_eval["score"])),
                    "consulting_quality": quality_eval["score"],
                    "quality_comment": quality_eval["comment"],
                }
            )
    metrics = summarize(rows)
    write_json(RESULTS_DIR / "offline_results.json", rows)
    write_json(RESULTS_DIR / "metrics.json", metrics)
    return rows, metrics


def main() -> None:
    rows, metrics = run()
    print(f"Evaluated {len(rows)} outputs; metrics written to {RESULTS_DIR}")
    for key, value in metrics["segments"].items():
        if key.startswith("variant:"):
            print(key, value)


if __name__ == "__main__":
    main()

