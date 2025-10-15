from dataclasses import dataclass
from typing import List


@dataclass
class ProbeTarget:
    name: str
    address: str
    probes: List[str] # e.g. ["http", "dns", "tcp"]


# Example runtime config (would be loaded from YAML/ENV)
CONFIG = {
    "run_interval_seconds": 5,
    "targets": [
        ProbeTarget(name="edge-us-1", address="edge-us-1.example.net", probes=["http","tcp"]),
        ProbeTarget(name="edge-eu-1", address="8.8.8.8", probes=["dns","tcp"]),
    ],
    "anomaly_window": 100,
}