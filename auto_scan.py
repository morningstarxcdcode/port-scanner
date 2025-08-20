from scanner.port_scanner import run_scan
from shodan_scan import run_shodan_scan
from wireless.wireless_attacks import run_attack


def run_auto_scan(target, ports="1-1000", scan_type="all", wireless=False):
    print(f"Starting auto scan on {target}")
    run_scan(target, ports, scan_type)
    run_shodan_scan(target)
    if wireless:
        run_attack(target)
    print("Auto scan completed.")
