
import logging

logger = logging.getLogger(__name__)

REQUIRED_TOP_LEVEL_KEYS = ["features", "models_params", "models_state",
                           "models_encoders", "spatial_anomaly", "models_predictor"]

def validate_config(config):
    missing_keys = [key for key in REQUIRED_TOP_LEVEL_KEYS if key not in config]
    if missing_keys:
        raise ValueError(f"Missing required top-level config keys: {missing_keys}")

    for feature, params in config.get("features", {}).items():
        if "min" not in params or "max" not in params:
            raise ValueError(f"Feature '{feature}' must include both 'min' and 'max' values.")

    logger.info("Configuration validated successfully.")


# config_validator.py
def validate_config(config):
    assert "htm_params" in config, "Missing 'htm_params' section"
    assert "spike_detection" in config, "Missing 'spike_detection' section"

    htm = config["htm_params"]
    assert 0.0 <= htm["anomaly_threshold"] <= 1.0, "Invalid 'anomaly_threshold'"
    assert htm["input_keys"], "At least one input feature must be specified"

    spike = config["spike_detection"]
    assert spike["recent_window"] > 0, "recent_window must be > 0"
    assert spike["prior_window"] > spike["recent_window"], "prior_window must be larger than recent_window"
    assert 0 < spike["growth_threshold"] < 1000, "growth_threshold should be a positive percent between 0 and 1000"

    logger.info("Configuration validated successfully.")
