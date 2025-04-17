# import logging

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )
# logger = logging.getLogger(__name__)


# import numpy as np

# class SpikeDetector:
#     def __init__(self, threshold=0.8, window=10):
#         self.threshold = threshold
#         self.window = window
#         self.history = []

#     def detect_spike(self, anomaly_score):
#         self.history.append(anomaly_score)
#         if len(self.history) > self.window:
#             self.history.pop(0)
#         avg_anomaly = np.mean(self.history)
#         if anomaly_score > self.threshold and anomaly_score > 1.5 * avg_anomaly:
#             logger.warning(f"Spike detected: {anomaly_score}")
#             return True
#         return False

# backend/spike_detector.py

from collections import deque
import numpy as np

class SpikeDetector:
    def __init__(self, recent_window=1, prior_window=2, growth_threshold=50):
        self.recent_window = recent_window
        self.prior_window = prior_window
        self.growth_threshold = growth_threshold
        self.total_window = prior_window + recent_window
        self.entropy_buffer = deque(maxlen=self.total_window)
        self.last_event = None

    def update(self, score, timestep=None):
        self.append(score)
        if self.ready():
            spike = self.detect_spike()
            lag = timestep - self.last_event if spike and self.last_event is not None else None
            if spike:
                self.last_event = timestep
            return spike, lag
        return False, None

    def append(self, score):
        self.entropy_buffer.append(score)

    def ready(self):
        return len(self.entropy_buffer) == self.total_window

    def detect_spike(self):
        if not self.ready():
            return False

        prior = list(self.entropy_buffer)[:self.prior_window]
        recent = list(self.entropy_buffer)[-self.recent_window:]

        mean_prior = np.mean(prior)
        mean_recent = np.mean(recent)

        if mean_prior == 0:
            return False

        percent_increase = ((mean_recent - mean_prior) / mean_prior) * 100
        return percent_increase > self.growth_threshold
