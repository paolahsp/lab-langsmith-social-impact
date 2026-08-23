from __future__ import annotations

import json
import os
import re
from typing import Any

BASE_INSTRUCTION = """You are a cautious social-impact consulting analyst.
Use only the supplied brief. Return valid JSON with exactly these string fields:
decision (proceed, clarify, or escalate), answer, and next_action.
Do not invent facts. If a material fact is absent, say so and choose clarify; choose escalate
when the brief signals safeguarding, legal, privacy, or financial-control risk."""

VARIANT_INSTRUCTIONS = {
    "concise": BASE_INSTRUCTION + " Keep the answer under 45 words.",
    "evidence_first": BASE_INSTRUCTION
    + " Cite at least one exact figure, timeframe, group, or control from the brief and make the next action operationally specific.",
}


def _traceable(func):
    """Use LangSmith tracing when installed; keep local validation dependency-free."""
    try:
        from langsmith import traceable

        return traceable(name="social-impact-consulting-target")(func)
    except ImportError:
        return func


def _parse_json(text: str) -> dict[str, str]:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.I | re.S)
    payload = json.loads(cleaned)
    required = {"decision", "answer", "next_action"}
    if set(payload) != required or payload["decision"] not in {"proceed", "clarify", "escalate"}:
        raise ValueError("Model response does not match the required schema")
    return {key: str(value).strip() for key, value in payload.items()}


@_traceable
def consulting_target(inputs: dict[str, Any], *, variant: str = "evidence_first") -> dict[str, str]:
    """Generate a structured consulting recommendation from one dataset input."""
    if variant not in VARIANT_INSTRUCTIONS:
        raise ValueError(f"Unknown prompt variant: {variant}")
    try:
        from langsmith.wrappers import wrap_openai
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Install project dependencies before running the cloud target") from exc

    client = wrap_openai(OpenAI())
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
        temperature=0,
        messages=[
            {"role": "system", "content": VARIANT_INSTRUCTIONS[variant]},
            {
                "role": "user",
                "content": f"BRIEF:\n{inputs['brief']}\n\nQUESTION:\n{inputs['question']}",
            },
        ],
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Model returned an empty response")
    return _parse_json(content)

