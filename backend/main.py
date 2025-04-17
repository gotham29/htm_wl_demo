import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

from streamer import DataStreamer
from htm_model import HTMWorkloadModel
from htm_streamer.utils.fs import load_config
from spike_detector import SpikeDetector
from config_validator import validate_config
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
        features = list(config['features'].keys())
        timestamp = 0
        for data in self.streamer.stream():
            timestamp += 1
            input = {feat: round(data[feat],3) for feat in features}
            model_output = self.htm_model.update(data)  #(anomaly_score, anomaly_likelihood, pred_count, steps_predictions)
            anomaly_score = model_output[0]
            pred_count = model_output[2]
            spike = self.spike_detector.detect_spike(anomaly_score)
            self.output_queue.put({
                "input_data": input,
                "anomaly_score": anomaly_score,
                "pred_count": pred_count,
                "spike": spike
            })
            output_str = f"input={input}; workload={anomaly_score}; preds={pred_count}; spike={spike}"
            logger.info(output_str)            


if __name__ == '__main__':

    # Get config & data paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "../config.yaml")
    data_path = os.path.join(current_dir, "../data/nasa_demo_data.csv")

    # Load YAML configuration explicitly
    config = load_config(config_path)
    # with open(config_path, 'r') as file:
    #     config = yaml.safe_load(file)
    validate_config(config)

    # Create and run pipeline explicitly
    pipeline = Pipeline(data_path, config)
    pipeline.run()


