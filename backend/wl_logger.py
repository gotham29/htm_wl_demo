# # import os
# # import csv
# # import json
# # from collections import deque
# # from tempfile import NamedTemporaryFile

# # class Logger:
# #     def __init__(self, log_dir="logs/stream_steps", log_console=True, max_files=100, file_type="csv"):
# #         self.log_dir = log_dir
# #         self.log_console = log_console
# #         self.max_files = max_files
# #         self.file_type = file_type.lower()
# #         self.files_written = deque()

# #         os.makedirs(self.log_dir, exist_ok=True)

# #     def log(self, timestep, anomaly_score, spike_flag, detection_lag=None, extra_data=None):
# #         row = {
# #             "timestep": timestep,
# #             "anomaly_score": anomaly_score,
# #             "spike_flag": spike_flag,
# #             "detection_lag": detection_lag
# #         }

# #         if extra_data:
# #             row.update(extra_data)

# #         if self.log_console:
# #             print(f"[{timestep}] Score: {anomaly_score:.4f}, Spike: {spike_flag}, Lag: {detection_lag}")

# #         filename = f"step_{timestep:03d}.{self.file_type}"
# #         final_path = os.path.join(self.log_dir, filename)

# #         # Atomic write via temp file and rename
# #         with NamedTemporaryFile("w", delete=False, dir=self.log_dir, suffix=".tmp") as tmpfile:
# #             if self.file_type == "csv":
# #                 writer = csv.DictWriter(tmpfile, fieldnames=row.keys())
# #                 writer.writeheader()
# #                 writer.writerow(row)
# #             elif self.file_type == "json":
# #                 json.dump([row], tmpfile)
# #             tmpfile.flush()
# #             os.fsync(tmpfile.fileno())

# #         os.replace(tmpfile.name, final_path)
# #         self.files_written.append(final_path)

# #         if len(self.files_written) > self.max_files:
# #             old_file = self.files_written.popleft()
# #             if os.path.exists(old_file):
# #                 os.remove(old_file)

# #     def clear_logs(self):
# #         for f in os.listdir(self.log_dir):
# #             full_path = os.path.join(self.log_dir, f)
# #             if os.path.isfile(full_path):
# #                 os.remove(full_path)
# #         self.files_written.clear()


# import csv
# import os
# import shutil
# from collections import deque


# class Logger:
#     def __init__(self, log_dir="backend/logs/stream_steps", max_files=200):
#         self.log_dir = log_dir
#         self.max_files = max_files
#         self.files_written = deque()

#         os.makedirs(self.log_dir, exist_ok=True)

#     def clear_logs(self):
#         """Delete all existing step logs."""
#         if os.path.exists(self.log_dir):
#             for f in os.listdir(self.log_dir):
#                 if f.endswith(".csv"):
#                     os.remove(os.path.join(self.log_dir, f))
#         self.files_written.clear()

#     def log(self, timestep, anomaly_score, spike_flag, detection_lag=None):
#         row = [timestep, anomaly_score, spike_flag, detection_lag]
#         step_file = f"step_{timestep:03}.csv"  # zero-padded
#         final_path = os.path.join(self.log_dir, step_file)
#         temp_path = final_path + ".tmp"

#         # Write atomically
#         with open(temp_path, 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(["timestep", "anomaly_score", "spike_flag", "detection_lag"])
#             writer.writerow(row)

#         os.replace(temp_path, final_path)
#         self.files_written.append(final_path)

#         # Enforce rolling log window
#         if len(self.files_written) > self.max_files:
#             old_file = self.files_written.popleft()
#             if os.path.exists(old_file):
#                 os.remove(old_file)


import csv
import os
import shutil
import yaml
from collections import deque

class Logger:
    def __init__(self, config_path="config.yaml", log_dir=None):
        # Load window size from config.yaml
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        frontend_config = config.get("frontend", {})
        self.max_files = frontend_config.get("plot_window_size", 120)
        self.log_dir = log_dir or frontend_config.get("log_dir", "backend/logs/stream_steps")
        self.files_written = deque()

        os.makedirs(self.log_dir, exist_ok=True)

    def clear_logs(self):
        if os.path.exists(self.log_dir):
            for f in os.listdir(self.log_dir):
                if f.endswith(".csv"):
                    os.remove(os.path.join(self.log_dir, f))
        self.files_written.clear()

    def log(self, timestep, anomaly_score, spike_flag, detection_lag=None):
        row = [timestep, anomaly_score, spike_flag, detection_lag]
        step_file = f"step_{timestep:03}.csv"
        final_path = os.path.join(self.log_dir, step_file)
        temp_path = final_path + ".tmp"

        with open(temp_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestep", "anomaly_score", "spike_flag", "detection_lag"])
            writer.writerow(row)

        os.replace(temp_path, final_path)
        self.files_written.append(final_path)

        if len(self.files_written) > self.max_files:
            old_file = self.files_written.popleft()
            if os.path.exists(old_file):
                os.remove(old_file)
