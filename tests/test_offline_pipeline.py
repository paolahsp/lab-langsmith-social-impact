from social_impact_eval.offline_run import run


def test_offline_ab_pipeline() -> None:
    rows, metrics = run()
    assert len(rows) == 30
    assert metrics["segments"]["variant:keyword_baseline"]["decision_accuracy"] == 0.8
    assert metrics["segments"]["variant:risk_aware"]["decision_accuracy"] == 1.0
    assert len(metrics["failures"]) == 3

