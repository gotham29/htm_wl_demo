import streamlit as st
import pandas as pd
import altair as alt
import time
import os

st.set_page_config(page_title="HTM-WL Realtime Demo", layout="wide")
st.title("\U0001F680 HTM-WL Real-Time Dashboard")
st.markdown("This dashboard streams HTM workload anomaly scores with spike detection.")

# Sidebar controls
log_path = st.sidebar.text_input("\U0001F50D Path to Stream Log", value="backend/logs/stream_output.csv")
refresh_interval = st.sidebar.slider("\u23F1 Refresh Interval (seconds)", 1, 10, 1)
n = st.sidebar.slider("\U0001F4CA Rows to Show in Plot", 50, 500, 100)

# Main dashboard loop
placeholder = st.empty()

while True:
    if not os.path.exists(log_path):
        placeholder.warning(f"No data found yet. Waiting for backend to write {os.path.basename(log_path)}...")
        time.sleep(refresh_interval)
        continue

    try:
        df = pd.read_csv(log_path)
    except Exception as e:
        placeholder.error(f"Error reading CSV: {e}")
        time.sleep(refresh_interval)
        continue

    if df.empty:
        placeholder.warning("Log file is currently empty...")
        time.sleep(refresh_interval)
        continue

    df = df.sort_values("timestep")
    recent_df = df.tail(n)

    latest_row = recent_df.iloc[-1]
    current_time = int(latest_row['timestep'])
    current_score = latest_row['anomaly_score']
    current_spike = bool(latest_row.get('spike_flag', False))
    current_lag = latest_row.get('detection_lag') if pd.notna(latest_row.get('detection_lag')) else "--"

    with placeholder.container():
        st.subheader("\U0001F4FA Real-Time Streaming Charts")
        st.markdown(f"**\u23F3 Current Timestep:** {current_time} | **\U0001F9E0 Anomaly Score:** {current_score:.2f} | **\u26A1 MWL Spike:** {'YES' if current_spike else 'No'} | **\u23F1 Lag:** {current_lag}")

        # Roll & Pitch Stick Input
        if "RollStick" in df.columns and "PitchStick" in df.columns:
            input_chart = alt.Chart(recent_df.reset_index()).transform_fold(
                ["RollStick", "PitchStick"],
                as_=["Control", "Value"]
            ).mark_line().encode(
                x='timestep:Q',
                y='Value:Q',
                color='Control:N'
            ).properties(title="Roll & Pitch Control Inputs")
            st.altair_chart(input_chart, use_container_width=True)

        # Anomaly Score
        anomaly_chart = alt.Chart(recent_df).mark_line(color='lightblue').encode(
            x='timestep:Q',
            y='anomaly_score:Q'
        ).properties(title="HTM Anomaly Score")

        spike_points = alt.Chart(recent_df[recent_df['spike_flag'] == True]).mark_point(
            color='red', size=60
        ).encode(
            x='timestep:Q',
            y='anomaly_score:Q',
            tooltip=['timestep', 'anomaly_score']
        )

        st.altair_chart(anomaly_chart + spike_points, use_container_width=True)

        # MWL Spike Detector (tick chart)
        spike_ticks = alt.Chart(recent_df[recent_df['spike_flag'] == True]).mark_tick(
            color='red', thickness=3
        ).encode(
            x='timestep:Q',
            y=alt.value(0.5),
            tooltip=['timestep']
        ).properties(title="\u26A1 MWL Spike Detection")
        st.altair_chart(spike_ticks, use_container_width=True)

        # Detection Lag Events
        if 'detection_lag' in df.columns and df['detection_lag'].notna().any():
            lag_chart = alt.Chart(recent_df[recent_df['detection_lag'].notna()]).mark_circle(
                color='orange', size=80
            ).encode(
                x='timestep:Q',
                y=alt.value(0.5),
                tooltip=['timestep', 'detection_lag']
            ).properties(title="\u23F3 Detection Lag Events")

            st.altair_chart(lag_chart, use_container_width=True)

    time.sleep(refresh_interval)
