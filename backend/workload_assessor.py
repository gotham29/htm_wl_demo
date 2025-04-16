import numpy as np

class SpikeDetector:
    def __init__(self, window_size=10, threshold=0.7):
        self.window_size = window_size
        self.threshold = threshold
        self.history = []

    def detect_spike(self, anomaly_score):
        self.history.append(anomaly_score)
        if len(self.history) > self.window_size:
            self.history.pop(0)
        avg_anomaly = np.mean(self.history)
        return anomaly_score > (avg_anomaly + self.threshold)
