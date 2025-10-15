from typing import List, Dict
import numpy as np
from sklearn.ensemble import IsolationForest


# Small wrapper for anomaly detection using IsolationForest
class AIAnalyzer:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.store = [] # simplistic fixed window of scalar metrics
        self.model = IsolationForest(contamination=0.02, random_state=42)
        self.fitted = False


    def _extract_metric_vector(self, observations: List[Dict]):
        # flatten observations into numeric vector(s). Example: use rtt_ms or failure flags
        vec = []
        for o in observations:
            rtt = o.get("rtt_ms")
            success = 1.0 if o.get("success") else 0.0
            # normalize missing RTT to large number
            vec.append([0.0 if rtt is None else float(rtt), success])
        return np.array(vec)


    def ingest_and_score(self, observations: List[Dict]) -> List[Dict]:
        """Ingest new observations and return anomaly scores for each observation."""
        X = self._extract_metric_vector(observations)
        if X.size == 0:
            return [{"anomaly_score": 0.0, "is_anomaly": False} for _ in observations]


        # maintain store (simple last N rows)
        if len(self.store) == 0:
            self.store = X.copy()
        else:
            self.store = np.vstack([self.store, X])
        if len(self.store) > self.window_size:
            self.store = self.store[-self.window_size :]


        if len(self.store) >= max(10, int(self.window_size * 0.1)):
            try:
                self.model.fit(self.store)
                self.fitted = True
            except Exception:
                self.fitted = False


        if self.fitted:
            # anomaly_score: negative outlier factor -> convert to positive score
            scores = -self.model.score_samples(X)
            is_anom = self.model.predict(X) == -1
        else:
            scores = np.zeros(X.shape[0])
            is_anom = np.zeros(X.shape[0], dtype=bool)


        out = []
        for s, ia in zip(scores.tolist(), is_anom.tolist()):
            out.append({"anomaly_score": float(s), "is_anomaly": bool(ia)})
        return out