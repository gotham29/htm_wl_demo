# logger.py
import csv
import os

class Logger:
    def __init__(self, config):
        self.log_to_file = config["logging"].get("log_to_file", False)
        self.log_console = config["logging"].get("log_console", True)
        self.log_path = config["logging"].get("log_path", "logs/run_log.csv")

        if self.log_to_file:
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            with open(self.log_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["timestep", "input", "anomaly_score", "pred_count", "spike_flag"])

    def log(self, timestep, input_vector, anomaly_score, pred_count, spike_flag):
        row = [timestep, input_vector, anomaly_score, pred_count, spike_flag]

        if self.log_console:
            print(f"[{timestep}] Score: {anomaly_score:.4f}, PredCount: {pred_count}, Spike: {spike_flag}")

        if self.log_to_file:
            with open(self.log_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(row)
