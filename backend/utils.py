# backend/utils.py

import pandas as pd

def load_data(filepath):
    """
    Loads CSV data and returns a list of row dicts for streaming.

    Each row becomes a dictionary: { "RollStick": value, "PitchStick": value, ... }
    """
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found: {filepath}")

    return df.to_dict(orient="records")
