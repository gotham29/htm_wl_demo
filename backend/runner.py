# from htm_model import HTMWorkloadModel
# from spike_detector import SpikeDetector
# from wl_logger import Logger
# from monitor import run_monitor_loop
# from utils import load_data

# import os
# import yaml

# def run_demo(data_path=None, config_path=None, flush_every=50):
#     # Get project root (parent of backend/)
#     repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#     # Set default paths if not provided
#     if config_path is None:
#         config_path = os.path.join(repo_root, "config.yaml")
#     if data_path is None:
#         data_path = os.path.join(repo_root, "data", "nasa_demo_data.csv")
#     # Load config.yaml
#     with open(config_path, 'r') as file:
#         config = yaml.safe_load(file)

#     # Extract keys from config
#     # input_keys = list(config["features"])
#     growth_threshold = config['spike_detection']["growth_threshold"]
#     recent_window = config['spike_detection']["recent_window"]
#     prior_window = config['spike_detection']["prior_window"]
#     anomaly_event_timesteps = config.get("anomaly_event_timesteps", [])
#     log_path = config.get("log_path", "logs/output.csv")

#     # Initialize components
#     model = HTMWorkloadModel(config)
#     detector = SpikeDetector(recent_window, prior_window, growth_threshold)
#     logger = Logger(
#         log_to_file=True,
#         log_path=log_path,
#         log_console=True,
#         flush_every=flush_every or config.get("log_flush_every", 50)
#     )


#     # Load data and run
#     data = load_data(data_path)
#     run_monitor_loop(data, model, detector, logger, anomaly_event_timesteps=anomaly_event_timesteps)


import time
import pandas as pd
from backend.htm_model import HTMWorkloadModel
from backend.spike_detector import SpikeDetector
from backend.wl_logger import WLLogger

# Load the NASA demo dataset once
demo_df = pd.read_csv("data/nasa_demo_data.csv")
input_columns = ["ROLL_STICK", "PITCH_STIC"]  #"RollStick", "PitchStick"

# Initialize HTM model and Spike detector
model = HTMWorkloadModel(config_path="config.yaml")
spike_detector = SpikeDetector()
logger = WLLogger(log_path="backend/logs/stream_output.csv")

while True:
    logger.clear_log()  # start fresh each loop
    print("Looping demo data...")

    for timestep, row in demo_df.iterrows():
        input_vector = {feat: row[feat] for feat in input_columns}  #{"RollStick": row["RollStick"], "PitchStick": row["PitchStick"]}
        score, _ = model.update(input_vector)
        is_spike, lag = detector.update(score, timestep)

        logger.log({
            "timestep": timestep,
            "anomaly_score": round(score, 3),
            "spike_flag": is_spike,
            "detection_lag": lag if lag is not None else "",
            "RollStick": row["RollStick"],
            "PitchStick": row["PitchStick"]
        })

        time.sleep(1)  # Match frontend refresh interval

# # Start infinite loop through the dataset
# while True:
#     print("[runner.py] Starting one full demo loop of NASA data...")
#     logger.clear_log()
#     for timestep, row in demo_df.iterrows():
#         input_vector = row[input_columns].to_dict()

#         # Update HTM model and get anomaly score
#         score, _ = model.update(input_vector)

#         # Update spike detector
#         spike_flag, detection_lag = spike_detector.update(score, timestep)

#         # Log output
#         logger.log({
#             "timestep": timestep,
#             "anomaly_score": score,
#             "spike_flag": spike_flag,
#             "detection_lag": detection_lag,
#             **input_vector  # log RollStick, PitchStick
#         })

#         time.sleep(1)  # Match frontend refresh interval
