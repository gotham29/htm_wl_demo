from htm_streamer import HTMmodel
from htm_streamer.data import Feature
from htm_streamer.utils import frozendict 
from htm_streamer.config import build_enc_params

class HTMWorkloadModel:
    def __init__(self, config):
        self.timestep = 0
        features_enc_params = build_enc_params(features=config['features'],
                                               models_encoders=config['models_encoders'])
        features = {name: Feature(name, params) for name, params in features_enc_params.items()}
        self.model = HTMmodel(features=frozendict(features),
                              use_spatial_pooler=config['models_state']['use_sp'],
                              return_pred_count=config['models_state']['return_pred_count'],
                              models_params=config['models_params'],
                              predictor_config=config['models_predictor'],
                              spatial_anomaly_config=config['spatial_anomaly'])

    def update(self, data_point, learn=True):
        self.timestep += 1
        print(f"data_point = \n{data_point}")
        return self.model.run(data_point, self.timestep, learn)
