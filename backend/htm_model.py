from htm_streamer import HTMStreamer

class HTMWorkloadModel:
    def __init__(self, config):
        self.model = HTMStreamer(config)
        self.initialized = False

    def update(self, data_point):
        if not self.initialized:
            self.model.initialize(data_point)
            self.initialized = True
        return self.model.run_realtime(data_point)
