"""
Main entry point for Advanced Port Scanner and Wireless Attack Tool
Author: morningstarxcdcode
Poster: morningstarxcdcode's Ethical Hacking Suite
Description: Professional CLI and GUI launcher with modular scanning and advanced cybersecurity options
"""

import argparse
import asyncio
import sys
from pathlib import Path

from config.config_manager import config
from crypto.crypto_analyzer import (
    PasswordGenerator,
    run_crypto_analysis,
    run_steganography_analysis,
)
from osint.osint_gatherer import OSINTGatherer
from scanner import port_scanner
from utils import logger
from vulnerability.vulnerability_scanner import run_vulnerability_scan
from wireless import wireless_attacks


def create_parser():
    """Create comprehensive argument parser."""
    parser = argparse.ArgumentParser(
        description="🛡️ Advanced Port Scanner & Cybersecurity Suite",
        epilog="""
Examples:
  %(prog)s --target 192.168.1.1 --ports 1-1000 --scan-type stealth
  %(prog)s --target example.com --osint --vulnerability-scan
  %(prog)s --target 192.168.1.1 --wireless-attack --interface wlan0
  %(prog)s --crypto-analyze "5d41402abc4b2a76b9719d911017c592" --type hash
  %(prog)s --password-gen --length 20 --symbols
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Target specification
    target_group = parser.add_argument_group("Target Specification")
    target_group.add_argument("--target", help="Target IP address, hostname, or domain")
    target_group.add_argument("--targets-file", help="File containing list of targets")

    # Scanning options
    scan_group = parser.add_argument_group("Scanning Options")
    scan_group.add_argument(
        "--ports",
        default="1-65535",
        help="Port range to scan (e.g., 1-1000, 22,80,443)",
    )
    scan_group.add_argument(
        "--scan-type",
        choices=["stealth", "aggressive", "all", "fast"],
        default="all",
        help="Type of scan to perform",
    )
    scan_group.add_argument(
        "--timeout", type=int, default=3, help="Connection timeout in seconds"
    )
    scan_group.add_argument(
        "--threads", type=int, default=100, help="Number of threads to use"
    )
    scan_group.add_argument(
        "--delay", type=float, default=0, help="Delay between scans in seconds"
    )
    scan_group.add_argument(
        "--retries",
        type=int,
        default=1,
        help="Number of retries for failed connections",
    )

    # Advanced scanning
    advanced_scan_group = parser.add_argument_group("Advanced Scanning")
    advanced_scan_group.add_argument(
        "--vulnerability-scan",
        action="store_true",
        help="Perform vulnerability assessment",
    )
    advanced_scan_group.add_argument(
        "--banner-grab", action="store_true", help="Grab service banners"
    )
    advanced_scan_group.add_argument(
        "--ssl-scan", action="store_true", help="Scan SSL/TLS configurations"
    )
    advanced_scan_group.add_argument(
        "--service-detection", action="store_true", help="Detect running services"
    )

    # OSINT options
    osint_group = parser.add_argument_group("OSINT (Open Source Intelligence)")
    osint_group.add_argument(
        "--osint", action="store_true", help="Perform OSINT gathering"
    )
    osint_group.add_argument(
        "--subdomain-enum", action="store_true", help="Enumerate subdomains"
    )
    osint_group.add_argument(
        "--social-media", action="store_true", help="Find social media profiles"
    )
    osint_group.add_argument(
        "--breach-check", action="store_true", help="Check for data breaches"
    )

    # Wireless options
    wireless_group = parser.add_argument_group("Wireless Attacks")
    wireless_group.add_argument(
        "--wireless-attack",
        action="store_true",
        help="Enable wireless attack simulation",
    )
    wireless_group.add_argument("--interface", help="Wireless interface to use")
    wireless_group.add_argument(
        "--monitor-mode", action="store_true", help="Enable monitor mode"
    )

    # Cryptography options
    crypto_group = parser.add_argument_group("Cryptography & Steganography")
    crypto_group.add_argument(
        "--crypto-analyze", help="Analyze cryptographic data (hash, cipher, etc.)"
    )
    crypto_group.add_argument(
        "--type",
        choices=["hash", "cipher", "auto"],
        default="auto",
        help="Type of cryptographic analysis",
    )
    crypto_group.add_argument("--wordlist", help="Wordlist file for hash cracking")
    crypto_group.add_argument("--stego-analyze", help="Analyze file for steganography")
    crypto_group.add_argument(
        "--password-gen", action="store_true", help="Generate secure password"
    )
    crypto_group.add_argument(
        "--length", type=int, default=16, help="Password length (default: 16)"
    )
    crypto_group.add_argument(
        "--symbols", action="store_true", help="Include symbols in password"
    )

    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument("--output", "-o", help="Output file for results")
    output_group.add_argument(
        "--format",
        choices=["json", "csv", "pdf", "xml", "txt"],
        default="json",
        help="Output format",
    )
    output_group.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    output_group.add_argument(
        "--quiet", "-q", action="store_true", help="Quiet mode - minimal output"
    )
    output_group.add_argument(
        "--no-color", action="store_true", help="Disable colored output"
    )

    # Configuration options
    config_group = parser.add_argument_group("Configuration")
    config_group.add_argument("--config", help="Configuration file to use")
    config_group.add_argument("--profile", help="Configuration profile to load")
    config_group.add_argument(
        "--list-profiles",
        action="store_true",
        help="List available configuration profiles",
    )
    config_group.add_argument(
        "--create-profile", help="Create new configuration profile"
    )

    # Interface options
    interface_group = parser.add_argument_group("Interface")
    interface_group.add_argument(
        "--mode", choices=["cli", "gui"], default="cli", help="Run mode: cli or gui"
    )
    interface_group.add_argument(
        "--interactive", action="store_true", help="Start interactive mode"
    )

    return parser


async def main():
    """Main application entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Setup logging
    logger.setup_logger()
    log = logger.get_logger()

    # Load configuration
    if args.profile:
        if not config.load_profile(args.profile):
            print(f"❌ Profile '{args.profile}' not found")
            return 1

    # Handle configuration commands
    if args.list_profiles:
        profiles = config.list_profiles()
        if profiles:
            print("📋 Available profiles:")
            for profile in profiles:
                print(f"  • {profile}")
        else:
            print("📋 No profiles found")
        return 0

    if args.create_profile:
        current_config = config.config.copy()
        config.create_profile(args.create_profile, current_config)
        print(f"✅ Profile '{args.create_profile}' created")
        return 0

    # Handle password generation
    if args.password_gen:
        generator = PasswordGenerator()
        password = generator.generate_secure_password(args.length, args.symbols)
        analysis = generator.analyze_password_strength(password)

        print(f"🔐 Generated Password: {password}")
        print(f"💪 Strength: {analysis['strength']} (Score: {analysis['score']}/100)")
        print(f"🧮 Entropy: {analysis['entropy']:.1f} bits")
        print(f"⏱️  Time to crack: {analysis['time_to_crack']}")

        if analysis["feedback"]:
            print("💡 Recommendations:")
            for feedback in analysis["feedback"]:
                print(f"  • {feedback}")

        return 0

    # Handle cryptography analysis
    if args.crypto_analyze:
        if args.wordlist and Path(args.wordlist).exists():
            with open(args.wordlist, "r") as f:
                wordlist = [line.strip() for line in f.readlines()]
        else:
            wordlist = None

        result = run_crypto_analysis(args.crypto_analyze, args.type)

        print("🔍 Cryptographic Analysis Results:")
        print(f"Data: {args.crypto_analyze}")

        if "possible_types" in result:
            print(f"Possible hash types: {', '.join(result['possible_types'])}")
            if result.get("cracked_password"):
                print(f"🎯 Cracked password: {result['cracked_password']}")
            else:
                print("❌ Password not found in wordlist")

        if "entropy" in result:
            print(f"Entropy: {result['entropy']:.2f}")
            print(
                f"Possible encodings: {', '.join(result.get('possible_encodings', []))}"
            )
            print(f"Possible ciphers: {', '.join(result.get('possible_ciphers', []))}")

        if "decryption_attempts" in result:
            decryptions = result["decryption_attempts"]
            if decryptions:
                print("🔓 Decryption attempts:")
                for method, decrypted in decryptions.items():
                    print(f"  {method}: {decrypted}")
            else:
                print("❌ No successful decryptions")

        return 0

    # Handle steganography analysis
    if args.stego_analyze:
        if not Path(args.stego_analyze).exists():
            print(f"❌ File not found: {args.stego_analyze}")
            return 1

        result = run_steganography_analysis(args.stego_analyze)

        if "error" in result:
            print(f"❌ {result['error']}")
            return 1

        print("🔍 Steganography Analysis Results:")
        print(f"File: {result.get('filename', args.stego_analyze)}")
        print(f"Format: {result.get('format', 'Unknown')}")
        print(f"Size: {result.get('size', 'Unknown')}")
        print(f"Chi-square test: {result.get('chi_square_test', 0):.2f}")

        if result.get("suspicious_patterns"):
            print("⚠️  Suspicious patterns detected:")
            for pattern in result["suspicious_patterns"]:
                print(f"  • {pattern}")

        if result.get("lsb_analysis"):
            print("🔍 LSB Analysis:")
            for channel, analysis in result["lsb_analysis"].items():
                print(
                    f"  {channel}: {analysis.get('suspicion_level', 'Unknown')} suspicion"
                )

        return 0

    # GUI mode
    if args.mode == "gui":
        try:
            import gui

            gui.run_gui()
            return 0
        except ImportError as e:
            if "tkinter" in str(e):
                print(
                    "❌ GUI mode requires tkinter. Please install tkinter or use CLI mode."
                )
                print("On Ubuntu/Debian: sudo apt-get install python3-tk")
                print("On CentOS/RHEL: sudo yum install tkinter")
            else:
                print(f"❌ Error importing GUI module: {e}")
            return 1
        except Exception as e:
            if "DISPLAY" in str(e) or "no display" in str(e).lower():
                print(
                    "❌ GUI mode requires a display. Running in headless environment."
                )
                print("Please use CLI mode instead: python3 main.py --target <IP>")
            else:
                print(f"❌ Error starting GUI: {e}")
            return 1

    # CLI mode - require target for most operations
    if not args.target and not args.targets_file:
        print("❌ Target is required for scanning operations.")
        print("Use --help for usage information.")
        return 1

    # Determine targets
    targets = []
    if args.target:
        targets.append(args.target)

    if args.targets_file:
        if Path(args.targets_file).exists():
            with open(args.targets_file, "r") as f:
                targets.extend([line.strip() for line in f.readlines() if line.strip()])
        else:
            print(f"❌ Targets file not found: {args.targets_file}")
            return 1

    # Process each target
    for target in targets:
        print(f"\n🎯 Processing target: {target}")
        print("=" * 60)

        # OSINT gathering
        if args.osint:
            print("🕵️ Gathering OSINT intelligence...")
            gatherer = OSINTGatherer()
            intelligence = await gatherer.gather_intelligence(target)
            print(gatherer.generate_osint_report(intelligence))

        # Port scanning
        if not args.osint or args.target:  # Run port scan unless only OSINT requested
            print("🔍 Starting port scan...")

            # Update config with command line options
            if args.timeout:
                config.set("scanning.default_timeout", args.timeout)
            if args.threads:
                config.set("scanning.max_threads", args.threads)
            if args.delay:
                config.set("scanning.scan_delay", args.delay)

            port_scanner.run_scan(target, args.ports, args.scan_type)

        # Vulnerability scanning
        if args.vulnerability_scan:
            print("🛡️ Starting vulnerability assessment...")

            # Parse port range for vulnerability scanning
            port_list = []
            if "," in args.ports:
                parts = args.ports.split(",")
                for part in parts:
                    if "-" in part:
                        start, end = part.split("-")
                        port_list.extend(range(int(start), int(end) + 1))
                    else:
                        port_list.append(int(part))
            elif "-" in args.ports:
                start, end = args.ports.split("-")
                port_list = list(
                    range(int(start), min(int(end) + 1, 1000))
                )  # Limit for performance
            else:
                port_list = [int(args.ports)]

            # Limit ports for vulnerability scanning
            if len(port_list) > 100:
                port_list = port_list[:100]
                print(
                    f"ℹ️  Limiting vulnerability scan to first 100 ports for performance"
                )

            vuln_report = await run_vulnerability_scan(target, port_list)

            print(f"\n🛡️ Vulnerability Assessment Results:")
            print(
                f"Total vulnerabilities found: {vuln_report['summary']['total_vulnerabilities']}"
            )
            print(f"Critical: {vuln_report['summary']['critical']}")
            print(f"High: {vuln_report['summary']['high']}")
            print(f"Medium: {vuln_report['summary']['medium']}")
            print(f"Low: {vuln_report['summary']['low']}")
            print(f"SSL issues: {vuln_report['summary']['ssl_issues']}")

            if vuln_report["vulnerabilities"]:
                print("\n🚨 Vulnerabilities found:")
                for vuln in vuln_report["vulnerabilities"][:10]:  # Show first 10
                    print(
                        f"  • {vuln['cve_id']} ({vuln['severity']}) - Port {vuln['port']}"
                    )
                    print(f"    {vuln['description']}")

        # Wireless attacks
        if args.wireless_attack:
            if not args.target:
                print("❌ Target IP is required for wireless attack mode.")
                continue

            print("📡 Starting wireless attack simulation...")
            wireless_attacks.run_attack(args.target)

    print("\n✅ Scan completed successfully!")
    return 0


def interactive_mode():
    """Start interactive mode."""
    print(
        """
🛡️ Advanced Port Scanner & Cybersecurity Suite - Interactive Mode
================================================================

Available commands:
  scan <target>           - Perform port scan
  osint <target>          - Gather OSINT intelligence  
  vuln <target>           - Vulnerability assessment
  crypto <data>           - Cryptographic analysis
  stego <file>            - Steganography analysis
  wireless <target>       - Wireless attack simulation
  config                  - Show configuration
  help                    - Show this help
  exit                    - Exit interactive mode

"""
    )

    while True:
        try:
            command = input("🔍 cybersec> ").strip()

            if command == "exit":
                break
            elif command == "help":
                print(
                    "Available commands: scan, osint, vuln, crypto, stego, wireless, config, help, exit"
                )
            elif command == "config":
                print(
                    f"Current configuration profile: {config.get('active_profile', 'default')}"
                )
                print(f"Scan timeout: {config.get('scanning.default_timeout')} seconds")
                print(f"Max threads: {config.get('scanning.max_threads')}")
            elif command.startswith("scan "):
                target = command.split(" ", 1)[1]
                port_scanner.run_scan(target, "1-1000", "all")
            else:
                print("Unknown command. Type 'help' for available commands.")

        except KeyboardInterrupt:
            print("\nExiting interactive mode...")
            break
        except EOFError:
            break


if __name__ == "__main__":
    if len(sys.argv) > 1 and "--interactive" in sys.argv:
        interactive_mode()
    else:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
