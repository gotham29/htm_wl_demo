import time
import os
import yaml
import pandas as pd
from htm_model import HTMWorkloadModel
from spike_detector import SpikeDetector
from wl_logger import Logger

# Load the NASA demo dataset once
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(repo_root, "config.yaml")
data_path = os.path.join(repo_root, "data", "nasa_demo_data.csv")

demo_df = pd.read_csv(data_path)
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

input_columns = list(config['features'])

# Initialize HTM model and Spike detector
model = HTMWorkloadModel(config=config)
spike_detector = SpikeDetector()
logger = Logger(log_dir = "backend/logs/stream_steps")  #Logger(log_path="backend/logs/stream_output.csv")

while True:
    logger.clear_logs()  # start fresh each loop
    print("Looping demo data...")

    for timestep, row in demo_df.iterrows():
        input_vector = {feat: row[feat] for feat in input_columns}
        model_output = model.update(input_vector)
        anomaly_score = model_output[0]
        is_spike, lag = spike_detector.update(anomaly_score, timestep)
        logger.log(timestep, anomaly_score, is_spike, lag)

        time.sleep(1)  # Match frontend refresh interval
