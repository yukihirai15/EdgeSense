import requests
from typing import Dict


LOGGER_NAME = "http_probe"


def run_http_probe(target: str, timeout: float = 5.0) -> Dict:
    """Run a simple HTTP GET and return a small result dict."""
    result = {"target": target, "success": False, "status_code": None, "rtt_ms": None, "error": None}
    try:
        import time
        start = time.time()
        r = requests.get(f"http://{target}", timeout=timeout)
        end = time.time()
        result.update({
            "success": r.ok,
            "status_code": r.status_code,
            "rtt_ms": (end - start) * 1000,
        })
    except Exception as e:
        result["error"] = str(e)
    return result