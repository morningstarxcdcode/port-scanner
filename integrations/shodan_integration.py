"""
Shodan Integration Module
Author: morningstar
Poster: morningstar's Ethical Hacking Suite
Description: Integration with Shodan API for enhanced scanning and data retrieval
"""

import os

import shodan  # type: ignore

# Get API key from environment variable or use a demo key
API_KEY = os.environ.get("SHODAN_API_KEY", "demo_key_not_functional")


def shodan_scan(target):
    if not target:
        print("Error: Target IP is required for Shodan scan.")
        return

    if API_KEY == "demo_key_not_functional":
        print(
            "⚠️  Shodan API key not configured. Please set SHODAN_API_KEY environment variable."
        )
        print("   For demo purposes, showing simulated results:")
        print(f"IP: {target}")
        print("Organization: Demo Organization")
        print("Operating System: Unknown")
        print("Open Ports: Demo scan - API key required for real data")
        return

    api = shodan.Shodan(API_KEY)
    try:
        result = api.host(target)
        print(f"IP: {result['ip_str']}")
        print(f"Organization: {result.get('org', 'n/a')}")
        print(f"Operating System: {result.get('os', 'n/a')}")
        print("Open Ports:")
        for port in result.get("ports", []):
            print(f" - {port}")
    except shodan.APIError as e:
        print(f"Shodan API Error: {e}")
        print(
            "Note: This could be due to an invalid API key or IP not found in Shodan database."
        )
    except Exception as e:
        print(f"Unexpected error during Shodan scan: {e}")
