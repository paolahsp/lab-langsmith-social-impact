from social_impact_eval.common import load_examples
from social_impact_eval.validate import validate_examples


def test_dataset_has_required_size_and_diversity() -> None:
    summary = validate_examples(load_examples())
    assert summary["examples"] == 15
    assert len(summary["categories"]) >= 5
    assert set(summary["difficulties"]) == {"easy", "medium", "hard"}


def test_decision_classes_are_balanced() -> None:
    summary = validate_examples(load_examples())
    assert summary["decisions"] == {"proceed": 5, "clarify": 5, "escalate": 5}

