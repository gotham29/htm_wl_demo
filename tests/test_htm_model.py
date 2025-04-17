import pytest

@pytest.mark.skip(reason="Native HTM bindings not available in this env")
def test_model_returns_anomaly_score():
    ...
