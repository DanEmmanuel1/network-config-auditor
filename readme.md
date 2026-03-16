# Network Config Auditor

A command-line security tool built in Python that audits Windows network configurations and alerts you to potential vulnerabilities.

---

## 🔍 What It Does

- **Port Scanner** — scans ports 1-1024 and flags risky open ports
- **SSH Auditor** — checks SSH configuration for insecure settings
- **Network Interfaces** — maps all active and inactive network adapters
- **DNS & Routing** — verifies DNS servers and default gateway
- **Firewall Status** — checks Windows Firewall across all profiles
- **Live Connections** — shows active outbound connections in real time
- **Listening Services** — identifies services open to incoming connections
- **Scheduled Scans** — runs automatically every X hours
- **Email Alerts** — sends an email when security risks are detected

---

## 🛠️ Built With

- Python 3.14
- [python-nmap](https://pypi.org/project/python-nmap/) — port scanning
- [psutil](https://pypi.org/project/psutil/) — network interface & connection data
- [paramiko](https://pypi.org/project/paramiko/) — SSH configuration auditing
- [rich](https://pypi.org/project/rich/) — formatted CLI output
- [colorama](https://pypi.org/project/colorama/) — terminal colors
- [schedule](https://pypi.org/project/schedule/) — automated scheduling

---

## 🚀 Getting Started

### Requirements
- Windows 10/11
- Python 3.8+
- [Nmap](https://nmap.org/download.html) installed and added to PATH
- Administrator privileges (required for port scanning)

### Installation

1. Clone the repository:
```
git clone https://github.com/DanEmmanuel1/network-config-auditor.git
cd network-config-auditor
```

2. Create and activate a virtual environment:
```
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up email alerts by creating an `emailer.py` file:
```python
SENDER_EMAIL = "your_gmail@gmail.com"
SENDER_APP_PASSWORD = "your_app_password"
RECEIVER_EMAIL = "your_gmail@gmail.com"
```

---

## 💻 Usage

**Scan your local machine:**
```
py auditor.py
```

**Scan a specific target:**
```
py auditor.py 192.168.1.1
```

**Run scheduled scans with email alerts:**
```
py scheduler.py
```

---

## 📁 Project Structure
```
network-config-auditor/
├── auditor.py            # Main entry point
├── port_scanner.py       # Port scanning module
├── ssh_auditor.py        # SSH config auditor
├── interface_check.py    # Network interface checker
├── dns_check.py          # DNS & routing checker
├── firewall_check.py     # Firewall & connections checker
├── scheduler.py          # Automated scheduling
└── requirements.txt      # Project dependencies
```

---

## ⚠️ Disclaimer

This tool is intended for use on networks and systems you own or have explicit permission to scan. Unauthorized scanning of networks is illegal.

---

## 👤 Author

**DanEmmanuel1**
- GitHub: [@DanEmmanuel1](https://github.com/DanEmmanuel1)