# 🛡️ PORT-SCANNER 🔭 | LIVE Network Security Recon Tool (MacOS)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue.svg" alt="Python 3.13">
  <img src="https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/Security-Hardened-critical" alt="Security">
</p>

<p align="center">
  ⚔️ Monitor network activity, detect scans, and identify threats in real-time with AI-ready scanning modules and next-gen integrations!
</p>

---

## 🎬 Demo Preview

<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOWxjNnU5eTN5emZzd3kxd3FtbXFzZmJmY3BiaWF0emJna3JybThwNiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/XaQzXJym8lREI/giphy.gif" width="75%" alt="Live Threat Monitoring">
  <br/>
  <em>Live Threat Monitoring in Action</em>
</p>

---

## 🚀 Project Overview

`PORT-SCANNER` is a live network security monitoring and recon tool designed for MacOS (and beyond 🧠), combining powerful tools like:

- 🛰️ `nmap`
- 🧠 `shodan`
- 📊 CSV & PDF Report Gen
- 🖼️ GUI + CLI scanner interface
- 🧪 Smart detection scripts

Perfect for:

- 👨‍💻 Ethical Hackers
- 🛡️ Cybersecurity Students
- 🔍 Red/Blue Teams

---

## ⚙️ Core Features

| 🔥 Feature                    | 🧠 Description                                                                 |
|------------------------------|------------------------------------------------------------------------------|
| 🎯 Real-Time Monitoring       | Detect live scans, probes, and suspicious port activity                       |
| 🛰️ Shodan Integration         | Pull device info, known vulns, fingerprints from Shodan API                   |
| 🔭 Nmap Scanning              | Use CLI-powered scans with multiple techniques (stealth, version, OS)         |
| 🖥️ GUI Dashboard              | Visual interface to scan, view results, and control options                   |
| 📝 Auto Logging               | Save all activity into logs + formatted CSV/PDF reports                       |
| 🧪 Vulnerability Detection    | Match banner versions against public CVEs                                    |

---

## 🧱 Project Structure

```bash
PORT-SCANNER/
├── auto_scan.py           # Background scan runner
├── gui.py                 # GUI frontend using Tkinter
├── main.py                # Main controller file
├── shodan_scan.py         # Shodan integration module
├── scanner/               # Core nmap-based scan logic
├── integrations/          # Third-party API integrations
├── reports/               # Auto-generated reports
├── utils/                 # Helper scripts
├── wireless/              # Wireless network scan modules
└── requirements.txt       # All dependencies
```

---

## 🛠️ Built With

- 🐍 Python 3.13  
- 🛰️ [Nmap](https://nmap.org/) – Scan engine  
- 🌐 [Shodan](https://shodan.io/) – Internet intelligence  
- 📦 Libraries:
  - `shodan`, `nmap`, `tkinter`, `fpdf`, `pandas`

---

## 📸 Screenshots & Live Demos

### 🎞️ GUI in Action

**What to Showcase:**

- The main dashboard displaying real-time scan results.
- Interactive elements like buttons or menus.
- Any dynamic graphs or charts representing network activity.

**How to Create:**

- Use screen recording tools like **Gifox** (macOS) or **Peek** (Linux) to capture the GUI in action.
- Keep the recording concise (5-10 seconds) focusing on key interactions.
- Optimize the GIF to be under 10MB for smooth loading on GitHub.

**Example Placeholder:**

```markdown
![GUI Demo](https://github.com/morningstarxcdcode/PORT-SCANNER/assets/YOUR_USERNAME/gui-demo.gif)
```

---

### 🛰️ Live Network Scan Detection

**What to Showcase:**

- Terminal output during a live scan.
- Detection of open ports and services.
- Integration with Shodan API displaying device information.

**How to Create:**

- Record your terminal session using **asciinema** and convert it to an animated SVG using **svg-term-cli**.
- Alternatively, use screen recording tools to capture the terminal output and convert it to a GIF.

**Example Placeholder:**

```markdown
![Live Scan](https://github.com/morningstarxcdcode/PORT-SCANNER/assets/YOUR_USERNAME/live-scan.gif)
```

---

### 📁 Auto Logs + Threat Reports

**What to Showcase:**

- A sample of the generated CSV or PDF report.
- Highlighted sections indicating detected threats or anomalies.
- The process of exporting or viewing reports within the application.

**How to Create:**

- Take high-resolution screenshots of the reports.
- Annotate or highlight key sections to draw attention.
- Ensure sensitive information is redacted or anonymized.

**Example Placeholder:**

```markdown
![Threat Report](https://github.com/morningstarxcdcode/PORT-SCANNER/assets/YOUR_USERNAME/threat-report.png)
```

---

## 🛠️ Advanced Usage Examples

### Targeting Specific Ports

To scan specific ports, you can specify the port range in the input field. For example, to scan ports 22 (SSH) and 80 (HTTP), you can enter:

```
22,80
```

### Using Nmap Options

You can also utilize various `nmap` options by modifying the command in the `advanced_port_scanner.py` file. For example, to enable OS detection, you can add the `-O` flag:

```python
subprocess.Popen(["nmap", "-O", target, port_range])
```

This will provide additional information about the operating system of the target.

---

## 🐍 GitHub Contribution Snake Animation

Add a dynamic snake animation to your README to showcase your GitHub activity in a fun way.

**Steps:**

1. **Set Up the Workflow:**
   - Navigate to your repository's **Actions** tab.
   - Click on **New Workflow** and choose **set up a workflow yourself**.
   - Replace the content with the following:

     ```yaml
     name: Generate Snake Animation

     on:
       schedule:
         - cron: "0 0 * * *"  # Runs daily at midnight
       workflow_dispatch:

     jobs:
       build:
         runs-on: ubuntu-latest
         steps:
           - uses: Platane/snk@master
             with:
               github_user_name: YOUR_USERNAME
               outputs: dist/github-contribution-grid-snake.svg
           - uses: crazy-max/ghaction-github-pages@v2
             with:
               target_branch: output
               build_dir: dist
             env:
               GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
     ```

   - Replace `YOUR_USERNAME` with your GitHub username.

2. **Add to README:**
   - After the workflow runs successfully, add the following to your `README.md`:

     ```markdown
     ![Snake animation](https://github.com/YOUR_USERNAME/YOUR_USERNAME/blob/output/github-contribution-grid-snake.svg)
     ```

   - Replace `YOUR_USERNAME` with your GitHub username.

This animation will display your contributions in a snake-like pattern, adding a dynamic visual to your profile.

---

## 📂 Assets Directory Structure

Organize your assets for clarity and maintainability:

```
PORT-SCANNER/
├── assets/
│   ├── gui-demo.gif
│   ├── live-scan.gif
│   ├── threat-report.png
│   └── github-contribution-grid-snake.svg
├── README.md
└── ...
```

---

## 🛠️ Tools for Creating Visuals

- **Gifox (macOS):** For high-quality screen recordings.
- **Peek (Linux):** Simple GIF recorder for Linux.
- **asciinema:** Record terminal sessions.
- **svg-term-cli:** Convert asciinema recordings to SVG animations.
- **ImageOptim / TinyPNG:** Compress images without losing quality.

---

## 📦 Final Touches

- Ensure all media files are optimized for web (preferably under 10MB).
- Use descriptive alt texts for accessibility.
- Regularly update visuals to reflect the latest features.

By incorporating these enhancements, your `PORT-SCANNER` README will not only be informative but also visually engaging, capturing the attention of users and contributors alike.
