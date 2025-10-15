# EdgeSense
*Intelligent Edge Test Automation Framework with ML-powered anomaly detection*

---

## Overview

EdgeSense is a Python framework to **monitor edge network nodes**.  
It performs **HTTP, DNS, and TCP probes**, collects metrics, and applies **ML anomaly detection**.

---

## Features

- Configurable **targets** via YAML or default config
- Runs **HTTP, TCP, and DNS probes**
- **Real-time anomaly detection** using ML/statistical scoring
- **Colorized console output** for terminal
- **DEBUG and INFO logging** for diagnostics
- Fully tested with **unit tests** and **GitHub Actions CI**

---

## Folder Structure

EdgeSense/
├── .github/
│ └── workflows/
│ └── python-ci.yml
├── docs/
├── examples/
├── src/
│ ├── init.py
│ ├── main.py
│ ├── config.py
│ ├── test_runner.py
│ ├── ai_analyzer.py
│ ├── console.py
│ └── logger.py
├── tests/
├── .gitignore
├── README.md
└── requirements.txt


---

## Installation


 git clone <repo_url>
 cd EdgeSense
 pip install -r requirements.txt



## Usage
### Using default config

python -m src.main

### Using YAML targets
python -m src.main examples/targets.yaml


## Example Table Output (Terminal)

| Target     | Probe | Port | Status | RTT (ms) | Anomaly |
| ---------- | ----- | ---- | ------ | -------- | ------- |
| google.com | DNS   |      | True   | 5.97     | OK      |
| google.com | TCP   | 80   | True   | 17.68    | OK      |
| google.com | HTTP  |      | 200    | 896.04   | OK      |
| 1.1.1.1    | DNS   |      | True   | 3.00     | OK      |
| 1.1.1.1    | TCP   | 80   | True   | 25.88    | OK      |


## Configuration

### Default targets in src/config.py:

CONFIG = {
    "run_interval_seconds": 30,
    "targets": [
        ProbeTarget(name="google", address="google.com", probes=["dns","tcp","http"]),
        ProbeTarget(name="cloudflare", address="1.1.1.1", probes=["dns","tcp"])
    ],
    "anomaly_window": 100
}


### YAML example (examples/targets.yaml):

targets:
  - name: google
    address: google.com
    probes: ["dns", "tcp", "http"]
  - name: cloudflare
    address: 1.1.1.1
    probes: ["dns", "tcp"]

## ML Anomaly Detection

### Located in src/ai_analyzer.py

### Maintains a sliding window of recent RTT metrics

### Computes z-score to detect anomalies

### Flags unusual probe results automatically

### Can be upgraded to more advanced ML models
