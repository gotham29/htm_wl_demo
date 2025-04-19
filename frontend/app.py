import streamlit as st
import pandas as pd
import yaml
import os
import sys
import threading
import time
import glob
import numpy as np
sys.path.append('backend')
from demo_runner import run_demo

st.set_page_config(layout="wide")
st.title("🚀 HTM-WL Real-Time Dashboard")

# --- Dataset Paths ---
dataset_root = "datasets"
datasets = [name for name in os.listdir(dataset_root) if os.path.isdir(os.path.join(dataset_root, name))]

# --- Selection Controls ---
data_mode = st.sidebar.radio("Choose Data Source", ["Demo Dataset", "Upload CSV"])
selected_dataset = None
uploaded_df = None
uploaded_config = {}

# --- Shared Variables ---
selected_features = []
recent_window = prior_window = growth_threshold = None
anomaly_event_timesteps = []
data_path = config_path = None

# --- Demo Dataset Mode ---
if data_mode == "Demo Dataset":
    selected_dataset = st.sidebar.selectbox("📁 Select Demo Dataset", datasets)
    config_path = os.path.join(dataset_root, selected_dataset, "config.yaml")
    data_path = os.path.join(dataset_root, selected_dataset, "data.csv")

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    st.sidebar.markdown("---")
    available_features = list(config.get("features", {}).keys())
    selected_features = st.sidebar.multiselect("Select Features", available_features, default=available_features[:1], max_selections=5)

    spike_cfg = config.get("spike_detection", {})
    recent_window = st.sidebar.number_input("Recent Window", 1, 100, spike_cfg.get("recent_window", 5))
    prior_window = st.sidebar.number_input("Prior Window", 1, 100, spike_cfg.get("prior_window", 15))
    growth_threshold = st.sidebar.number_input("Growth Threshold (%)", 1, 500, spike_cfg.get("growth_threshold", 50))

    anomaly_event_timesteps = config.get("anomaly_event_timesteps", [])
    st.sidebar.text(f"Anomaly Timesteps: {anomaly_event_timesteps}")

# --- Upload Mode ---
elif data_mode == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")

    if uploaded_file is not None:
        uploaded_df = pd.read_csv(uploaded_file)
        numeric_cols = uploaded_df.select_dtypes(include=[np.number]).columns.tolist()

        selected_features = st.sidebar.multiselect("Select Features", numeric_cols, default=numeric_cols[:1], max_selections=5)
        recent_window = st.sidebar.number_input("Recent Window", 1, 100, 5)
        prior_window = st.sidebar.number_input("Prior Window", 1, 100, 15)
        growth_threshold = st.sidebar.number_input("Growth Threshold (%)", 1, 500, 50)
        anomaly_text = st.sidebar.text_input("Anomaly Timesteps (comma-separated)", "")

        # Convert anomaly list to ints
        if anomaly_text:
            try:
                anomaly_event_timesteps = [int(x.strip()) for x in anomaly_text.split(",") if x.strip().isdigit()]
            except Exception:
                anomaly_event_timesteps = []

        # Save temp data and config
        os.makedirs("user_data", exist_ok=True)
        data_path = "user_data/uploaded.csv"
        config_path = "user_data/config.yaml"
        uploaded_df.to_csv(data_path, index=False)

        uploaded_config = {
            "features": {},
            "frontend": {
                "plot_window_size": 120,
                "log_dir": "backend/logs/stream_steps"
            },
            "spike_detection": {
                "recent_window": recent_window,
                "prior_window": prior_window,
                "growth_threshold": growth_threshold
            },
            "anomaly_event_timesteps": anomaly_event_timesteps
        }

        for col in selected_features:
            np_dtype = uploaded_df[col].dtype
            if np.issubdtype(np_dtype, np.floating):
                dtype = "float"
            elif np.issubdtype(np_dtype, np.integer):
                dtype = "int"
            else:
                continue  # skip unsupported types

            uploaded_config["features"][col] = {
                "min": float(uploaded_df[col].min()),
                "max": float(uploaded_df[col].max()),
                "type": dtype,
                "weight": 1.0
            }

        with open(config_path, 'w') as f:
            yaml.dump(uploaded_config, f)

# --- Run Button ---
st.sidebar.markdown("---")
run_clicked = st.sidebar.button("▶️ Start Streaming")

# Session flag
if "thread_running" not in st.session_state:
    st.session_state.thread_running = False

# --- Start Background Thread ---
if run_clicked and not st.session_state.thread_running:
    st.success("Starting backend thread...")

    def thread_target():
        print("\n🔁 run_demo() has started execution.")
        run_demo(
            data_path,
            config_path,
            selected_features,
            recent_window,
            prior_window,
            growth_threshold
        )
        st.session_state.thread_running = False

    threading.Thread(target=thread_target, daemon=True).start()
    st.session_state.thread_running = True

# --- Live Plot Section ---
st.markdown("---")
st.subheader("📊 Live Real-Time Plot")
log_dir = "backend/logs/stream_steps"
plot_placeholder = st.empty()
last_files = set()
data_so_far = pd.DataFrame()

if st.session_state.thread_running:
    for _ in range(300):  # limit loop for safety
        step_files = sorted(glob.glob(os.path.join(log_dir, "step_*.csv")))
        new_files = [f for f in step_files if f not in last_files]

        if new_files:
            new_dfs = [pd.read_csv(f) for f in new_files]
            data_so_far = pd.concat([data_so_far] + new_dfs, ignore_index=True)
            last_files.update(new_files)

            # Trim window
            plot_window_size = 120
            data_so_far = data_so_far.tail(plot_window_size)

            with plot_placeholder.container():
                st.metric("Current Timestep", int(data_so_far["timestep"].iloc[-1]))
                st.metric("Anomaly Score", f"{data_so_far['anomaly_score'].iloc[-1]:.3f}")
                st.metric("Spike", "Yes" if data_so_far['spike_flag'].iloc[-1] else "No")
                st.metric("Lag", data_so_far['detection_lag'].iloc[-1])

                st.line_chart(data_so_far.set_index("timestep")["anomaly_score"])

                # Show inputs
                input_cols = [c for c in data_so_far.columns if c not in ["timestep", "anomaly_score", "spike_flag", "detection_lag"]]
                for col in input_cols:
                    st.line_chart(data_so_far.set_index("timestep")[col])

        time.sleep(1)

    st.success("Streaming ended. Reload to start again.")

