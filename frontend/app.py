import streamlit as st
import pandas as pd
import altair as alt
import os
import time
import glob

st.set_page_config(page_title="HTM-WL Realtime Demo", layout="wide")
st.title("🚀 HTM-WL Real-Time Dashboard")
st.markdown("This dashboard streams HTM workload anomaly scores with spike detection.")

# Sidebar controls
log_dir = st.sidebar.text_input("📂 Log Directory", value="backend/logs/stream_steps")
refresh_interval = st.sidebar.slider("⏱ Refresh Interval (seconds)", 1, 10, 1)
n = st.sidebar.slider("📊 Rows to Show in Plot", 50, 500, 100)

placeholder = st.empty()
latest_timestep = None

while True:
    if not os.path.isdir(log_dir):
        placeholder.warning(f"Waiting for log directory '{log_dir}' to be created...")
        time.sleep(refresh_interval)
        continue

    log_files = sorted(glob.glob(os.path.join(log_dir, "step_*.csv")))
    if not log_files:
        placeholder.warning("No step log files found yet...")
        time.sleep(refresh_interval)
        continue

    # Concatenate most recent log files
    df_list = []
    for file in log_files[-n:]:
        try:
            df = pd.read_csv(file)
            df_list.append(df)
        except Exception as e:
            continue  # skip unreadable files

    if not df_list:
        placeholder.warning("No valid log data yet...")
        time.sleep(refresh_interval)
        continue

    df = pd.concat(df_list, ignore_index=True)

    # UI
    with placeholder.container():
        st.markdown("### 📉 Real-Time Streaming Charts")

        current_step = int(df['timestep'].iloc[-1])
        score = df['anomaly_score'].iloc[-1]
        spike = df['spike_flag'].iloc[-1]
        lag = df['detection_lag'].iloc[-1] if 'detection_lag' in df.columns else None

        status_cols = st.columns(4)
        status_cols[0].markdown(f"**🔄 Current Timestep:** `{current_step}`")
        status_cols[1].markdown(f"**📈 Anomaly Score:** `{score:.3f}`")
        status_cols[2].markdown(f"**⚡ MWL Spike:** `{'Yes' if spike else 'No'}`")
        status_cols[3].markdown(f"**⏳ Lag:** `{int(lag) if pd.notna(lag) else '—'}`")

        anomaly_chart = alt.Chart(df).mark_line(color='lightblue').encode(
            x='timestep:Q',
            y='anomaly_score:Q'
        ).properties(height=300)

        spikes = alt.Chart(df[df['spike_flag'] == True]).mark_point(color='red', size=60).encode(
            x='timestep:Q',
            y='anomaly_score:Q'
        )

        st.altair_chart(anomaly_chart + spikes, use_container_width=True)

        if 'detection_lag' in df.columns and df['detection_lag'].notna().any():
            lag_chart = alt.Chart(df[df['detection_lag'].notna()]).mark_circle(color='orange', size=80).encode(
                x='timestep:Q',
                y=alt.value(1)
            ).properties(title="⏱ Detection Lag Events")
            st.altair_chart(lag_chart, use_container_width=True)

    time.sleep(refresh_interval)
