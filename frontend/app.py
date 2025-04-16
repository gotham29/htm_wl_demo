import streamlit as st
import pandas as pd
import numpy as np
import time

st.title('Real-Time HTM-WL Monitoring Dashboard')

data_placeholder = st.empty()
anomaly_chart = st.line_chart()
spike_indicator = st.empty()

def simulate_streaming(filepath):
    data = pd.read_csv(filepath)
    anomaly_scores = []
    for _, row in data.iterrows():
        anomaly_score = np.random.rand()  # Replace with real-time anomaly score from backend
        spike = anomaly_score > 0.8  # Replace with real-time spike detection from backend
        anomaly_scores.append(anomaly_score)

        with data_placeholder.container():
            st.write(f"PitchStick: {row['PitchStick']}, RollStick: {row['RollStick']}")
            st.write(f"Anomaly Score (Workload): {anomaly_score:.2f}")
            spike_indicator.markdown(
                f"<h2 style='color:{'red' if spike else 'green'};'>Spike Detected: {spike}</h2>",
                unsafe_allow_html=True
            )

        anomaly_chart.add_rows([anomaly_score])
        time.sleep(0.5)

if st.button('Start Demo'):
    simulate_streaming('../data/nasa_demo_data.csv')
