from streamer import DataStreamer
from htm_model import HTMWorkloadModel
from workload_assessor import SpikeDetector
import queue
import os
import yaml

class Pipeline:
    def __init__(self, data_path, config, interval=0.5):
        self.streamer = DataStreamer(data_path, interval)
        self.htm_model = HTMWorkloadModel(config)
        self.spike_detector = SpikeDetector()
        self.output_queue = queue.Queue()

    def run(self):
        for data in self.streamer.stream():
            print(f"Processing data point: {data}")  # Ensure data is printing
            anomaly_score = self.htm_model.update(data)
            spike = self.spike_detector.detect_spike(anomaly_score)
            self.output_queue.put({
                "input_data": data,
                "anomaly_score": anomaly_score,
                "spike": spike
            })
            print({
                "input_data": data,
                "anomaly_score": anomaly_score,
                "spike": spike
            })  # Clearly print results

if __name__ == '__main__':

    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the paths relative to the script's location
    config_path = os.path.join(current_dir, '..', 'config.yaml')
    data_path = os.path.join(current_dir, '..', 'data', 'nasa_demo_data.csv')

    # Normalize to absolute paths
    config_path = os.path.abspath(config_path)
    data_path = os.path.abspath(data_path)

    # Load YAML configuration explicitly
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Create and run pipeline explicitly
    pipeline = Pipeline(data_path, config)
    pipeline.run()
