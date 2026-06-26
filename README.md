# ⚡ Smart Cache Cleaner v1.3.0
🎉 NOW WITH REAL CLEANING & ACTIVE WORKING MODES!

This version introduces the ultimate interactive interface! You can now choose between running a safe simulation to analyze your system or launching a real, deep cleanup of your PC. All physical file deletions, quarantine management, and Recycle Bin emptying functions are now fully unlocked and operational.

A lightweight, high-speed, and open-source system optimizer built with Python. It scans temporary files, calculates system cache recovery, and safely handles unused files through an intelligent quarantine system—all managed directly through an optimized graphical interface.

---

## ✨ Core Features

### 🗑️ Smart Cleanup Workflow
* **Obvious Junk Detection**: Automatically detects and permanently deletes `.tmp`, `.log`, `.bak` files, and zero-byte (0 KB) files cluttering your drive.
* **Intelligent Desktop Quarantine**: Identifies files older than 14 days and moves them to a dedicated folder on your Desktop (`Cleaner_Quarantine`), letting you review them before final removal.
* **Dual Operational Modes**: Separate software paths for a safe simulation preview or a real, destructive operational cleanup.
* **Terminal-Free GUI**: Utilizes native Windows API integration to instantly hide the black command prompt window on startup, rendering only the clean graphical interface.

### ⚡ Performance & Safety
* **High-Speed Scanning**: Analyzes thousands of temporary files inside the Windows `%TEMP%` directory in seconds.
* **Real-Time Progress Bar**: Dynamic live graphical interface showing progress percentage and exact file counts as the scan progresses.
* **100% Privacy & Safety**: Runs entirely offline on your local computer. Zero tracking, zero telemetry.
* **Built-in Guardrails**: Automatically skips symbolic links (`symlinks`) and gracefully handles system-locked or permission-restricted files without crashing.

---

## 🚀 How to Run

To ensure maximum transparency, this software runs directly from its Python source code. This allows you to inspect every single line of code and easily bypass rigid Windows restrictions (like *Smart App Control*).

### Step 1: Install Python
1. Open the **Microsoft Store** on your Windows PC.
2. Search for **Python** (version 3.11, 3.12, or later recommended).
3. Click **Get** → **Install**. It is official, free, and takes seconds.

### Step 2: Download & Run
1. Download the `cleaner.py` file (or save it as `cleaner.pyw` to natively bypass the terminal window).
2. Double-click the file to launch it instantly!

*Alternative for developers (via terminal):*
```bash
python cleaner.py
```

---

## 🎮 Using the GUI

| Button | Action | Color |
| :--- | :--- | :--- |
| **RUN SIMULATION** | **Safe preview mode**: Scans files and calculates potential space recovered without modifying or deleting anything. | 🔴 Red |
| **REAL CLEAN** | **Real cleanup mode**: Launches the full active workflow. Deletes junk, moves old files to quarantine, and prompts to empty the Recycle Bin. | 🟢 Green |
| **CANCEL** | Instantly closes the application safely at any time. | ⚫ Gray |

### The Operational Process Flow
1. **Scan Phase**: Analyzes all files currently residing in the Windows `%TEMP%` directory.
2. **Action Phase**: Executes direct deletion for obvious junk and transfers older files into the Desktop Quarantine folder.
3. **Review Phase**: A dialog window prompts you to check the quarantine folder. Move out anything you want to keep; clicking OK will permanently wipe the remaining discarded files.
4. **Trash Phase**: Offers a native one-click integration to safely empty the Windows Recycle Bin.

---

## 🛡️ Active Safety Features
* **Symlink Skipping**: Automatically ignores symbolic links to prevent any unintended directory escaping.
* **Error Resilience**: Safely skips system-protected or active in-use files without freezing the software thread.
* **Button Locking**: Disables all interactive GUI buttons immediately after a click to prevent accidental double-executions.

---

## 📝 License
Distributed under the MIT License. See the `LICENSE` file for full details.

---

## 🌟 Support the Project & Shape the Community!
This project scales directly with community interaction! Help us hit our development milestones to unlock upcoming features:

🎯 **Community Goal: Help us reach 50 Stars!** ⭐
As soon as this repository hits 50 Stars, I will instantly release the **Version 2.0 "Ultimate Edition"**, featuring deeper cleaning algorithms and full custom exclusions!

Want to see behind-the-scenes development, vote on upcoming updates, or chat directly about the source code? 🎶

[**Join Our WhatsApp Group**](https://whatsapp.com/channel/0029Vb8qa36IiRollahObS2Z) 🚀

Click the link above to join our tech community and help us build the next big update!

*Made with ❤️ for system optimization | Windows Only*

