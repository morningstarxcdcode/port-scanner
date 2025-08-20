"""
Main entry point for Advanced Port Scanner and Wireless Attack Tool
Author: morningstarxcdcode
Poster: morningstarxcdcode's Ethical Hacking Suite
Description: CLI and GUI launcher with modular scanning and wireless attack options
"""

import argparse
from scanner import port_scanner
from wireless import wireless_attacks
from utils import logger

def main():
    parser = argparse.ArgumentParser(description="Ultimate Advanced Port Scanner and Wireless Attack Tool")
    parser.add_argument("--mode", choices=["cli", "gui"], default="cli", help="Run mode: cli or gui")
    parser.add_argument("--target", help="Target IP or hostname")
    parser.add_argument("--ports", default="1-65535", help="Port range to scan, e.g. 1-1000")
    parser.add_argument("--scan-type", default="all", help="Scan type or combination of scan types")
    parser.add_argument("--wireless-attack", action="store_true", help="Enable wireless attack mode")
    args = parser.parse_args()

    logger.setup_logger()

    if args.mode == "gui":
        try:
            import gui
            gui.run_gui()
        except ImportError as e:
            if "tkinter" in str(e):
                print("Error: GUI mode requires tkinter. Please install tkinter or use CLI mode.")
                print("On Ubuntu/Debian: sudo apt-get install python3-tk")
                print("On CentOS/RHEL: sudo yum install tkinter")
            else:
                print(f"Error importing GUI module: {e}")
            return
        except Exception as e:
            if "DISPLAY" in str(e) or "no display" in str(e).lower():
                print("Error: GUI mode requires a display. Running in headless environment.")
                print("Please use CLI mode instead: python3 main.py --target <IP>")
            else:
                print(f"Error starting GUI: {e}")
            return
    else:
        if args.wireless_attack:
            if not args.target:
                print("Error: Target IP is required for wireless attack mode.")
                return
            wireless_attacks.run_attack(args.target)
        else:
            if not args.target:
                print("Error: Target IP is required for port scanning.")
                return
            port_scanner.run_scan(args.target, args.ports, args.scan_type)

if __name__ == "__main__":
    main()
