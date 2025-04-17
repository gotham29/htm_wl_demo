from htm_model import HTMWorkloadModel
from spike_detector import SpikeDetector
from wl_logger import Logger
from monitor import run_monitor_loop
from utils import load_data

import os
import yaml

def run_demo(data_path=None, config_path=None):
    # Get project root (parent of backend/)
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Set default paths if not provided
    if config_path is None:
        config_path = os.path.join(repo_root, "config.yaml")
    if data_path is None:
        data_path = os.path.join(repo_root, "data", "nasa_demo_data.csv")
    # Load config.yaml
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Extract keys from config
    # input_keys = list(config["features"])
    growth_threshold = config['spike_detection']["growth_threshold"]
    recent_window = config['spike_detection']["recent_window"]
    prior_window = config['spike_detection']["prior_window"]
    anomaly_event_timesteps = config.get("anomaly_event_timesteps", [])
    log_path = config.get("log_path", "logs/output.csv")

    # Initialize components
    model = HTMWorkloadModel(config)
    detector = SpikeDetector(recent_window, prior_window, growth_threshold)
    logger = Logger(log_to_file=True, log_path=log_path, log_console=True)

    # Load data and run
    data = load_data(data_path)
    run_monitor_loop(data, model, detector, logger, anomaly_event_timesteps=anomaly_event_timesteps)
