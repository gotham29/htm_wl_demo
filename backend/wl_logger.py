import csv
import os

class Logger:
    def __init__(self, log_to_file=True, log_path="logs/output.csv", log_console=True, flush_every=50):
        self.log_to_file = log_to_file
        self.log_console = log_console
        self.log_path = log_path
        self.flush_every = flush_every
        self.buffer = []

        if self.log_to_file:
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            with open(self.log_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestep", "anomaly_score", "spike_flag", "detection_lag"])

    def _initialize_log(self):
        with open(self.log_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestep", "anomaly_score", "spike_flag", "detection_lag"])

    def log(self, timestep, anomaly_score, spike_flag, detection_lag=None):
        row = [timestep, anomaly_score, spike_flag, detection_lag]

        if self.log_console:
            print(f"[{timestep}] Score: {anomaly_score:.4f}, Spike: {spike_flag}, Lag: {detection_lag}")

        if self.log_to_file:
            self.buffer.append(row)
            if len(self.buffer) >= self.flush_every:
                self._flush()

    def clear_log(self):
        """Optional: Clear log file before starting a new cycle."""
        self._initialize_log()

    def _flush(self):
        if not self.buffer:
            return
        with open(self.log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.buffer)
        self.buffer.clear()

    def close(self):
        self._flush()
