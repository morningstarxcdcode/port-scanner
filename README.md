# 🛡️ Advanced Port Scanner & Cybersecurity Suite

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Security-Professional-red" alt="Security">
</p>

A comprehensive, modular cybersecurity suite designed for ethical hacking, penetration testing, cybersecurity education, and network security assessments. Built with professional-grade tools and techniques used by cybersecurity experts worldwide.

## ✨ Features

### 🎯 Core Scanning Capabilities
- **Advanced Port Scanning** - Multi-threaded scanning with stealth modes and banner grabbing
- **Vulnerability Assessment** - Professional-grade vulnerability detection and analysis
- **Service Detection** - Comprehensive service enumeration and version detection
- **SSL/TLS Analysis** - Certificate validation and security configuration analysis

### 🕵️ OSINT (Open Source Intelligence)
- **Domain Intelligence** - WHOIS, DNS, subdomain enumeration
- **Certificate Transparency** - SSL certificate history and analysis
- **Social Media Discovery** - Automated social media profile identification
- **Geolocation Analysis** - IP and domain geographical information
- **Reputation Checking** - Multi-source threat intelligence integration
- **Breach Data Analysis** - Data breach history and exposure checking

### 🔒 Cryptography & Steganography
- **Hash Analysis** - Multi-format hash identification and cracking
- **Cipher Analysis** - Classical and modern cipher detection and decryption
- **Password Generation** - Cryptographically secure password creation
- **Password Strength Analysis** - Comprehensive password security assessment
- **Steganography Detection** - Image-based hidden data analysis
- **LSB Analysis** - Least Significant Bit manipulation detection

### 📡 Network Security
- **Wireless Attack Simulation** - Educational wireless security testing
- **Network Reconnaissance** - Advanced network mapping and discovery
- **Protocol Analysis** - Deep packet inspection and analysis
- **Traffic Monitoring** - Real-time network traffic analysis

### 🖥️ Professional Interface
- **CLI Interface** - Comprehensive command-line interface with advanced options
- **GUI Interface** - User-friendly graphical interface for all operations
- **Interactive Mode** - Real-time interactive cybersecurity console
- **Configuration Profiles** - Save and load custom configuration sets

### 📊 Reporting & Analysis
- **Multi-format Reports** - JSON, CSV, PDF, XML output formats
- **Visual Analytics** - Charts and graphs for security metrics
- **Executive Summaries** - High-level security assessment reports
- **Technical Details** - In-depth technical vulnerability information

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/morningstarxcdcode/port-scanner.git
cd port-scanner

# Install dependencies
pip install -r requirements.txt

# Basic usage
python main.py --target example.com --ports 1-1000
```

### Basic Examples

```bash
# Port scanning
python main.py --target 192.168.1.1 --ports 1-1000 --scan-type stealth

# Vulnerability assessment
python main.py --target example.com --vulnerability-scan --ports 80,443

# OSINT gathering
python main.py --target example.com --osint --subdomain-enum

# Password generation
python main.py --password-gen --length 20 --symbols

# Hash analysis
python main.py --crypto-analyze "5d41402abc4b2a76b9719d911017c592" --type hash

# Steganography analysis
python main.py --stego-analyze suspicious_image.png

# Interactive mode
python main.py --interactive
```

## 📁 Project Structure

```
port-scanner/
├── main.py                      # Main entry point with advanced CLI
├── demo.py                      # Feature demonstration script
├── gui.py                       # Professional GUI interface
├── config/                      # Configuration management
│   ├── __init__.py
│   └── config_manager.py        # Advanced configuration system
├── scanner/                     # Core scanning modules
│   ├── __init__.py
│   └── port_scanner.py         # Enhanced port scanning engine
├── vulnerability/               # Vulnerability assessment
│   ├── __init__.py
│   └── vulnerability_scanner.py # Professional vulnerability scanner
├── osint/                      # OSINT gathering tools
│   ├── __init__.py
│   └── osint_gatherer.py       # Comprehensive intelligence gathering
├── crypto/                     # Cryptography & steganography
│   ├── __init__.py
│   └── crypto_analyzer.py      # Advanced crypto analysis tools
├── wireless/                   # Wireless security testing
│   ├── __init__.py
│   └── wireless_attacks.py     # Wireless attack simulations
├── integrations/               # Third-party integrations
│   ├── __init__.py
│   └── shodan_integration.py   # Shodan API integration
├── reports/                    # Report generation
│   ├── __init__.py
│   └── report_generator.py     # Multi-format report generator
├── utils/                      # Utility modules
│   ├── __init__.py
│   └── logger.py              # Professional logging system
├── tests/                      # Comprehensive test suite
│   └── test_port_scanner.py
├── .github/workflows/          # CI/CD workflows
│   ├── ci.yml
│   └── release.yml
├── .circleci/                  # CircleCI configuration
│   └── config.yml
├── requirements.txt            # Python dependencies
├── setup.py                   # Package setup
└── README.md
```

## 🔧 Advanced Configuration

### Configuration Profiles

Create and manage configuration profiles for different use cases:

```bash
# Create a stealth scanning profile
python main.py --create-profile stealth

