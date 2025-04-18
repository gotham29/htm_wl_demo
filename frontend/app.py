import streamlit as st
import pandas as pd
import altair as alt
import os
import time
import yaml
from glob import glob

# --- CONFIGURATION ---
DEFAULT_LOG_DIR = "backend/logs/stream_steps"
DEFAULT_REFRESH_INTERVAL = 2
DEFAULT_WINDOW_SIZE = 120
CONFIG_YAML_PATH = "config.yaml"

# --- PAGE SETUP ---
st.set_page_config(page_title="HTM-WL Realtime Dashboard", layout="wide")
st.title("🚀 HTM-WL Real-Time Dashboard")
st.markdown("This dashboard streams HTM workload anomaly scores with spike detection.")

# --- SIDEBAR ---
log_dir = st.sidebar.text_input("🗂 Log Directory", value=DEFAULT_LOG_DIR)
refresh_interval = st.sidebar.slider("⏱ Refresh Interval (seconds)", 1, 10, DEFAULT_REFRESH_INTERVAL)
window_size = st.sidebar.slider("📊 Rows to Show in Plot", 50, 500, DEFAULT_WINDOW_SIZE)

# --- FEATURE EXTRACTION FROM CONFIG ---
def get_input_features_from_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config.get('features', [])
    except Exception as e:
        st.warning(f"Failed to read features from {config_path}: {e}")
        return []

input_features = get_input_features_from_config(CONFIG_YAML_PATH)

# --- MAIN DISPLAY PLACEHOLDER ---
placeholder = st.empty()

# --- MAIN LOOP ---
last_seen_files = set()

while True:
    if not os.path.exists(log_dir):
        placeholder.warning(f"Waiting for log directory '{log_dir}' to be created...")
        time.sleep(refresh_interval)
        continue

    step_files = sorted(glob(os.path.join(log_dir, "step_*.csv")))

    if not step_files:
        placeholder.warning("No step log files found yet...")
        time.sleep(refresh_interval)
        continue

    # Track newly seen files
    new_files = [f for f in step_files if f not in last_seen_files]
    last_seen_files.update(step_files)

    try:
        # Read only the most recent N files
        files_to_read = step_files[-window_size:]
        dfs = [pd.read_csv(f) for f in files_to_read if os.path.isfile(f)]
        df = pd.concat(dfs).sort_values(by="timestep")
    except Exception as e:
        placeholder.error(f"Data loading error: {e}")
        time.sleep(refresh_interval)
        continue

    if df.empty or "timestep" not in df.columns:
        placeholder.warning("No valid data found in the files.")
        time.sleep(refresh_interval)
        continue

    # --- DASHBOARD CONTENT ---
    with placeholder.container():
        st.markdown("## 📉 Real-Time Streaming Charts")

        current_timestep = int(df["timestep"].iloc[-1])
        current_score = df["anomaly_score"].iloc[-1]
        current_spike = df["spike_flag"].iloc[-1]
        current_lag = df["detection_lag"].iloc[-1] if not pd.isna(df["detection_lag"].iloc[-1]) else "-"

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🕓 Current Timestep", current_timestep)
        col2.metric("📈 Anomaly Score", f"{current_score:.3f}")
        col3.metric("⚡ MWL Spike", "Yes" if current_spike else "No")
        col4.metric("⏳ Lag", current_lag)

        # --- ANOMALY SCORE PLOT ---
        base = alt.Chart(df).encode(x='timestep:Q')
        anomaly_line = base.mark_line(color='lightblue').encode(y='anomaly_score:Q')
        spikes = base.transform_filter("datum.spike_flag == true").mark_point(color='red', size=60).encode(y='anomaly_score:Q')
        st.altair_chart(anomaly_line + spikes, use_container_width=True)

        # --- INPUT FEATURE PLOTS ---
        if input_features:
            for feature in input_features:
                if feature in df.columns:
                    st.altair_chart(
                        alt.Chart(df).mark_line().encode(
                            x='timestep:Q',
                            y=alt.Y(f'{feature}:Q', title=feature),
                            tooltip=['timestep', feature]
                        ).properties(title=f"🎮 Input Feature: {feature}"),
                        use_container_width=True
                    )

        # --- DETECTION LAG EVENTS ---
        if 'detection_lag' in df.columns:
            lag_events = df[df['detection_lag'].notna()]
            if not lag_events.empty:
                st.altair_chart(
                    alt.Chart(lag_events).mark_circle(size=80, color='orange').encode(
                        x='timestep:Q',
                        y=alt.value(1),
                        tooltip=['timestep', 'detection_lag']
                    ).properties(title="⌛ Detection Lag Events"),
                    use_container_width=True
                )

    time.sleep(refresh_interval)
