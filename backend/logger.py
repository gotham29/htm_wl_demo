# # logger.py
# import csv
# import os

# class Logger:
#     def __init__(self, config):
#         self.log_to_file = config["logging"].get("log_to_file", False)
#         self.log_console = config["logging"].get("log_console", True)
#         self.log_path = config["logging"].get("log_path", "logs/run_log.csv")

#         if self.log_to_file:
#             os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
#             with open(self.log_path, 'w', newline='') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(["timestep", "input", "anomaly_score", "pred_count", "spike_flag"])

#     def log(self, timestep, input_vector, anomaly_score, pred_count, spike_flag):
#         row = [timestep, input_vector, anomaly_score, pred_count, spike_flag]

#         if self.log_console:
#             print(f"[{timestep}] Score: {anomaly_score:.4f}, PredCount: {pred_count}, Spike: {spike_flag}")

#         if self.log_to_file:
#             with open(self.log_path, 'a', newline='') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(row)


# logger.py
import logging
from htm_streamer.utils.logging import get_logger

class Logger:
    def __init__(self, config):
        # Initialize logging based on the config
        self.logger = get_logger()
        self.log_file = config["logging"]["log_file"]
        self.log_level = config["logging"]["log_level"]

        self._setup_logger()

    def _setup_logger(self):
        # Set the logging level and output file
        self.logger.setLevel(self.log_level)
        file_handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log(self, timestep, anomaly_score, spike_flag, detection_lag):
        # Log relevant data during the process
        log_message = f"Timestep: {timestep}, Anomaly Score: {anomaly_score}, Spike Detected: {spike_flag}, Detection Lag: {detection_lag}"
        self.logger.info(log_message)

    def log_error(self, message):
        # Log an error message
        self.logger.error(message)
