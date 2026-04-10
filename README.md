# Cross-Machine DoS Attack Script for CEH Training

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational%20Use%20Only-red)](LICENSE)
[![CEH](https://img.shields.io/badge/CEH-Training%20Tool-orange)](https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/)

`DOS_juice.py` is an advanced Denial-of-Service (DoS) simulation tool designed for **authorized security testing and CEH training**. It targets the [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) web application running on a remote Ubuntu machine from a Kali Linux attacker system.

> **⚠️ DISCLAIMER:** This script is intended **strictly for educational purposes** and **authorized penetration testing** within controlled environments. Unauthorized use against systems you do not own or have explicit permission to test is **illegal** and **unethical**. The author assumes no liability for misuse.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Attack Vectors](#-attack-vectors)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Command Line Arguments](#-command-line-arguments)
- [Example](#-example)
- [How It Works](#-how-it-works)
- [Output](#-output)
- [Defensive Takeaways (CEH Learning)](#-defensive-takeaways-ceh-learning)
- [Important Notes](#-important-notes)
- [License & Legal](#-license--legal)

---

## 🔍 Overview

This script simulates a multi‑vector DoS attack against a Juice Shop instance. It is designed for **cross‑machine** testing (Kali → Ubuntu), not localhost execution. It demonstrates how an attacker can:

- Flood the server with legitimate‑looking HTTP requests.
- Exhaust connection pools using slow‑header attacks (Slowloris).
- Consume CPU/memory with XML bomb payloads.
- Monitor server responsiveness in real time.

All code is written in Python 3 and uses only standard library modules (`requests`, `threading`, `socket`, etc.) to minimize external dependencies.

---

## ⚡ Attack Vectors

| Vector                | Description                                                                                     | Thread Allocation |
|-----------------------|-------------------------------------------------------------------------------------------------|-------------------|
| **HTTP Flood**        | Rapid GET/POST requests to various Juice Shop endpoints using randomized user agents and delays. | 70%               |
| **Slowloris Simulation** | Keeps many connections open by sending incomplete HTTP requests and slowly drip‑feeding headers. | 20%               |
| **XML Bomb**          | Sends an exponentially expanding XML entity payload to the `/rest/products/reviews` endpoint.    | 10%               |

The script also includes a **SYN flood simulation** (requires root privileges) that is included in the code but not actively launched by default.

---

## 📦 Prerequisites

- **Attacker Machine:** Kali Linux (or any Linux with Python 3.6+)
- **Target Machine:** Ubuntu running OWASP Juice Shop on port `3000`
- **Python Packages:** `requests` (install via `pip`)
- **Optional:** `sudo` / root privileges for raw socket operations (SYN flood)

---

## 🔧 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ceh-dos-juice-shop.git
   cd ceh-dos-juice-shop


## install required Python library
   pip3 install requests

## 🚀 Usage
    Run the script from your Kali terminal, providing the IP address of the Ubuntu target:

    ```bash
    python3 DOS_juice.py -t <TARGET_IP> [OPTIONS]
   Command Line Arguments
## Argument	Description
  -t , --target	(Required) IP address of the Ubuntu machine running Juice Shop.
  -p, --port	Port Juice Shop is listening on (default: 3000).
  -th, --threads	Number of concurrent threads (default: 500).
  -d, --duration	Attack duration in seconds. If omitted, attack runs until interrupted (Ctrl+C)

## 🧠 How It Works
    Initialization: The script builds a list of realistic Juice Shop URLs and user agents.
    
    Banner & Confirmation: It displays attack details and requires the user to type attack to proceed.
    
    Threaded Attack: Based on the thread count, it spawns:

    HTTP flood threads hitting random endpoints.

   Slowloris threads maintaining half‑open connections.

   XML bomb threads posting malicious XML entities.

   Monitoring: A separate thread checks the target’s health every 5 seconds and reports status changes.

   Termination: Attack stops after the specified duration or when interrupted. Final statistics and server status are         displayed. 

## Output
During execution you will see a real‑time status line:

text
[120s] ✅ Success: 15230 ❌ Failed: 412 📊 Rate: 97.4%
When finished, a summary is printed:

text
======================================================================
📊 FINAL ATTACK STATISTICS
======================================================================
⏱️  Duration: 60.2 seconds
✅ Successful requests: 45123
❌ Failed requests: 1877
📈 Total requests: 47000
🚀 Avg requests/sec: 780.4

🔍 Checking final server status...
✅ Server is still responding


## Defensive Takeaways (CEH Learning)
This tool demonstrates why the following security controls are essential:

Rate Limiting: Prevents a single IP from overwhelming the server.

Web Application Firewall (WAF): Blocks malicious payloads and abnormal traffic patterns.

Connection Timeouts & Limits: Mitigates Slowloris‑style attacks.

Content Delivery Network (CDN): Absorbs and distributes volumetric traffic.

Input Validation: Protects against XML bombs and other parser‑based DoS.

## ⚠️ Important Notes
Cross‑Machine Only: The script will refuse to run if localhost or 127.0.0.1 is provided as the target.

Ethical Use: You must have explicit written permission to test the target system.

Performance: The effectiveness of the attack depends on network bandwidth, target server resources, and thread count.

Educational Context: This script is meant to accompany CEH coursework or hands‑on labs—do not use it in production or against real assets.

## 📜 License & Legal
This project is provided for educational use only. There is no formal open‑source license; all rights are reserved by the author. Redistribution or use outside of authorized training environments is prohibited.

By using this software, you agree that you are solely responsible for your actions and that you will adhere to all applicable laws and regulations.

## Happy (Ethical) Hacking! 🔐
Stay curious, stay legal.
