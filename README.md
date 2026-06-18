# ⚡ Smart Cache Cleaner v2.0.0

### 🎉 NOW WITH FULL CLEANING FEATURES!
This is **no longer a simulation**. The software now performs **real, permanent file deletion and optimization** with a professional quarantine system. Always run a simulation first to preview what will be deleted!

---

A lightweight, high-speed, and open-source system cleaner built with Python. It scans temporary files, removes junk, quarantines old files, and recovers disk space—all while keeping your personal data safe.

## ✨ Core Features

### 🗑️ Smart Cleanup System
* **Real File Deletion:** Automatically removes `.tmp`, `.log`, `.bak`, `.cache`, `.temp` files (configurable).
* **Intelligent Quarantine:** Old & unused files are moved to a secure quarantine folder on your Desktop instead of immediate deletion.
* **Safety-First Approach:** Review quarantined files before permanent deletion—restore anything you need.
* **Dry-Run Mode:** Run a simulation first to see exactly what will be cleaned, no files touched!

### ⚡ Performance & Safety
* **High-Speed Scanning:** Analyzes thousands of temporary files in seconds.
* **Real-Time Progress Bar:** Live GUI showing cleanup progress and file count.
* **100% Privacy & Safety:** Runs entirely offline on your local computer. Zero telemetry.
* **Symlink Protection:** Automatically skips symbolic links and system-critical files.
* **Detailed Logging:** All operations logged to `Desktop/Cleaner_Logs/` for audit trails.

### 🎯 Advanced Features
* **JSON Configuration:** Fully customizable via `cleaner_config.json`.
* **Automatic Trash Cleanup:** Optional automatic Windows Recycle Bin emptying.
* **Error Resilience:** Gracefully handles permission errors and inaccessible files.
* **Multi-threaded GUI:** Non-blocking interface with cancellation support.
* **Detailed Report:** Post-cleanup summary with space freed, files moved, failed operations.

## 📋 Configuration

The tool creates a config file on first run: `~/Desktop/cleaner_config.json`

```json
{
    "junk_extensions": [".tmp", ".log", ".bak", ".cache", ".temp"],
    "days_threshold": 14,
    "enable_logging": true,
    "scan_subdirectories": true,
    "file_size_threshold_kb": 0,
    "timeout_per_file_seconds": 5
}
```

**Customize these settings:**
- `junk_extensions`: Add/remove file types to target
- `days_threshold`: Files unused longer than this are quarantined (in days)
- `file_size_threshold_kb`: Minimum file size to consider (0 = empty files)
- `enable_logging`: Toggle detailed operation logs

## 🚀 How to Run

### Step 1: Install Python
1. Open **Microsoft Store** on your Windows PC.
2. Search for **Python** (version 3.11, 3.12, or later recommended).
3. Click **Get** → **Install**. Official, free, takes seconds.

### Step 2: Download & Run
1. Download `cleaner.py` from this repository.
2. Double-click the file to launch instantly!

**From Terminal (Advanced):**
```bash
python cleaner.py
```

## 🎮 Using the GUI

| Button | Action |
|--------|--------|
| **▶ PULIZIA REALE** | Start real cleaning (scans → deletes junk → quarantines old files) |
| **🔍 SIMULAZIONE** | Preview mode: see what will be cleaned without any changes |
| **⏹ ANNULLA** | Stop the operation at any time |

### Cleanup Workflow
1. **Scan Phase:** Analyzes all files in `%TEMP%` directory
2. **Action Phase:** 
   - Direct deletion for obvious junk files
   - Quarantine for old/unused files (review first!)
3. **Review Phase:** Inspect quarantined files, restore anything important
4. **Trash Phase:** Option to empty Windows Recycle Bin
5. **Report:** Summary with space freed and operation stats

## 📊 Output Files

After cleanup, you'll find:
- **Cleaner_Quarantine** (Desktop): Temporarily holds old files for review
- **Cleaner_Logs** (Desktop): Detailed operation logs with timestamps

## 🛡️ Safety Features

✅ **Symlink Detection:** Never follows symbolic links (prevents system damage)  
✅ **Permission Handling:** Gracefully skips files you don't have access to  
✅ **Quarantine System:** Review before permanent deletion  
✅ **Backup Logs:** Every operation logged for recovery reference  
✅ **Error Recovery:** Continues processing on individual file errors  
✅ **Cancellable:** Stop anytime without partial damage  

## 📝 License

Distributed under the **MIT License**. See `LICENSE` for full details.

## 🚀 Roadmap

- ✅ v2.0.0 (Current) - Full cleaning + quarantine system
- 🔜 v2.1 - Cloud backup integration for quarantined files
- 🔜 v2.2 - Browser cache & temp profile cleaning
- 🔜 v2.3 - Scheduled automated cleanup tasks
- 🔜 v3.0 - Advanced registry cleaning & optimization

## 🌟 Show Your Support

If this tool has saved you disk space and helped your PC run faster, please:
- ⭐ **Star this repository**
- 🐛 **Report bugs** via GitHub Issues
- 💡 **Suggest features** you'd like to see
- 🤝 **Contribute** improvements via Pull Requests

---

**⚠️ DISCLAIMER:** This software modifies your file system. Always:
1. Backup important data first
2. Run simulation mode before actual cleanup
3. Review quarantined files before final deletion
4. Use at your own risk

**Made with ❤️ for system optimization | Windows Only (for now)**
