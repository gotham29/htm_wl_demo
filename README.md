
# HTM-WL Demo

This repository demonstrates real-time workload estimation using Hierarchical Temporal Memory (HTM) and behavioral entropy analysis. It is designed to showcase the capabilities of the `htm_streamer` module within a production-oriented backend pipeline. 

## 🧠 What It Does

- Continuously streams operator control data (e.g., from NASA datasets)
- Uses HTM to assess workload by computing anomaly scores
- Detects sudden spikes in mental workload using a lightweight spike detector
- Outputs a real-time queue of data points, anomaly scores, and spike flags

---

## 🗂️ Repository Structure

```
htm_wl_demo/
├── backend/
│   ├── htm_model.py            # Interfaces with HTMStreamer
│   ├── workload_assessor.py    # Spike detection logic
│   ├── streamer.py             # Streams data row-by-row
│   └── main.py                 # Runs the real-time backend
├── data/
│   └── nasa_demo_data.csv      # Sample NASA-like behavioral dataset
├── frontend/
│   └── app.py                  # Placeholder for Streamlit UI (TBD)
├── config.yaml                 # HTM and data stream configuration
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run the Backend

### 1. Clone the Required Repos

```bash
git clone https://github.com/gotham29/htm_wl_demo.git
git clone https://github.com/gotham29/htm_streamer.git
```

### 2. Install Dependencies

> **Note:** You must install [`htm.core`](https://github.com/htm-community/htm.core) from source first.

#### a. Clone and Build `htm.core`

```bash
git clone https://github.com/htm-community/htm.core.git
cd htm.core
python setup.py install
```

#### b. Create Virtual Environment

```bash
cd ../htm_wl_demo
python3 -m venv htm_wl_env
source htm_wl_env/bin/activate
pip install -e ../htm_streamer  # Local install of private package
pip install -r requirements.txt
```

### 3. Run the Demo

```bash
python backend/main.py
```

You should see real-time anomaly scores and spike detection output in the console.

---

## 🔧 Configuration

The `config.yaml` file defines:

- Input feature scaling (min/max per feature)
- HTM model parameters
- Inference interval (in seconds)

Adjust this file to match your data stream.

---

## 🧪 Testing & Data

The system currently runs on a simulated NASA dataset of control inputs. In production, it is intended to interface with streaming operator telemetry in any numeric format.

---

## 🧱 Next Steps

- [ ] Add real-time visualization dashboard using Streamlit
- [ ] Dockerize for deployment
- [ ] Expand anomaly interpretation

---

## 🧑‍💻 Author

Developed by [@gotham29](https://github.com/gotham29) to transition HTM-WL from research to real-time applications.
