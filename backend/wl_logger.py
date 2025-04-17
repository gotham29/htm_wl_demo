# backend/wl_logger.py

import csv
import os

class Logger:
    def __init__(self, log_to_file=True, log_path="logs/output.csv", log_console=True):
        self.log_to_file = log_to_file
        self.log_console = log_console
        self.log_path = log_path

        if self.log_to_file:
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            with open(self.log_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestep", "anomaly_score", "spike_flag", "detection_lag"])

    def log(self, timestep, anomaly_score, spike_flag, detection_lag=None):
        row = [timestep, anomaly_score, spike_flag, detection_lag]

        if self.log_console:
            print(f"[{timestep}] Score: {anomaly_score:.4f}, Spike: {spike_flag}, Lag: {detection_lag}")

        if self.log_to_file:
            with open(self.log_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)
