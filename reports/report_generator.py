"""
Report Generator Module
Author: morningstar
Poster: morningstar's Ethical Hacking Suite
Description: Generates detailed reports for port scans and wireless attacks
"""

import datetime
import json


def generate_report(scan_results, filename=None):
    report = {"scan_date": datetime.datetime.now().isoformat(), "results": scan_results}
    if not filename:
        filename = (
            f"scan_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
    try:
        with open(filename, "w") as f:
            json.dump(report, f, indent=4)
        print(f"Report saved to {filename}")
    except Exception as e:
        print(f"Failed to save report: {e}")
