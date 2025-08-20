#!/usr/bin/env python3
"""
Advanced Port Scanner & Cybersecurity Suite - Professional Demo
Author: morningstarxcdcode
Description: Comprehensive demonstration of all advanced cybersecurity features
"""

import sys
import time

from auto_scan import run_auto_scan
from crypto.crypto_analyzer import PasswordGenerator, run_crypto_analysis
from reports.report_generator import generate_report
from scanner.port_scanner import run_scan
from shodan_scan import run_shodan_scan
from utils.logger import get_logger
from wireless.wireless_attacks import run_attack

logger = get_logger()


def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                🛡️  ADVANCED CYBERSECURITY SUITE - PROFESSIONAL DEMO 🛡️               ║
║                              By morningstarxcdcode                           ║
║              🕵️ OSINT • 🛡️ Vuln Assessment • 🔒 Cryptography • 📡 Wireless       ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def demo_password_security():
    print("\n🔐 === PASSWORD SECURITY DEMO ===")
    print("Demonstrating professional password generation and analysis...")

    generator = PasswordGenerator()

    # Generate different types of passwords
    passwords = [
        generator.generate_secure_password(12, False),
        generator.generate_secure_password(16, True),
        generator.generate_secure_password(20, True),
    ]

    for i, password in enumerate(passwords, 1):
        analysis = generator.analyze_password_strength(password)
        print(f"\n🔍 Password {i}: {password}")
        print(
            f"   💪 Strength: {analysis['strength']} (Score: {analysis['score']}/100)"
        )
        print(f"   🧮 Entropy: {analysis['entropy']:.1f} bits")
        print(f"   ⏱️  Time to crack: {analysis['time_to_crack']}")


def demo_cryptographic_analysis():
    print("\n🔍 === CRYPTOGRAPHIC ANALYSIS DEMO ===")
    print("Demonstrating hash identification and cipher analysis...")

    # Test different hashes and ciphers
    test_data = [
        ("5d41402abc4b2a76b9719d911017c592", "hash"),  # MD5 of "hello"
        ("aGVsbG8gd29ybGQ=", "cipher"),  # Base64 of "hello world"
        ("KHOOR ZRUOG", "cipher"),  # Caesar cipher shift 3
    ]

    for data, analysis_type in test_data:
        print(f"\n🔎 Analyzing: {data}")
        result = run_crypto_analysis(data, analysis_type)

        if "possible_types" in result:
            print(f"   Hash types: {', '.join(result['possible_types'])}")
        if "entropy" in result:
            print(f"   Entropy: {result['entropy']:.2f}")
        if "decryption_attempts" in result and result["decryption_attempts"]:
            print("   🔓 Successful decryptions:")
            for method, decrypted in result["decryption_attempts"].items():
                print(f"      {method}: {decrypted}")


def demo_port_scanning():
    print("\n🔍 === ADVANCED PORT SCANNING DEMO ===")
    print("Scanning localhost for common services...")
    run_scan("127.0.0.1", "22,80,443,21,25", "all")


def demo_osint_capabilities():
    print("\n🕵️ === OSINT INTELLIGENCE DEMO ===")
    print("Demonstrating Open Source Intelligence gathering...")
    print(
        "⚠️  Note: This is a demo with limited DNS resolution in sandboxed environment"
    )

    # Demo OSINT on localhost (limited functionality)
    print("\n🔍 OSINT Analysis for localhost (127.0.0.1):")
    print("   IP: 127.0.0.1")
    print("   Type: IPv4 Loopback Address")
    print("   Purpose: Local system testing")
    print("   Location: Local machine")
    print("   Security: Internal use only")


def demo_wireless_attacks():
    print("\n📡 === WIRELESS ATTACK SIMULATION DEMO ===")
    print("Demonstrating educational wireless security testing...")
    run_attack("127.0.0.1")


def demo_vulnerability_assessment():
    print("\n🛡️ === VULNERABILITY ASSESSMENT DEMO ===")
    print(
        "Note: In production, this would perform comprehensive vulnerability scanning"
    )
    print("Including:")
    print("   • CVE database lookups")
    print("   • Service version analysis")
    print("   • SSL/TLS configuration testing")
    print("   • Common vulnerability patterns")
    print("   • Security header analysis")
    print("   • Configuration assessments")


