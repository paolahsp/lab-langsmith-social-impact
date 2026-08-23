from __future__ import annotations

import re
from typing import Any, Callable


def decision_correctness(
    inputs: dict[str, Any], outputs: dict[str, Any], reference_outputs: dict[str, Any]
) -> dict[str, Any]:
    """Exact-match the decision label, the central routing signal."""
    del inputs
    score = outputs.get("decision") == reference_outputs.get("decision")
    return {"key": "decision_correctness", "score": score}


def consulting_quality(
    inputs: dict[str, Any], outputs: dict[str, Any], reference_outputs: dict[str, Any]
) -> dict[str, Any]:
    """Custom 0–1 score for grounding, actionability, format, and calibrated decision."""
    del reference_outputs
    text = " ".join(str(outputs.get(key, "")) for key in ("answer", "next_action")).lower()
    brief_tokens = {
        token
        for token in re.findall(r"[a-z0-9€%]+", inputs.get("brief", "").lower())
        if len(token) >= 4 or any(char.isdigit() for char in token)
    }
    output_tokens = set(re.findall(r"[a-z0-9€%]+", text))
    grounded = min(1.0, len(brief_tokens & output_tokens) / 3)
    actionable_verbs = {"verify", "confirm", "pause", "document", "collect", "approve", "review", "escalate"}
    actionable = float(bool(actionable_verbs & output_tokens))
    valid_format = float(
        outputs.get("decision") in {"proceed", "clarify", "escalate"}
        and bool(outputs.get("answer"))
        and bool(outputs.get("next_action"))
    )
    score = round((0.45 * grounded) + (0.30 * actionable) + (0.25 * valid_format), 3)
    return {
        "key": "consulting_quality",
        "score": score,
        "comment": f"grounding={grounded:.2f}; actionability={actionable:.2f}; format={valid_format:.2f}",
    }


CORRECTNESS_PROMPT = """Evaluate whether the assistant output is correct and complete for the consulting task.
Use the reference output as the standard but allow equivalent wording. Penalize invented facts and unsafe
recommendations. Inputs: {inputs}\nAssistant output: {outputs}\nReference output: {reference_outputs}"""


def build_openevals_correctness(model: str | None = None) -> Callable:
    """Create the optional reference-aware OpenEvals LLM-as-judge evaluator."""
    from openevals.llm import create_llm_as_judge

    return create_llm_as_judge(
        prompt=CORRECTNESS_PROMPT,
        model=model or "openai:gpt-5.4-mini",
        feedback_key="semantic_correctness",
    )

