import argparse
from runner import run_demo

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run HTM-WL demo pipeline.")
    parser.add_argument("--config", type=str, default=None, help="Path to config YAML file.")
    parser.add_argument("--data", type=str, default=None, help="Path to input data CSV.")
    parser.add_argument("--flush_every", type=int, default=None, help="How many timesteps between log flushes.")

    args = parser.parse_args()

    run_demo(
        config_path=args.config,
        data_path=args.data,
        flush_every=args.flush_every
    )
