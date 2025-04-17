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
import time
import numpy as np
from config import Config
from logger import Logger
from htm_model import HTMWorkloadModel  # Preserved from your repo
from spike_detector import SpikeDetector  # Custom logic for spike detection

def load_data(config):
    # Use the data loading utility provided by htm_streamer
    from htm_streamer.data import load_nasa_data
    return load_nasa_data(config["data"]["data_file"])

def main():
    # Load configuration
    config = Config("run_pipeline.yaml")
    logger = Logger(config)

    # Retrieve HTM parameters from the config
    input_keys = config["htm_params"]["input_keys"]
    anomaly_threshold = config["htm_params"]["anomaly_threshold"]

    # Initialize the HTM model and spike detector
    htm = HTMWorkloadModel(input_keys=input_keys)  # Keep custom model
    spike_detector = SpikeDetector(config["spike_detection"]["recent_window"],
                                   config["spike_detection"]["prior_window"],
                                   config["spike_detection"]["growth_threshold"])

    # Load the data
    data = load_data(config)
    lag_start = None
    detection_lag = None
    timestep = 0

    for row in data:
        timestep += 1
        input_vector = {key: row[key] for key in input_keys}

        # Update the HTM model and calculate anomaly score
        anomaly_score = htm.update(input_vector)[0]  # Assuming the model returns a tuple: (score, sdr)

        # Detect spikes
        spike_detector.append(anomaly_score)
        spike_flag = False
        if spike_detector.ready():
            spike_flag = spike_detector.detect_spike()

        # Log the results
        if timestep == 1000:  # Simulating a known MWL-inducing event
            lag_start = timestep

        if spike_flag and lag_start and detection_lag is None:
            detection_lag = timestep - lag_start

        logger.log(timestep, anomaly_score, spike_flag, detection_lag)

        # Simulate real-time stream (adjust as needed for your setup)
        time.sleep(0.01)

    print("Run complete.")

if __name__ == "__main__":
    main()
