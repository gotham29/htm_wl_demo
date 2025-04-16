from streamer import DataStreamer
from htm_model import HTMWorkloadModel
from workload_assessor import SpikeDetector
import queue

class Pipeline:
    def __init__(self, data_path, config, interval=0.5):
        self.streamer = DataStreamer(data_path, interval)
        self.htm_model = HTMWorkloadModel(config)
        self.spike_detector = SpikeDetector()
        self.output_queue = queue.Queue()

    def run(self):
        for data in self.streamer.stream():
            anomaly_score = self.htm_model.update(data)
            spike = self.spike_detector.detect_spike(anomaly_score)
            self.output_queue.put({
                "input_data": data,
                "anomaly_score": anomaly_score,
                "spike": spike
            })
