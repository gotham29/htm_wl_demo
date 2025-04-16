import pandas as pd
import time

class DataStreamer:
    def __init__(self, filepath, interval=0.5):
        self.data = pd.read_csv(filepath)
        self.interval = interval

    def stream(self):
        for _, row in self.data.iterrows():
            yield row.to_dict()
            time.sleep(self.interval)
