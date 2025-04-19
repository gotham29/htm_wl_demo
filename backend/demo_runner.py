import time
import yaml
import pandas as pd
from htm_model import HTMWorkloadModel
from spike_detector import SpikeDetector
from wl_logger import Logger

def run_demo(data_path, config_path, selected_features, recent_window, prior_window, growth_threshold):
    
    print("🔁 run_demo() has started execution.")

    # Load dataset and config
    df = pd.read_csv(data_path)
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Inject UI choices into config
    config['features'] = {feat: config['features'][feat] for feat in selected_features}
    config['spike_detection'] = {
        'recent_window': recent_window,
        'prior_window': prior_window,
        'growth_threshold': growth_threshold
    }

    logger = Logger(log_dir=config['frontend']['log_dir'])
    logger.clear_logs()

    def init_model_objects(cfg):
        model = HTMWorkloadModel(config=cfg)
        spike_detector = SpikeDetector(
            recent_window=cfg["spike_detection"]["recent_window"],
            prior_window=cfg["spike_detection"]["prior_window"],
            growth_threshold=cfg["spike_detection"]["growth_threshold"],
            anomaly_event_timesteps=cfg.get("anomaly_event_timesteps", [])
        )
        return model, spike_detector

    print(f"▶️ Streaming started for {data_path}")
    model, spike_detector = init_model_objects(config)

    for timestep, row in df.iterrows():
        input_vector = {feat: row[feat] for feat in config['features']}
        score = model.update(input_vector)[0]
        spike, lag = spike_detector.update(score, timestep)
        logger.log(
            timestep=timestep,
            anomaly_score=score,
            spike_flag=spike,
            detection_lag=lag,
            input_vector=input_vector
        )

        time.sleep(1)