# Load a specific profile
python main.py --profile stealth --target example.com

# List available profiles
python main.py --list-profiles
```

### API Integration

Configure API keys for enhanced functionality:

```bash
export SHODAN_API_KEY="your_shodan_api_key"
export VIRUSTOTAL_API_KEY="your_virustotal_api_key"
export HAVE_I_BEEN_PWNED_KEY="your_hibp_api_key"
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# All tests
python -m unittest discover tests/ -v

# Specific test modules
python -m unittest tests.test_port_scanner -v

# With coverage report
pip install coverage
coverage run -m unittest discover tests/
coverage report -m
```

## 🛠️ Development

### Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Follow coding standards (use `black`, `isort`, `flake8`)
4. Add comprehensive tests
5. Update documentation
6. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
7. Push to the branch (`git push origin feature/AmazingFeature`)
8. Open a Pull Request

### Code Quality

The project maintains high code quality standards:

```bash
# Code formatting
black .
isort .

# Linting
flake8 .

# Type checking
mypy .

# Security scanning
bandit -r .
```

## 🔒 Security & Ethics

**IMPORTANT**: This tool is designed for **legitimate security testing only**.

### ✅ Authorized Use Cases:
- Educational purposes and learning cybersecurity
- Authorized penetration testing with proper documentation
- Security research on systems you own or have explicit permission to test
- Network administration and security assessment of your own infrastructure
- Bug bounty programs with proper scope and authorization

### ❌ Prohibited Activities:
- Unauthorized scanning or testing of systems you don't own
- Malicious activities or attacks against any systems
- Violating terms of service or applicable laws
- Using the tool for illegal purposes

### Legal Disclaimer:
Users are responsible for compliance with all applicable laws and regulations. Always obtain proper authorization before testing any systems. The developers assume no liability for misuse of this tool.

## 📊 Examples

### Comprehensive Security Assessment

```bash
# Full security assessment of a target
python main.py --target example.com \
               --ports 1-10000 \
               --vulnerability-scan \
               --osint \
               --ssl-scan \
               --output security_report.json \
               --format json
```

### Cryptographic Analysis Workflow

```bash
# Analyze a suspicious hash
python main.py --crypto-analyze "d41d8cd98f00b204e9800998ecf8427e" --type hash

# Generate secure passwords
python main.py --password-gen --length 32 --symbols

# Analyze image for steganography
python main.py --stego-analyze suspicious_image.png
```

### OSINT Investigation

```bash
# Comprehensive domain intelligence
python main.py --target suspicious-domain.com \
               --osint \
               --subdomain-enum \
               --social-media \
               --breach-check \
               --verbose
```

## 🔧 Professional Features

### Multi-Target Scanning
```bash
# Scan multiple targets from file
echo -e "192.168.1.1\n192.168.1.2\nexample.com" > targets.txt
python main.py --targets-file targets.txt --vulnerability-scan
```

### Advanced Output Options
```bash
# Generate executive summary report
python main.py --target example.com --format pdf --output executive_report.pdf

# Quiet mode for scripting
python main.py --target example.com --quiet --output results.json
```

### Performance Tuning
```bash
# High-speed scanning
python main.py --target example.com --threads 200 --timeout 1 --delay 0

# Stealth scanning
python main.py --target example.com --scan-type stealth --delay 1 --threads 10
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/morningstarxcdcode/port-scanner/issues) page
2. Create a new issue if needed
3. Provide detailed information about the problem
4. Include system information and error logs

## 🙏 Acknowledgments

- Built with Python and professional cybersecurity libraries
- Inspired by industry-standard penetration testing tools
- Shodan API integration for threat intelligence
- The cybersecurity community for inspiration and best practices
- Open source security tools and frameworks

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ for the cybersecurity community by <a href="https://github.com/morningstarxcdcode">morningstarxcdcode</a>
</p>

<p align="center">
  <strong>⚡ Built for Security Professionals ⚡</strong>
</p>