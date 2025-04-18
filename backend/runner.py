import time
import os
import yaml
import pandas as pd
from htm_model import HTMWorkloadModel
from spike_detector import SpikeDetector
from wl_logger import Logger

# Resolve repo paths
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(repo_root, "config.yaml")
data_path = os.path.join(repo_root, "data", "nasa_demo_data.csv")

# Load dataset and config
demo_df = pd.read_csv(data_path)
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

input_columns = list(config['features'])
logger = Logger(log_dir="backend/logs/stream_steps")
logger.clear_logs()  # Only once at the very beginning

def init_model_objects(cfg):
    model = HTMWorkloadModel(config=cfg)
    spike_detector = SpikeDetector(
        recent_window=cfg["spike_detection"]["recent_window"],
        prior_window=cfg["spike_detection"]["prior_window"],
        growth_threshold=cfg["spike_detection"]["growth_threshold"],
        anomaly_event_timesteps=cfg.get("anomaly_event_timesteps", [])
    )
    return model, spike_detector

# Streaming loop
while True:
    # Initialize model
    model, spike_detector = init_model_objects(config)
    # Clear logs at the beginning of each loop to reset frontend plot
    logger.clear_logs()
    # Loop over demo file
    for timestep, row in demo_df.iterrows():
        input_vector = {feat.strip(): row[feat] for feat in input_columns}
        anomaly_score = model.update(input_vector)[0]
        is_spike, lag = spike_detector.update(anomaly_score, timestep)
        logger.log(timestep, anomaly_score, is_spike, lag)
        if timestep % 10 == 0:
            print(f"Step {timestep}: score={anomaly_score:.4f} | spike={is_spike} | lag={lag}")
        time.sleep(1)
