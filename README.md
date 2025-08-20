# 🛡️ Advanced Port Scanner & Wireless Attack Tool

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

A comprehensive, modular port scanner and wireless attack simulation tool designed for ethical hacking, cybersecurity education, and network security assessments.

## ✨ Features

- 🎯 **Advanced Port Scanning** - Multi-threaded scanning with banner grabbing and vulnerability detection
- 🖥️ **GUI & CLI Interfaces** - Both graphical and command-line interfaces available
- 📡 **Wireless Attack Simulation** - Educational wireless security testing modules
- 🌐 **Shodan Integration** - Real-time threat intelligence via Shodan API
- 📊 **Report Generation** - Automated JSON reports with scan results
- 🔄 **Auto Scan Mode** - Comprehensive automated scanning workflows
- 🧵 **Multi-threading** - Fast concurrent scanning capabilities
- 🛡️ **Error Handling** - Robust error handling and graceful failures

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/morningstarxcdcode/port-scanner.git
   cd port-scanner
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **For GUI support (optional):**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # CentOS/RHEL  
   sudo yum install tkinter
   
   # macOS (with Homebrew)
   brew install python-tk
   ```

### Usage

#### Command Line Interface

```bash
# Basic port scan
python3 main.py --target 192.168.1.1 --ports 22,80,443

# Range scanning
python3 main.py --target 192.168.1.1 --ports 1-1000

# Wireless attack simulation
python3 main.py --target 192.168.1.1 --wireless-attack

# GUI mode
python3 main.py --mode gui
```

#### Demo Mode

Run the interactive demo to see all features:

```bash
# Run all demos
python3 demo.py

# Interactive mode
python3 demo.py --interactive
```

## 📁 Project Structure

```
port-scanner/
├── main.py                    # Main entry point
├── demo.py                    # Feature demonstration script
├── gui.py                     # GUI interface
├── scanner/                   # Core scanning modules
│   ├── __init__.py
│   └── port_scanner.py       # Advanced port scanning logic
├── wireless/                  # Wireless attack simulations
│   ├── __init__.py
│   └── wireless_attacks.py
├── integrations/             # Third-party integrations
│   ├── __init__.py
│   └── shodan_integration.py # Shodan API integration
├── reports/                  # Report generation
│   ├── __init__.py
│   └── report_generator.py
├── utils/                    # Utility modules
│   ├── __init__.py
│   └── logger.py            # Logging configuration
├── tests/                    # Unit tests
│   └── test_port_scanner.py
├── .github/workflows/        # CI/CD workflows
│   ├── ci.yml
│   └── release.yml
├── requirements.txt          # Python dependencies
├── setup.py                 # Package setup
└── README.md
```

## 🔧 Configuration

### Environment Variables

- `SHODAN_API_KEY` - Your Shodan API key for real threat intelligence

### API Keys

To use Shodan integration:

1. Sign up at [shodan.io](https://shodan.io)
2. Get your API key
3. Set environment variable:
   ```bash
   export SHODAN_API_KEY="your_api_key_here"
   ```

## 📊 Examples

### Port Scanning

```python
from scanner.port_scanner import run_scan

# Scan specific ports
run_scan("192.168.1.1", "22,80,443,8080")

# Scan port range  
run_scan("192.168.1.1", "1-1000")
```

### Report Generation

```python
from reports.report_generator import generate_report

results = [
    {"port": 22, "status": "open", "service": "SSH"},
    {"port": 80, "status": "open", "service": "HTTP"}
]
generate_report(results, "scan_results.json")
```

### Auto Scan

```python
from auto_scan import run_auto_scan

# Comprehensive scan with all modules
run_auto_scan("192.168.1.1", "1-1000", wireless=True)
```

## 🧪 Testing

Run the test suite:

```bash
# All tests
python -m unittest discover tests/ -v

# Specific test
python -m unittest tests.test_port_scanner -v
```

## 🛠️ Development

### Adding New Features

1. Create feature branch
2. Add tests in `tests/`
3. Implement feature
4. Update documentation
5. Submit pull request

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Include error handling

## 🔒 Security & Ethics

This tool is designed for:
- ✅ Educational purposes
- ✅ Authorized penetration testing
- ✅ Security research on owned systems
- ✅ Network administration

**DO NOT** use for:
- ❌ Unauthorized scanning
- ❌ Malicious activities
- ❌ Attacking systems you don't own

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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

## 🙏 Acknowledgments

- Built with Python and open-source libraries
- Shodan API for threat intelligence
- The cybersecurity community for inspiration and guidance

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/morningstarxcdcode">morningstarxcdcode</a>
</p>