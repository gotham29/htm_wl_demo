# backend/monitor.py
import time

def run_monitor_loop(data, model, detector, logger, anomaly_event_timestep=1000):
    timestep = 0
    lag_start = None
    detection_lag = None

    for row in data:
        timestep += 1
        input_vector = {key: row[key] for key in model.input_keys}

        anomaly_score = model.update(input_vector)[0]
        detector.append(anomaly_score)

        spike_flag = False
        if detector.ready():
            spike_flag = detector.detect_spike()

        if timestep == anomaly_event_timestep:
            lag_start = timestep
        if spike_flag and lag_start and detection_lag is None:
            detection_lag = timestep - lag_start

        logger.log(timestep, anomaly_score, spike_flag, detection_lag)
        time.sleep(0.01)
