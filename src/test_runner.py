import time
import concurrent.futures
from .config import ProbeTarget
from typing import List, Dict
from .probes import http_probe, dns_probe, tcp_probe
from .logger import setup_logger


logger = setup_logger("test_runner")


PROBE_MAP = {
    "http": http_probe.run_http_probe,
    "dns": dns_probe.run_dns_probe,
    "tcp": tcp_probe.run_tcp_probe,
}




def run_probes_for_target(target: ProbeTarget) -> List[Dict]:
    tasks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futures = []
        for probe_name in target.probes:  # <-- use attribute, not .get()
            fn = PROBE_MAP.get(probe_name)
            if not fn:
                logger.warning("Unknown probe %s for target %s", probe_name, target.name)
                continue
            futures.append(ex.submit(fn, target.address))
        for fut in concurrent.futures.as_completed(futures):
            try:
                tasks.append(fut.result())
            except Exception as e:
                logger.exception("Probe raised: %s", e)
    return tasks




def collect_run(targets: List[ProbeTarget]) -> List[Dict]:
    aggregated = []
    for t in targets:
        aggregated.extend(run_probes_for_target(t))
    return aggregated