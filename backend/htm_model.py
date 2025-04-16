from htm_streamer import HTMmodel 

class HTMWorkloadModel:
    def __init__(self, config):
        self.model = HTMmodel(config)
        self.initialized = False

    def update(self, data_point):
        if not self.initialized:
            self.model.initialize(data_point)
            self.initialized = True
        return self.model.run_realtime(data_point)
