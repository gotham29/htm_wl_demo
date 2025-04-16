import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


import pandas as pd
import time

class DataStreamer:
    def __init__(self, data_path, interval=0.5):
        self.data = pd.read_csv(data_path)
        self.interval = interval

    def stream(self):
        for _, row in self.data.iterrows():
            yield row.to_dict()
            time.sleep(self.interval)
