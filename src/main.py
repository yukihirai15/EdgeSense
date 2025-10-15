import time
import yaml
import sys
from tabulate import tabulate
from colorama import Fore, Style, init
from .config import CONFIG, ProbeTarget
from .logger import setup_logger
from .test_runner import collect_run
from .ai_analyzer import AIAnalyzer
from .utils.console import print_probe_results

init(autoreset=True, convert=True, wrap=True)

#logger = setup_logger("main")
logger = setup_logger("main", level="DEBUG") # TEST




def load_targets_from_file(path: str):
    with open(path) as f:
        raw = yaml.safe_load(f)
    targets = [ProbeTarget(**t) for t in raw.get("targets", [])]
    return targets




def main(config_path: str = None):
    # simple orchestrator
    logger.info("Starting Intelligent Edge Test Framework")
    targets = CONFIG.get("targets")
    if config_path:
        targets = load_targets_from_file(config_path)


    analyzer = AIAnalyzer(window_size=CONFIG.get("anomaly_window", 100))


    try:
        while True:
            results = collect_run(targets)
            ##########################print("Probe results:", results)  # show raw results
            analysis = analyzer.ingest_and_score(results)

            # Pretty-print results using the console module
            print_probe_results(results, analysis)

        # simple reporting: print anomalies
            for r, a in zip(results, analysis):
                logger.debug("Probe result: %s | Analysis: %s", r, a) ##### DEBUG  #####
                if a["is_anomaly"]:
                    logger.warning("Anomaly detected: %s => %s", r, a)
            time.sleep(CONFIG.get("run_interval_seconds", 30))
    except KeyboardInterrupt:
        logger.info("Shutting down")




if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else None
    main(config_path)