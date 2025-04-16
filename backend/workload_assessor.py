import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


import numpy as np

class SpikeDetector:
    def __init__(self, threshold=0.8, window=10):
        self.threshold = threshold
        self.window = window
        self.history = []

    def detect_spike(self, anomaly_score):
        self.history.append(anomaly_score)
        if len(self.history) > self.window:
            self.history.pop(0)
        avg_anomaly = np.mean(self.history)
        if anomaly_score > self.threshold and anomaly_score > 1.5 * avg_anomaly:
            logger.warning(f"Spike detected: {anomaly_score}")
            return True
        return False
