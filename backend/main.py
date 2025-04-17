# import logging

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )
# logger = logging.getLogger(__name__)

# from streamer import DataStreamer
# from htm_model import HTMWorkloadModel
# from workload_assessor import SpikeDetector
# from config_validator import validate_config
# import queue
# import os
# import yaml

# class Pipeline:
#     def __init__(self, data_path, config, interval=0.5):
#         self.streamer = DataStreamer(data_path, interval)
#         self.htm_model = HTMWorkloadModel(config)
#         self.spike_detector = SpikeDetector()
#         self.output_queue = queue.Queue()

#     def run(self):
#         for data in self.streamer.stream():
#             output_tuple = self.htm_model.update(data)  #(anomaly_score, anomaly_likelihood, pred_count, steps_predictions)
#             anomaly_score = output_tuple[0]
#             prediction_count = output_tuple[2]
#             spike = self.spike_detector.detect_spike(anomaly_score)
#             self.output_queue.put({
#                 "input_data": data,
#                 "anomaly_score": anomaly_score,
#                 "prediction_count": prediction_count,
#                 "spike": spike
#             })
#             output_str = f"input={data}; workload={anomaly_score}; predcount={prediction_count}; spike={spike}"
#             logger.info(output_str)


# if __name__ == '__main__':

#     # Get config & data paths
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     config_path = os.path.join(current_dir, "../config.yaml")
#     data_path = os.path.join(current_dir, "../data/nasa_demo_data.csv")

#     # Load YAML configuration explicitly
#     with open(config_path, 'r') as file:
#         config = yaml.safe_load(file)
#     validate_config(config)

#     # Create and run pipeline explicitly
#     pipeline = Pipeline(data_path, config)
#     pipeline.run()


# main.py
import os
import time
import numpy as np
from config import Config
from logger import Logger
from htm_model import HTMWorkloadModel  # You should already have this module
from spike_detector import SpikeDetector  # This module compares recent/prior entropy

def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "../data/nasa_demo_data.csv")
    return pd.read_csv(data_path)


def main():
    config = Config("config.yaml")  #"run_pipeline.yaml"
    logger = Logger(config)

    input_keys = config['features'].keys()  #config["htm_params"]["input_keys"]
    recent_window = config["spike_detection"]["recent_window"]
    prior_window = config["spike_detection"]["prior_window"]
    growth_threshold = config["spike_detection"]["growth_threshold"]

    htm_model = HTMWorkloadModel(config)  #(input_keys=input_keys)
    spike_detector = SpikeDetector(recent_window, prior_window, growth_threshold)

    data = load_data()
    timestep = 0
    for row in data:
        timestep += 1
        input_vector = {key: row[key] for key in input_keys}

        model_output = htm_model.update(input_vector)  #(anomaly_score, anomaly_likelihood, pred_count, steps_predictions)
        anomaly_score = model_output[0]
        pred_count = model_output[2]
        spike_detector.append(anomaly_score)

        spike_flag = False
        if spike_detector.ready():
            spike_flag = spike_detector.detect_spike()

        logger.log(timestep, input_vector, anomaly_score, pred_count, spike_flag)

        time.sleep(0.01)

    print("Run complete.")

if __name__ == "__main__":
    main()
