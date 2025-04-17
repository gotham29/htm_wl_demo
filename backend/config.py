# # config.py
# import yaml
# from config_validator import validate_config

# class Config:
#     def __init__(self, config_path):
#         with open(config_path, 'r') as file:
#             self.config = yaml.safe_load(file)
#         validate_config(self.config)

#     def get(self, key, default=None):
#         return self.config.get(key, default)

#     def __getitem__(self, key):
#         return self.config[key]

#     def __str__(self):
#         return str(self.config)

# config.py
import os
import yaml
from htm_streamer.utils.fs import load_config

class Config:
    def __init__(self, config_file="config.yaml"):  #run_pipeline.yaml
        # Loading configuration from a YAML file using htm_streamer's load_config utility
        self.config = load_config(config_file)
        self._validate_config()

    def _validate_config(self):
        # Perform validation of the loaded configuration (if needed)
        # For now, we assume the config is valid if it loads correctly
        if not self.config:
            raise ValueError(f"Configuration file {config_file} could not be loaded!")

    def __getitem__(self, key):
        return self.config.get(key, None)
