from collections import deque
import numpy as np


class SpikeDetector:
    def __init__(self, recent_window=1, prior_window=2, growth_threshold=50, anomaly_event_timesteps=None):
        self.recent_window = recent_window
        self.prior_window = prior_window
        self.growth_threshold = growth_threshold
        self.total_window = recent_window + prior_window
        self.entropy_buffer = deque(maxlen=self.total_window)
        self.anomaly_event_timesteps = anomaly_event_timesteps or []
        self.detected_events = set()  # Tracks anomaly events that have been flagged

    def update(self, score, timestep):
        self.entropy_buffer.append(score)
        if len(self.entropy_buffer) < self.total_window:
            return False, None

        prior = list(self.entropy_buffer)[:self.prior_window]
        recent = list(self.entropy_buffer)[-self.recent_window:]
        mean_prior = sum(prior) / len(prior)
        mean_recent = sum(recent) / len(recent)

        if mean_prior == 0:
            return False, None

        percent_increase = ((mean_recent - mean_prior) / mean_prior) * 100
        is_spike = percent_increase > self.growth_threshold

        if is_spike:
            # Only report lag if tied to an anomaly event
            for anomaly_time in sorted(self.anomaly_event_timesteps, reverse=True):
                if anomaly_time <= timestep and anomaly_time not in self.detected_events:
                    lag = timestep - anomaly_time
                    self.detected_events.add(anomaly_time)
                    return True, lag
            return True, None  # Detected spike, but not a new event-based one
        return False, None

    def reset(self):
        self.entropy_buffer.clear()
        self.detected_events.clear()
