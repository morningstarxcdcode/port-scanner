from integrations.shodan_integration import shodan_scan


def run_shodan_scan(target):
    print(f"Running Shodan scan on {target}")
    shodan_scan(target)
