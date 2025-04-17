import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.spike_detector import SpikeDetector

class TestSpikeDetector(unittest.TestCase):
    def test_spike_detection(self):
        # Prior: mean = 1.0, Recent: mean = 2.0 → 100% growth
        detector = SpikeDetector(recent_window=2, prior_window=2, growth_threshold=50)
        detector.append(1.0)
        detector.append(1.0)
        detector.append(2.0)
        detector.append(2.0)
        self.assertTrue(detector.ready())
        self.assertTrue(detector.detect_spike())

    def test_no_spike_when_below_threshold(self):
        detector = SpikeDetector(recent_window=2, prior_window=2, growth_threshold=150)
        detector.append(1.0)
        detector.append(1.0)
        detector.append(1.5)
        detector.append(1.5)
        self.assertTrue(detector.ready())
        self.assertFalse(detector.detect_spike())

if __name__ == '__main__':
    unittest.main()
