import csv
import os
import shutil
import yaml
from collections import deque

class Logger:
    def __init__(self, config_path="config.yaml", log_dir=None):
        # Load config
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        frontend_config = config.get("frontend", {})

        # Set up logging directory and window size
        self.log_dir = log_dir or frontend_config.get("log_dir", "backend/logs/stream_steps")
        self.max_files = frontend_config.get("plot_window_size", 120)

        os.makedirs(self.log_dir, exist_ok=True)  # ✅ Ensure log directory exists
        self.files_written = deque()

    def clear_logs(self):
        if os.path.exists(self.log_dir):
            for f in os.listdir(self.log_dir):
                if f.endswith(".csv"):
                    os.remove(os.path.join(self.log_dir, f))
        self.files_written.clear()

    # def log(self, timestep, anomaly_score, spike_flag, detection_lag=None):
    #     row = [timestep, anomaly_score, spike_flag, detection_lag]
    #     step_file = f"step_{timestep:03}.csv"
    #     final_path = os.path.join(self.log_dir, step_file)
    #     temp_path = final_path + ".tmp"

    #     with open(temp_path, 'w', newline='') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(["timestep", "anomaly_score", "spike_flag", "detection_lag"])
    #         writer.writerow(row)

    #     os.replace(temp_path, final_path)
    #     self.files_written.append(final_path)

    #     # Enforce sliding window size
    #     if len(self.files_written) > self.max_files:
    #         old_file = self.files_written.popleft()
    #         if os.path.exists(old_file):
    #             os.remove(old_file)
    def log(self, timestep, anomaly_score, spike_flag, detection_lag=None, input_vector=None):
        row = {
            "timestep": timestep,
            "anomaly_score": anomaly_score,
            "spike_flag": spike_flag,
            "detection_lag": detection_lag
        }

        if input_vector:
            row.update(input_vector)  # add model input features to the row

        step_file = f"step_{timestep:03}.csv"
        final_path = os.path.join(self.log_dir, step_file)
        temp_path = final_path + ".tmp"

        with open(temp_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            writer.writeheader()
            writer.writerow(row)

        os.replace(temp_path, final_path)
        self.files_written.append(final_path)

        if len(self.files_written) > self.max_files:
            old_file = self.files_written.popleft()
            if os.path.exists(old_file):
                os.remove(old_file)

