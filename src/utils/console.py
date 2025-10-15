from tabulate import tabulate
from colorama import Fore, Style, init

init(autoreset=True)

def print_probe_results(results, analysis):
    table = []
    for r, a in zip(results, analysis):
        # Determine probe type
        if "answers" in r:
            probe_type = "DNS"
        elif "status_code" in r:
            probe_type = "HTTP"
        elif "port" in r:
            probe_type = "TCP"
        else:
            probe_type = "Unknown"

        status = "ANOMALY!" if a["is_anomaly"] else "OK"
        color = Fore.RED if a["is_anomaly"] else Fore.GREEN

        row = [
            color + str(r.get("target", "")) + Style.RESET_ALL,
            probe_type,  # NEW column
            str(r.get("port", "")),
            str(r.get("status_code", r.get("success", ""))),
            f"{r.get('rtt_ms', ''):.2f}" if r.get("rtt_ms") else "",
            status
        ]
        table.append(row)

    headers = ["Target", "Probe", "Port", "Status", "RTT (ms)", "Anomaly"]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
