import socket
from typing import Dict


def run_tcp_probe(target: str, port: int = 80, timeout: float = 3.0) -> Dict:
    result = {"target": target, "port": port, "success": False, "rtt_ms": None, "error": None}
    try:
        import time
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        start = time.time()
        s.connect((target, port))
        end = time.time()
        s.close()
        result["success"] = True
        result["rtt_ms"] = (end - start) * 1000
    except Exception as e:
        result["error"] = str(e)
    return result