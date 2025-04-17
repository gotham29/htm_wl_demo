import time

def run_monitor_loop(data, model, detector, logger, anomaly_event_timesteps=None):
    if anomaly_event_timesteps is None:
        anomaly_event_timesteps = []

    unhandled_events = set(anomaly_event_timesteps)
    handled_events = set()
    detection_lag = None

    for row in data:
        input_vector = {key: row[key] for key in model.features}

        anomaly_score = model.update(input_vector)[0]
        detector.append(anomaly_score)

        spike_flag = False
        if detector.ready():
            spike_flag = detector.detect_spike()

        # Assign detection lag only for first spike after a specific unhandled anomaly
        detection_lag = None
        if spike_flag:
            for event_time in sorted(unhandled_events):
                if model.timestep > event_time:
                    detection_lag = model.timestep - event_time
                    handled_events.add(event_time)
                    break  # only report lag for the earliest unhandled event

        # Remove handled events so future spikes don't reuse them
        unhandled_events -= handled_events

        logger.log(model.timestep, anomaly_score, spike_flag, detection_lag)
        
        time.sleep(0.01)