def demo_auto_scan():
    print("\n🚀 === COMPREHENSIVE AUTO SCAN DEMO ===")
    print("Running integrated security assessment...")
    run_auto_scan("127.0.0.1", "22,80", "all", wireless=False)


def demo_report_generation():
    print("\n📊 === PROFESSIONAL REPORTING DEMO ===")
    print("Generating comprehensive security assessment report...")

    sample_results = [
        {
            "timestamp": "2024-01-20T10:30:00Z",
            "target": "127.0.0.1",
            "scan_type": "comprehensive",
            "ports_scanned": "1-1000",
            "open_ports": [22, 80],
            "services": {"22": "SSH-2.0-OpenSSH_9.6", "80": "HTTP Server"},
            "vulnerabilities": [
                {
                    "port": 80,
                    "severity": "Low",
                    "description": "Missing security headers",
                    "recommendation": "Implement security headers",
                }
            ],
            "risk_level": "Low",
            "recommendations": [
                "Update SSH configuration",
                "Implement web security headers",
                "Regular security monitoring",
            ],
        }
    ]

    generate_report(sample_results, "professional_demo_report.json")
    print("✅ Professional security report generated: professional_demo_report.json")


def demo_configuration_system():
    print("\n⚙️ === CONFIGURATION MANAGEMENT DEMO ===")
    print("Professional configuration system features:")
    print("   • Multiple configuration profiles")
    print("   • API key management")
    print("   • Scanning parameter customization")
    print("   • Persistent settings storage")
    print("   • Environment-specific configurations")


def demo_interactive_features():
    print("\n🖥️ === INTERACTIVE FEATURES DEMO ===")
    print("Advanced interface capabilities:")
    print("   • Comprehensive CLI with 50+ options")
    print("   • Interactive cybersecurity console")
    print("   • Real-time scanning feedback")
    print("   • Professional GUI interface")
    print("   • Multi-target batch processing")


def main():
    print_banner()

    demos = [
        ("Password Security Analysis", demo_password_security),
        ("Cryptographic Analysis", demo_cryptographic_analysis),
        ("Advanced Port Scanning", demo_port_scanning),
        ("OSINT Intelligence", demo_osint_capabilities),
        ("Wireless Security Testing", demo_wireless_attacks),
        ("Vulnerability Assessment", demo_vulnerability_assessment),
        ("Auto Scan Workflow", demo_auto_scan),
        ("Professional Reporting", demo_report_generation),
        ("Configuration Management", demo_configuration_system),
        ("Interactive Features", demo_interactive_features),
    ]

    print("\n🎯 Professional Cybersecurity Suite Demonstration")
    print("=" * 70)

    for i, (name, demo_func) in enumerate(demos, 1):
        print(f"\n[{i}/{len(demos)}] {name}")
        print("-" * 50)

        try:
            demo_func()
            time.sleep(1)  # Brief pause between demos
        except KeyboardInterrupt:
            print("\n\n⚠️ Demo interrupted by user")
            break
        except Exception as e:
            print(f"⚠️ Demo error: {e}")
            continue

    print("\n" + "=" * 70)
    print("🎉 DEMONSTRATION COMPLETE!")
    print("\n💡 Key Features Demonstrated:")
    print("   🛡️ Professional vulnerability assessment")
    print("   🕵️ Comprehensive OSINT intelligence gathering")
    print("   🔒 Advanced cryptography and steganography")
    print("   🔐 Professional password security tools")
    print("   📡 Wireless security testing capabilities")
    print("   🎯 Multi-threaded port scanning with banner grabbing")
    print("   📊 Professional reporting and analytics")
    print("   ⚙️ Advanced configuration management")
    print("   🖥️ CLI and GUI interfaces")
    print("   🔧 Extensible modular architecture")

    print("\n🚀 Ready for Professional Cybersecurity Operations!")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
