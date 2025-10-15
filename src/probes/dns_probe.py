import dns.resolver
from typing import Dict


def run_dns_probe(target: str, query_name: str = "example.com", timeout: float = 2.0) -> Dict:
    result = {"target": target, "success": False, "answers": [], "rtt_ms": None, "error": None}
    try:
        import time
        resolver = dns.resolver.Resolver()
        resolver.lifetime = timeout
        start = time.time()
        answers = resolver.resolve(query_name)
        end = time.time()
        result["answers"] = [a.to_text() for a in answers]
        result["success"] = True
        result["rtt_ms"] = (end - start) * 1000
    except Exception as e:
        result["error"] = str(e)
    return result