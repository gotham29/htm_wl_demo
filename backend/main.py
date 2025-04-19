# import argparse
# from runner import run_demo

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Run HTM-WL demo pipeline.")
#     parser.add_argument("--config", type=str, default=None, help="Path to config YAML file.")
#     parser.add_argument("--data", type=str, default=None, help="Path to input data CSV.")
#     parser.add_argument("--flush_every", type=int, default=None, help="How many timesteps between log flushes.")

#     args = parser.parse_args()

#     run_demo(
#         config_path=args.config,
#         data_path=args.data,
#         flush_every=args.flush_every
#     )


import time
import os
import yaml
import pandas as pd
from demo_runner import run_demo

CONFIG_SIGNAL_PATH = "backend/selected_config.yaml"

def wait_for_config_selection():
    print("Waiting for dataset selection...")
    while not os.path.exists(CONFIG_SIGNAL_PATH):
        time.sleep(1)
    return CONFIG_SIGNAL_PATH

if __name__ == "__main__":
    config_path = wait_for_config_selection()
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    data_path = config["data_path"]
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at {data_path}")

    df = pd.read_csv(data_path)
    run_demo(df, config)
