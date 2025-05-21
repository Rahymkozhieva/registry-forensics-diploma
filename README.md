# 🧠 Registry Forensics Tools — Diploma Project

## 📘 Project Overview

This repository contains the source code, sample data, and documentation for the diploma project _"Development of a Method for Automatic Extraction of Windows Registry Data in Digital Forensics"_ completed at **Astana IT University**, 2025.

The project includes two independent Python-based tools:
- **Method 1 (Offline Registry Analysis)** — analyzing `.DAT` registry hive files (e.g. `SYSTEM`, `NTUSER.DAT`) using `python-registry3`
- **Method 2 (Live System Analysis)** — scanning a running Windows system using `winreg` to extract digital artefacts in real time

## 🛠 Project Structure


## ⚙️ Technologies Used

- Python 3.11+
- `python-registry3`
- `tkinter`
- `winreg`
- JSON

## 🔍 Features

### ✔ Method 1 — Offline Analysis
- Parses `NTUSER.DAT`, `SYSTEM`, and other `.DAT` registry hive files
- Extracts:
  - USB device history (`USBSTOR`)
  - Autostart programs (`Run`)
- Outputs data to `registry_report.json`
- Works without needing a live Windows environment

### ✔ Method 2 — Live System Scan
- Extracts real-time artefacts from a running Windows system:
  - Installed programs
  - USB history
  - Startup entries
  - Recently executed apps
  - Network adapters
- Outputs to `registry_data.json`
- Simple GUI interface (Tkinter)

## 📷 Screenshots

<p float="left">
  <img src="screenshots/main_menu.png" width="350"/>
  <img src="screenshots/result_run_usb.png" width="350"/>
</p>

## 📄 Diploma Thesis

This project is part of a diploma thesis on the topic:

> "Development of a Method for Automatic Extraction of Windows Registry Data in Digital Forensics"

Submitted to: **Astana IT University, 2025**  
Student: **Еркежан [Your Last Name]**  
Supervisor: *[Supervisor Name]*

## 📁 Sample Outputs

- [`registry_report_sample.json`](method_1_offline_dat/registry_report_sample.json)
- [`registry_data_sample.json`](method_2_live_system/registry_data_sample.json)

## 🛡 Disclaimer

This code is provided for academic and forensic research purposes. Use responsibly and only on systems you are authorized to analyze.

---

