from social_impact_eval.evaluators import consulting_quality, decision_correctness


def test_decision_correctness_exact_match() -> None:
    result = decision_correctness({}, {"decision": "proceed"}, {"decision": "proceed"})
    assert result == {"key": "decision_correctness", "score": True}


def test_consulting_quality_rewards_grounded_action() -> None:
    inputs = {"brief": "The signed report covers 218 participants before 30 September."}
    outputs = {
        "decision": "proceed",
        "answer": "The signed report covers 218 participants before 30 September.",
        "next_action": "Document and approve the evidence.",
    }
    result = consulting_quality(inputs, outputs, {})
    assert result["score"] >= 0.75

