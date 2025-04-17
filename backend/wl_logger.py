import csv
import os
from collections import deque

class Logger:
    def __init__(self, log_dir="logs/stream", log_console=True, max_files=100):
        self.log_dir = log_dir
        self.log_console = log_console
        self.max_files = max_files
        self.files_written = deque()

        os.makedirs(self.log_dir, exist_ok=True)

    def log(self, timestep, anomaly_score, spike_flag, detection_lag=None):
        row = [timestep, anomaly_score, spike_flag, detection_lag]

        if self.log_console:
            print(f"[{timestep}] Score: {anomaly_score:.4f}, Spike: {spike_flag}, Lag: {detection_lag}")

        file_path = os.path.join(self.log_dir, f"step_{timestep:03d}.csv")
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestep", "anomaly_score", "spike_flag", "detection_lag"])
            writer.writerow(row)

        self.files_written.append(file_path)
        if len(self.files_written) > self.max_files:
            old_file = self.files_written.popleft()
            if os.path.exists(old_file):
                os.remove(old_file)

    def clear_logs(self):
        for f in os.listdir(self.log_dir):
            full_path = os.path.join(self.log_dir, f)
            if os.path.isfile(full_path):
                os.remove(full_path)
        self.files_written.clear()
