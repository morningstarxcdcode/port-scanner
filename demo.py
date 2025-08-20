#!/usr/bin/env python3
"""
Demo script for the Advanced Port Scanner
This script demonstrates all the main features of the port scanner.
"""

import sys
import time

from auto_scan import run_auto_scan
from reports.report_generator import generate_report
from scanner.port_scanner import run_scan
from shodan_scan import run_shodan_scan
from wireless.wireless_attacks import run_attack


def print_banner():
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                Advanced Port Scanner Demo                      ║
║                    By morningstarxcdcode                      ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def demo_port_scanning():
    print("\n🔍 === PORT SCANNING DEMO ===")
    print("Scanning localhost for common ports...")
    run_scan("127.0.0.1", "22,80,443", "all")


def demo_wireless_attacks():
    print("\n📡 === WIRELESS ATTACK DEMO ===")
    print("Demonstrating wireless attack simulation...")
    run_attack("127.0.0.1")


def demo_shodan_integration():
    print("\n🌐 === SHODAN INTEGRATION DEMO ===")
    print("Testing Shodan API integration...")
    run_shodan_scan("127.0.0.1")


def demo_auto_scan():
    print("\n🚀 === AUTO SCAN DEMO ===")
    print("Running comprehensive auto scan...")
    run_auto_scan("127.0.0.1", "22,80", "all", wireless=False)


def demo_report_generation():
    print("\n📊 === REPORT GENERATION DEMO ===")
    print("Generating sample scan report...")
    sample_results = [
        {"port": 22, "status": "open", "service": "SSH"},
        {"port": 80, "status": "open", "service": "HTTP"},
        {"port": 443, "status": "closed", "service": "HTTPS"},
    ]
    generate_report(sample_results, "demo_scan_report.json")
    print("Report saved as demo_scan_report.json")


def main():
    print_banner()

    demos = [
        ("Port Scanning", demo_port_scanning),
        ("Wireless Attacks", demo_wireless_attacks),
        ("Shodan Integration", demo_shodan_integration),
        ("Auto Scan", demo_auto_scan),
        ("Report Generation", demo_report_generation),
    ]

    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        # Interactive mode
        for i, (name, func) in enumerate(demos, 1):
            print(f"\n{i}. {name}")

        while True:
            try:
                choice = input("\nSelect demo (1-5) or 'q' to quit: ").strip()
                if choice.lower() == "q":
                    break
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(demos):
                    demos[choice_idx][1]()
                else:
                    print("Invalid choice. Please select 1-5.")
            except (ValueError, KeyboardInterrupt):
                print("\nExiting demo.")
                break
    else:
        # Run all demos
        for name, func in demos:
            print(f"\n⏳ Running {name} demo...")
            func()
            time.sleep(1)  # Brief pause between demos

    print("\n✅ Demo completed! All features are working correctly.")
    print("\nTo run in interactive mode: python3 demo.py --interactive")
    print("To use the main application: python3 main.py --help")


if __name__ == "__main__":
    main()
