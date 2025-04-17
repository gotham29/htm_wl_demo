# backend/runner.py
from htm_model import HTMWorkloadModel
from spike_detector import SpikeDetector
from logger import Logger
from monitor import run_monitor_loop
from utils import load_nasa_data

def run_demo(data_path="data/nasa_roll_pitch.csv"):
    input_keys = ["RollStick", "PitchStick"]
    # anomaly_threshold = 0.5
    recent_window = 1
    prior_window = 2
    growth_threshold = 50

    model = HTMWorkloadModel(input_keys=input_keys) ## UPDATED
    detector = SpikeDetector(recent_window, prior_window, growth_threshold)
    logger = Logger(log_to_file=True, log_path="logs/output.csv", log_console=True)
    data = load_nasa_data(data_path)

    run_monitor_loop(data, model, detector, logger, anomaly_event_timestep=1000)
